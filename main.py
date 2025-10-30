# python
import os
import sys
import argparse

from dotenv import load_dotenv
from google import genai
from google.genai import types

from config import MAX_ITERS
from prompts import system_prompt
from call_functions import available_functions
from functions.call_function import call_function

def main():
    # Load env vars from .env if present
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    
    # Fail fast if API key missing
    if not api_key:
        print("Error: GEMINI_API_KEY not set.")
        sys.exit(1)

    # Create Gemini client
    client = genai.Client(api_key=api_key)

    # CLI setup
    parser = argparse.ArgumentParser(
        description="LLM-powered CLI that can read, update, and run Python code via Gemini tools."
    )
    parser.add_argument(
        'prompt',
        type=str,
        help='Free-form prompt for the model'
    )
    parser.add_argument(
        '--verbose',
        '-v',
        action='store_true',
        help='Enable detailed output'
    )
    args = parser.parse_args()

    # Seed the conversation with the user prompt
    messages = [
        types.Content(role="user", parts=[types.Part(text=args.prompt)]),
    ]

    # Agent loop: iterate tool->model until final text or max iters
    for _ in range(MAX_ITERS):
        try:
            # Ask the model for the next step using full message history
            response = client.models.generate_content(
                model='gemini-2.0-flash-001',
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions],           # advertise available tools
                    system_instruction=system_prompt,      # steer behavior toward tool use
                ),
            )

            # Add all candidate contents to the conversation
            if getattr(response, "candidates", None):
                for cand in response.candidates:
                    if cand.content is not None:
                        messages.append(cand.content)

        except Exception as e:
            # Handle API call failures
            print(f"generate_content failed: {e}")
            sys.exit(1)

        try:
            # Optional usage metadata
            meta = getattr(response, "usage_metadata", None)
            if args.verbose:
                print()
                print(f'User prompt: "{args.prompt}"')
                if meta is not None:
                    if hasattr(meta, "prompt_token_count"):
                        print(f"Prompt tokens: {meta.prompt_token_count}")
                    if hasattr(meta, "candidates_token_count"):
                        print(f"Response tokens: {meta.candidates_token_count}")

            # If the model requested tool calls, execute them
            calls = getattr(response, "function_calls", None)
            if calls:
                for fc in calls:
                    # Dispatch the tool call to our implementation
                    function_call_result = call_function(fc, verbose=args.verbose)

                    # Validate/peek into the tool response payload (optional)
                    try:
                        resp = function_call_result.parts[0].function_response.response

                        # Append the structured tool response for the next turn
                        messages.append(
                            types.Content(
                                role="user",
                                parts=[
                                    types.Part(
                                        function_response=function_call_result.parts[0].function_response
                                    )
                                ],
                            )
                        )

                    except Exception:
                        # The tool must return a standardized Content shape
                        raise RuntimeError("Function call returned invalid Content shape")
                    
                    # Verbose: show summarized tool output
                    if args.verbose:
                        print(f"-> {resp}")

                # Continue so the model can react to tool outputs
                continue

            # No tool calls: if we have final text, print and exit
            if response.text:
                print(response.text)
                break

        except Exception as e:
            # Handle unexpected response shapes or output errors
            print(f"failed to read response: {e}")
            sys.exit(1)

if __name__ == "__main__":
    # CLI entry point
    main()
    