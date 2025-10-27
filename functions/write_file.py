import os

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