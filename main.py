import os
from dotenv import load_dotenv
from google import genai
import sys
from google.genai import types
from prompts import system_prompt
from call_function import available_functions
from call_function import call_function

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


def generate_content(client, messages, verbose):
    max_iterations = 20
    for _ in range(max_iterations):
        try:
            response = client.models.generate_content(
                model='gemini-2.0-flash-001',
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions], system_instruction=system_prompt),
            )

            if verbose:
                print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
                print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

            # Add the model's response to the conversation history
            if response.candidates:
                for candidate in response.candidates:
                    messages.append(candidate.content)

            # --- START FIX ---
            # **Priority 1: Check for and process function calls.**
            if response.function_calls:
                for call in response.function_calls:
                    function_call_result = call_function(call, verbose)

                    if not function_call_result.parts or not getattr(function_call_result.parts[0], "function_response", None) or function_call_result.parts[0].function_response.response is None:
                        raise RuntimeError("Function call did not return a valid function_response.response")

                    if verbose:
                        print(f"-> {function_call_result.parts[0].function_response.response}")
                    
                    # Add the function call result to the conversation history
                    messages.append(function_call_result)
                
                # After processing all calls, continue to the next loop iteration
                # to send the function results back to the model.
                continue

            # **Priority 2: If no function calls, check for a final text response.**
            if response.text:
                print(f"Final response:\n{response.text}")
                break # We are done

            # **Priority 3: Handle unexpected state (no text, no calls).**
            if not response.text and not response.function_calls:
                print("Warning: Model returned no text and no function calls.")
                break
            # --- END FIX ---

        except Exception as e:
            print(f"An error occurred: {e}")
            break
    else:
        print("Maximum iterations reached. Exiting.")


if __name__ == "__main__":
    main()