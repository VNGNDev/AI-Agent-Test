import os
import subprocess

def run_python_file(working_directory: str, file_path: str, args: list[str] | None = None) -> str:
    try:
        abs_working_directory: str = os.path.abspath(working_directory)
        target_path: str = os.path.normpath(os.path.join(abs_working_directory, file_path))
        valid_path: bool = os.path.commonpath([abs_working_directory, target_path]) == abs_working_directory
        if not valid_path:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        command: list[str] = ["python", target_path]
        if args is not None and len(args) > 0:
            command.extend(args)

        output_result = subprocess.run(command, capture_output=True, text=True, timeout=30.0)
        output_string: str = ""
        if output_result.returncode != 0:
            output_string += f"Process exited with code {output_result.returncode}\n"
        
        if not output_result.stdout and not output_result.stderr:
            output_string += "No output produced\n"
        else:
            output_string += f"STDOUT: {output_result.stdout}\n"
            output_string += f"STDERR: {output_result.stderr}\n"

        return output_string
    except Exception as e:
        return f'Error: executing Python file: {e}'



scheme_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Run the python file, in a specified path relative to the working directory, providing the result of the execution",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path of the file, relative to the working directory",
                },
                "args": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Extra arguments for the execution of the python file"
                 }
            },
            "required": ["file_path"],
        },
    },
}
