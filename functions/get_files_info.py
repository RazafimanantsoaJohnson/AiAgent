import os
from config import FILE_MAX_CHARS
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters = types.Schema(
        type= types.Type.OBJECT,
        properties= {
            "directory": types.Schema(
                type= types.Type.STRING,
                description= "The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself. (Do not send None; use '.' as a zero value instead)",
            )
        }
    )
)

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Read the content of a file at a given path",
    parameters = types.Schema(
        type= types.Type.OBJECT,
        properties= {
            "file_path": types.Schema(
                type= types.Type.STRING,
                description= "The file to read content from, relative to the working directory. The parameter is required",
            )
        }
    )
)


def get_files_info(working_directory, directory="."):
    # instead of throwing errors we want to return error strings
    try:
        path = os.path.join(working_directory, directory)
        parent_absolute_path = os.path.abspath(working_directory)
        absolute_path = os.path.abspath(path)
        result = ""

        if not (absolute_path.startswith(parent_absolute_path)):
            return (f"Error: Cannot list \"{directory}\" as it is outside the permitted working directory ")

        if not os.path.isdir(path):
            return f"Error: \"{path}\" is not a directory"
        
        for found_path in os.listdir(path):
            fileAbsPath = os.path.join(path, found_path)
            isDir = os.path.isdir(fileAbsPath)
            result += f"- {found_path}: file_size={os.path.getsize(fileAbsPath)} bytes, is_dir={isDir}\n"
        
        return result
    except Exception as e:
        return f"Error: {e}"

def get_file_content(working_directory, file_path):

    try:
        path = os.path.join(working_directory,file_path)
        parent_absolute_path = os.path.abspath(working_directory)
        absolute_path = os.path.abspath(path)
        result = ""

        print("- Calling function: get_file_content")

        if not (absolute_path.startswith(parent_absolute_path)):
            return (f"Error: Cannot read \"{directory}\" as it is outside the permitted working directory ")
        if not os.path.isfile(path):
            return f"Error: File not found or is not a regular file: \"{file_path}\""

        with open(absolute_path, "r") as f:
            whole_content = f.read()
            if len(whole_content)> FILE_MAX_CHARS:
                result = whole_content[:FILE_MAX_CHARS]
                result += f"[...File \"{file_path}\" truncated at {FILE_MAX_CHARS} characters ]"
            else:
                result = whole_content
            f.close()

        return result
    except Exception as e:
        return f"Error: {e}"
