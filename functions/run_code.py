import os
import subprocess
from config import SUBPROCESS_EXECUTION_TIMEOUT

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

        
