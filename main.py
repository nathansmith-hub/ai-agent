# python
import os
import sys
import argparse

from dotenv import load_dotenv
from google import genai
from google.genai import types

from prompts import system_prompt
from call_functions import available_functions
from functions.call_function import call_function

def main():
    # Load environment variables from a .env file if present
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    
    # Exit early if the API key is missing
    if not api_key:
        print("Error: GEMINI_API_KEY not set.")
        sys.exit(1)

    # Initialize the Gemini client using the provided API key
    client = genai.Client(api_key=api_key)

    # Configure the CLI interface and help text
    parser = argparse.ArgumentParser(
        description="An LLM-powered command-line program capable of reading, updating, and running Python code using the Gemini API."
    )

    # Required positional argument: free-form prompt for the model
    parser.add_argument(
        'prompt',
        type=str,
        help='The text prompt to send to the generative model'
    )

    # Optional verbosity flag for additional diagnostics
    parser.add_argument(
        '--verbose',
        '-v',
        action='store_true',
        help='Enable verbose output for detailed steps and debugging.'
    )

    # Parse CLI arguments
    args = parser.parse_args()

    # Build a single-turn user message for the API
    messages = [
        types.Content(role="user", parts=[types.Part(text=args.prompt)]),
    ]

    try:
        # Invoke the model with tool definitions and a system instruction
        response = client.models.generate_content(
            model='gemini-2.0-flash-001',
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions],   # advertise callable tools
                system_instruction=system_prompt,  # steer the model’s behavior
            ),
        )
    except Exception as e:
        # Surface model invocation failures
        print(f"generate_content failed: {e}")
        sys.exit(1)

    try:
        # Optionally print request/response metadata when verbose
        meta = getattr(response, "usage_metadata", None)
        if args.verbose:
            print()
            print(f'User prompt: "{args.prompt}"')
            if meta is not None:
                if hasattr(meta, "prompt_token_count"):
                    print(f"Prompt tokens: {meta.prompt_token_count}")
                if hasattr(meta, "candidates_token_count"):
                    print(f"Response tokens: {meta.candidates_token_count}")

        # Prefer executing tool calls over printing free-form text
        calls = getattr(response, "function_calls", None)
        if calls:
            for fc in calls:
                # Route the model's function call to our dispatcher
                function_call_result = call_function(fc, verbose=args.verbose)

                # Validate the standardized tool response shape
                try:
                    resp = function_call_result.parts[0].function_response.response
                except Exception:
                    raise RuntimeError("Function call returned invalid Content shape")
                
                # Show the tool result in verbose mode
                if args.verbose:
                    print(f"-> {resp}")
        else:
            # Fall back to plain text if no function call was requested
            print(response.text)
    except Exception as e:
        # Handle unexpected response shapes or printing errors
        print(f"failed to read response: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Standard CLI entrypoint
    main()
