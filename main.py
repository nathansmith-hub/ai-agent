# python
import os
import sys
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types

def main():
    # Load environment variables from a .env file if present
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    
    # Fail fast if no API key is configured
    if not api_key:
        print("Error: GEMINI_API_KEY not set.")
        sys.exit(1)

    #Initialize the Gemini client with explicit credentials
    client = genai.Client(api_key=api_key)

    #Configure CLI interface and usage documentation
    parser = argparse.ArgumentParser(
        description="An LLM-powered command-line program capable of reading, updating, and running Python code using the Gemini API."
    )

    # Required free-form prompt to send to the model
    parser.add_argument(
        'prompt',
        type=str,
        help='The text prompt to send to the generative model'
    )

    #Optional verbose flag to print request/response metadata
    parser.add_argument(
        '--verbose',
        '-v',
        action='store_true',
        help='Enable verbose output for detailed steps and debugging.'
    )

    args = parser.parse_args()

    # Construct a single-turn message for the API
    messages = [
        types.Content(role="user", parts=[types.Part(text=args.prompt)]),
    ]

    try:
        # Call the fast generation model for low-latency responses
        response = client.models.generate_content(
            model='gemini-2.0-flash-001',
            contents=messages,
        )
    except Exception as e:
        # Network/auth/model errors surface here
        print(f"generate_content failed: {e}")
        sys.exit(1)

    try:
        # Optional: print prompt and token usage when verbose
        meta = getattr(response, "usage_metadata", None)
        if args.verbose:
            print()
            print(f'User prompt: "{args.prompt}"')
            if meta is not None:
                if hasattr(meta, "prompt_token_count"):
                    print(f"Prompt tokens: {meta.prompt_token_count}")
                if hasattr(meta, "candidates_token_count"):
                    print(f"Response tokens: {meta.candidates_token_count}")
        #Primary output: plain text body of the model response
        print(response.text)
    except Exception as e:
        # Handle unexpected response shapes or access errors
        print(f"failed to read response: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Entrypoint guard for direct CLI execution
    main()
