import os
from config import MAX_CHARS

def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        abs_routh: str = os.path.abspath(working_directory)
        target_dir: str = os.path.normpath(os.path.join(abs_routh, file_path))
        valid_target_dir = os.path.commonpath([abs_routh, target_dir]) == abs_routh 
        if not valid_target_dir:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_dir):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(target_dir, 'r') as f:
            file_content_string = f.read(MAX_CHARS)
            if f.read(1):
                file_content_string += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'

        return file_content_string
    except Exception as e:
        return f'Error: {e}'

scheme_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Read the file in a specified path relative to the working directory, providing content in string format",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the file, relative to the working directory",
                },
            },
        },
        "required": ["file_path"],
    },
}
