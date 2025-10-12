import os
import sys
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    
    if not api_key:
        print("Error: GEMINI_API_KEY not set.")
        sys.exit(1)

    client = genai.Client(api_key=api_key)

    parser = argparse.ArgumentParser(
        description="An LLM-powered command-line program capable of reading, updating, and running Python code using the Gemini API."
    )

    parser.add_argument(
        'prompt',
        type=str,
        help='The text prompt to send to the generative model'
    )

    parser.add_argument(
        '--verbose',
        '-v',
        action='store_true',
        help='Enable verbose output for detailed steps and debugging.'
    )

    args = parser.parse_args()

    messages = [
        types.Content(role="user", parts=[types.Part(text=args.prompt)]),
    ]

    try:
        response = client.models.generate_content(
            model='gemini-2.0-flash-001',
            contents=messages,
        )
    except Exception as e:
        print(f"generate_content failed: {e}")
        sys.exit(1)

    try:
        meta = getattr(response, "usage_metadata", None)
        if args.verbose:
            print()
            print(f'User prompt: "{args.prompt}"')
            if meta is not None:
                if hasattr(meta, "prompt_token_count"):
                    print(f"Prompt tokens: {meta.prompt_token_count}")
                if hasattr(meta, "candidates_token_count"):
                    print(f"Response tokens: {meta.candidates_token_count}")
        print(response.text)
    except Exception as e:
        print(f"failed to read response: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
