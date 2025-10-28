import os
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write content into a specific file; it will create the file if it doesn't exist. Will mostly be used to write python code to modify codebase in our case.",
    parameters = types.Schema(
        type= types.Type.OBJECT,
        properties= {
            "file_path": types.Schema(
                type= types.Type.STRING,
                description= "Required parameter to specify the file to write into; can be a non-existent file.",
            ),
            "content": types.Schema(
                type= types.Type.STRING,
                description= "The content to write in the defined by file_path."
            )
        }
    )
)

def write_file(working_directory, file_path, content):
    try:
        path = os.path.join(working_directory, file_path)
        target_dir = os.path.dirname(path)
        parent_absolute_path = os.path.abspath(working_directory)
        absolute_path = os.path.abspath(path)
        result = ""

        if not (absolute_path.startswith(parent_absolute_path)):
            return (f"Error: Cannot write \"{path}\" as it is outside the permitted working directory ")

        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

        with open(path, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        
    except Exception as e:
        return f"Error: {e}"