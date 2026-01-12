import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import argparse 

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")


client = genai.Client(api_key=api_key)

user_prompt = argparse.ArgumentParser(description="Generate content using Gemini API")
user_prompt.add_argument("prompt", type=str, help="The prompt to generate content for")
user_prompt.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = user_prompt.parse_args()
prompt = args.prompt

messages = [
    types.Content(
        role="user",
        parts=[types.Part(text=prompt)]
    )
]
response = client.models.generate_content(
    model="gemini-2.5-flash", contents=messages
)

if api_key is None:
    raise ValueError("GEMINI_API_KEY environment variable not set")

if response.usage_metadata:
    prompt_tokens = response.usage_metadata.prompt_token_count
    response_tokens = response.usage_metadata.candidates_token_count
else: 
    raise RuntimeError("No usage metadata found in the response.")


def main():
    if args.verbose:
        print("User prompt:", prompt)
        print("Prompt tokens:", prompt_tokens)
        print("Response tokens:", response_tokens)
        print(response.text)
    else: 
        print(response.text)

if __name__ == "__main__":
    main()
