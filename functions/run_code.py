import os
import subprocess
from config import SUBPROCESS_EXECUTION_TIMEOUT
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Will run the python file at the specified path. (Run the code and return the stdout, stderr in a string)",
    parameters = types.Schema(
        type= types.Type.OBJECT,
        properties= {
            "file_path": types.Schema(
                type= types.Type.STRING,
                description= "Required parameter to specify the python code to run.",
            ),
            "args": types.Schema(
                type= types.Type.ARRAY, 
                items= types.Schema(
                    type= types.Type.STRING,
                    description= "Optional argument to pass to the python file"
                
                ),
                description= "An array of strings defining the arguments to pass to the python run command. Not mandatory (send an empty array as a zero value)"
            )
        }
    )
)

# types.FunctionDeclaration(
#     name="write_file",
#     description="Write content into a specific file; it will create the file if it doesn't exist. Will mostly be used to write python code to modify codebase in our case.",
#     parameters = types.Schema(
#         type= types.Type.OBJECT,
#         properties= {
#             "file_path": types.Schema(
#                 type= types.Type.STRING,
#                 description= "Required parameter to specify the file to write into; can be a non-existent file.",
#             ),
#             "content": types.Schema(
#                 type= types.Type.STRING,
#                 description= "The content to write in the defined by file_path."
#             )
#         }
#     )
# )


def run_python_file(working_directory, file_path, args=[]):
    try:
        path = os.path.join(working_directory, file_path)
        parent_absolute_path = os.path.abspath(working_directory)
        absolute_path = os.path.abspath(path)
        execution_result = ""

        if not (absolute_path.startswith(parent_absolute_path)):
            return f"Error: Cannot execute \"{path}\" as it is outside the permitted working directory "

        if not (os.path.isfile(path)):
            return f"Error: File \"{file_path}\" not found."
        
        if not file_path.endswith(".py"):
            return f"Error: \"{file_path}\" is not a python file."

        cmd = ["python",absolute_path]
        cmd.extend(args)

        result = subprocess.run(cmd, timeout=SUBPROCESS_EXECUTION_TIMEOUT, capture_output = True, cwd= parent_absolute_path, text=True )

        result_stdout= result.stdout
        result_stderr = result.stderr
        execution_result += f"STDOUT:{result_stdout}\nSTDERR:{result_stderr}"

        if result.returncode != 0:
            execution_result += f"Process exited with code {result.returncode}\n"
        if result_stdout == "":
            execution_result += "No output produced"

        return execution_result

    except Exception as e:
        return f"Error: executing Python file: \"{e}\""

        
