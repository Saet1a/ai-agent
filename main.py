import os
from dotenv import load_dotenv
from google import genai
import sys
from google.genai import types




def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    verbose = "--verbose" in sys.argv
    arguments = []

    for arg in sys.argv[1:]:
        if not arg.startswith("--"):
            arguments.append(arg)    

    if not arguments:
        print("Please provide a prompt as a command line argument.")
        sys.exit(1)

    prompt = " ".join(arguments)

    if verbose:
        print(f"User prompt: {prompt}\n")

    messages = [
    types.Content(role="user", parts=[types.Part(text=prompt)]),]

    generate_content(client,messages,verbose)


def generate_content(client,messages,verbose):
    response = client.models.generate_content(
        model='gemini-2.0-flash-001',
        contents=messages,
    )
    print(response.text)
    if verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")


if __name__ == "__main__":
    main()
