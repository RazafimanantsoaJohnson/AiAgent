import os

def get_files_info(working_directory, directory="."):
    # instead of throwing errors we want to return error strings
    try:
        path = os.path.join(working_directory, directory)
        parentAbsolutePath = os.path.abspath(working_directory)
        absolutePath = os.path.abspath(path)
        result = ""

        if not (absolutePath.startswith(parentAbsolutePath)):
            return (f"Error: Cannot list \"{directory}\" as it is outside the permitted working directory ")

        if not os.path.isdir(path):
            return f"Error: \"{path}\" is not a directory"
        
        for foundPath in os.listdir(path):
            fileAbsPath = os.path.join(path, foundPath)
            isDir = os.path.isdir(fileAbsPath)
            result += f"- {foundPath}: file_size={os.path.getsize(fileAbsPath)} bytes, is_dir={isDir}\n"
        
        return result
    except Exception as e:
        return f"Error: {e}"

