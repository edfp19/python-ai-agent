import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
import argparse
import prompts
from functions.call_function import available_functions, call_function


def main():
    load_dotenv()

    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise ValueError("GEMINI_API_KEY environment variable not set")

    client = genai.Client(api_key=api_key)

    parser = argparse.ArgumentParser(description="Generate content using Gemini API")
    parser.add_argument("prompt", type=str, help="The prompt to generate content for")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    prompt = args.prompt

    messages = [types.Content(role="user", parts=[types.Part(text=prompt)])]

    
    for _ in range(20):
        response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config=types.GenerateContentConfig(
            system_instruction=prompts.system_prompt,
            tools=[available_functions],
            temperature=0.0,
        ),
    )
        if response.candidates:
            for candidate in response.candidates:
                messages.append(candidate.content)
        if response.usage_metadata:
            prompt_tokens = response.usage_metadata.prompt_token_count
            response_tokens = response.usage_metadata.candidates_token_count
        else:
            raise RuntimeError("No usage metadata found in the response.")
        if args.verbose:
            print("User prompt:", prompt)
            print("Prompt tokens:", prompt_tokens)
            print("Response tokens:", response_tokens)
        if response.function_calls:
            function_results = []
            for function_call in response.function_calls:
                function_call_result = call_function(function_call, args.verbose)
                if function_call_result.parts == [] or function_call_result.parts is None:
                    raise Exception("Function call result has no parts")
                if function_call_result.parts[0].function_response is None:
                    raise Exception("Function call result part has no function response")
                if function_call_result.parts[0].function_response.response is None:
                    raise Exception(
                        "Function call result part has no function response content"
                    )
                function_results.append(function_call_result.parts[0])
                print(f" - Calling function: {function_call.name}")
            messages.append(types.Content(role="user", parts=function_results))
        else: 
            print(response.text)
            break
    else:
        print("Reached maximum number of iterations without a final response.")
        sys.exit(1)


if __name__ == "__main__":
    main()
