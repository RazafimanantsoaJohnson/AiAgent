import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import get_files_info

messages = []

supported_params = ["--verbose"]

def main():
    load_dotenv()

    api_key = os.environ.get("GEMINI_API_KEY")

    if (len(sys.argv) < 2):
        raise Exception("there are missing arguments please check")
        return
    
    prompt = sys.argv[1]

    messages.append(
        types.Content(role="user", parts=[types.Part(text=prompt)])
    )
    print(get_files_info(os.getcwd(), "./calculator"))

    return 

    client = genai.Client(api_key= api_key)
    response = client.models.generate_content(model= "gemini-2.0-flash-001", contents=messages )
    
    # print(response.text)
    if supported_params[0] in sys.argv:
        print(f"User prompt: {prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")


if __name__ == "__main__":
    main()
