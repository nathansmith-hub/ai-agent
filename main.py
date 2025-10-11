import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    
    if not api_key:
        print("Error: GEMINI_API_KEY not set.")
        sys.exit(1)
    
    if len(sys.argv) < 2:
        print("Error: A command line prompt is required.")
        sys.exit(1)

    user_prompt = sys.argv[1]
    client = genai.Client(api_key=api_key)

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
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
        print(response.text)
        meta = getattr(response, "usage_metadata", None)
        if meta:
            print()
            print(f"Prompt tokens: {meta.prompt_token_count}")
            print(f"Response tokens: {meta.candidates_token_count}")
    except Exception as e:
        print(f"failed to read response: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
