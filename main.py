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
    # Load environment variables from .env file (if it exists)
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    
    # Exit immediately if the API key isn't configured
    if not api_key:
        print("Error: GEMINI_API_KEY not set.")
        sys.exit(1)

    # Initialize the Gemini API client
    client = genai.Client(api_key=api_key)

    # Set up CLI argument parsing
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

    # Start the conversation history with the user's input
    messages = [
        types.Content(role="user", parts=[types.Part(text=args.prompt)]),
    ]

    #  Run the agent loop: let the model call tools and respond until it finishes or hits the iteration limit
    for _ in range(MAX_ITERS):
        try:
            # Send the conversation history to Gemini and get the next response
            response = client.models.generate_content(
                model='gemini-2.0-flash-001',
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions],           # provide the list of callable tools
                    system_instruction=system_prompt,      # guide the model's behavior
                ),
            )

            # Check that we received a valid response
            if not response:
                raise RuntimeError("Gemini API returned empty response")

            # Add the model's response to the conversation history
            if getattr(response, "candidates", None):
                for cand in response.candidates:
                    if cand.content is not None:
                        messages.append(cand.content)
            
            else:
                # Missing candidates might indicate rate limiting or API problems
                raise RuntimeError("Gemini API response contained no candidates")

        except ValueError as e:
            # The request had invalid parameters
            print(f"Invalid request parameters:  {e}")
            sys.exit(1)

        except ConnectionError as e:
            # Network connection to the API failed
            print(f"Network error connecting to Gemini API:  {e}")
            sys.exit(1)

        except Exception as e:
            # Catch any other errors from the API call
            print(f"generate_content failed: {e}")
            sys.exit(1)

        try:
            # Display token usage information if verbose mode is enabled
            meta = getattr(response, "usage_metadata", None)
            if args.verbose:
                print()
                print(f'User prompt: "{args.prompt}"')
                if not meta:
                    print("Warning:  No usage metadata available.")
                else:
                        print(f"Prompt tokens: {meta.prompt_token_count}")
                        print(f"Response tokens: {meta.candidates_token_count}")

            # Check if the model wants to call any tools (functions)
            calls = getattr(response, "function_calls", None)
            if calls:
                for fc in calls:
                    try:
                        # Execute the requested function and get the result
                        function_call_result = call_function(fc, verbose=args.verbose)

                        # Ensure the function returned a properly structured result
                        if not function_call_result.parts:
                            raise RuntimeError(f"Function '{fc.name}' returned no parts")
                        
                        if not function_call_result.parts[0].function_response:
                            raise RuntimeError(f"Function '{fc.name}' returned invalid response structure")

                        # Extract the actual response data from the function result
                        resp = function_call_result.parts[0].function_response.response

                        # Add the function's output to the conversation so the model can see it
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

                        # Show the function output in verbose mode
                        if args.verbose:
                            print(f"-> {resp}")

                    except RuntimeError as e:
                        print(f"Function call error:  {e}")
                        sys.exit(1)
                    
                    except (IndexError, AttributeError) as e:
                        print(f"Function '{fc.name}' returned malformed response:  {e}")
                        sys.exit(1)

                # Go back to the start of the loop so the model can process the function results
                continue

            # If there are no function calls, check for a final text response
            if response.text:
                print(response.text)
                break

        except Exception as e:
            # Handle any unexpected errors while processing the response
            print(f"failed to read response: {e}")
            sys.exit(1)

    else:
        # This executes only if the loop finished without breaking (hit max iterations)
        print(f"Warning: Agent reached maximum iterations ({MAX_ITERS}) without completing")
        sys.exit(1)

if __name__ == "__main__":
    # Run the main function when this script is executed directly
    main()
    
