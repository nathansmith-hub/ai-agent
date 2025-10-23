# python
import os
import sys
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info

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

    # Required, free-form prompt to send to the model
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

    args = parser.parse_args()

    # Build a single-turn user message for the API
    messages = [
        types.Content(role="user", parts=[types.Part(text=args.prompt)]),
    ]

    # Declare available tool(s) for the model (function schemas only)
    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
        ]
    )

    try:
        # System instruction guiding the model’s tool-usage behavior
        system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""
        # Invoke the model with tools enabled
        response = client.models.generate_content(
            model='gemini-2.0-flash-001',
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions],
                system_instruction=system_prompt,
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

        # Primary output: prefer function-calls over free-form text
        calls = getattr(response, "function_calls", None)
        if calls:
            for fc in calls:
                print(f"Calling function: {fc.name}({fc.args})")
        else:
            print(response.text)
    except Exception as e:
        # Handle unexpected response shapes or printing errors
        print(f"failed to read response: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Standard CLI entrypoint
    main()
