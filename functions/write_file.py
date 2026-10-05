import os

def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        abs_working_path: str = os.path.abspath(working_directory)
        target_dir: str = os.path.normpath(os.path.join(abs_working_path, file_path))
        valid_path: bool = os.path.commonpath([abs_working_path, target_dir]) == abs_working_path
        if not valid_path:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if os.path.isdir(target_dir):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        os.makedirs(os.path.dirname(target_dir), exist_ok=True)
        with open(target_dir, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {e}"


scheme_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Write the new content in the file, in a specified directory relative to the working directory, providing result of the function",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the file, relative to the working directory",
                },
                "content": {
                    "type": "string",
                    "description": "Content to write in the file, in string format",
                },
            },
            "required": ["file_path", "content"]
        },
    },
}
