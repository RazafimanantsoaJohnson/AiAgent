from functions.get_files_info import get_files_info, get_file_content, schema_get_files_info, schema_get_file_content
from functions.run_code import run_python_file
from functions.write_file import write_file
from google.genai import types


def call_function(function_call_part, verbose=False):
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")
    result = ""
    function_call_part.args['working_directory']= "./calculator"

    function_dict = {
        'get_files_info': get_files_info,
        'get_file_content': get_file_content,
        'write_file': write_file,
        'run_python_file': run_python_file
    }

    if function_dict[function_call_part.name] == None:
        print(f"unrecognized function: {function_call_part.name}")
        return types.Content(
            role= "tool",
            parts= [
                types.Part.from_function_response(
                    name= function_call_part.name,
                    response= {"error": f"Unknown function: {function_call_part.name}"}
                )
            ]
        )
    result= (function_dict[function_call_part.name])(**function_call_part.args)
    return types.Content(
        role= "tool",
        parts= [
            types.Part.from_function_response(
                name= function_call_part.name,
                response= {"result": result},
            )
        ]
    )

    # match function_call_part.name:
    #     case "get_files_info":
    #         result = get_files_info(**function_call_part.args)
    #         break
    #     case "get_file_content":
    #         result = get_file_content(**function_call_part.args)
    #         break
    #     case "write_file":
    #         result = write_file(**function_call_part.args)
    #         break
    #     case "run_python_file":
    #         result = run_python_file(**function_call_part.args)
    #         break
    #     case _:
    #         print("unrecognized function")
    
