import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import get_files_info, schema_get_files_info, schema_get_file_content
from functions.run_code import schema_run_python_file
from functions.write_file import schema_write_file
from call_functions import call_function

messages = []

supported_params = ["--verbose"]

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

available_functions = types.Tool(
    function_declarations= [
        schema_get_files_info ,schema_get_file_content, schema_write_file, schema_run_python_file #, schema_run_python_file, schema_get_file_content, schema_write_file
    ]
)

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

    client = genai.Client(api_key= api_key)
    config = types.GenerateContentConfig(
        tools= [available_functions], system_instruction= system_prompt
    )
    response = client.models.generate_content(
        model= "gemini-2.0-flash-001", contents=messages, config= config
    )

    isVerboseSet = supported_params[0] in sys.argv
    
    if isVerboseSet:
        print(f"User prompt: {prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    
    if len(response.function_calls) == 0:
        print(response.text)
        return
    
    for function_call in response.function_calls:
        function_call_result = call_function(function_call ,isVerboseSet)
        if function_call_result.parts[0].function_response.response == None:
            raise Exception(f"Something went wrong when calling the function: {function_call_result}")
        
        if isVerboseSet:
            print(f"-> {function_call_result.parts[0].function_response.response}")



if __name__ == "__main__":
    main()
