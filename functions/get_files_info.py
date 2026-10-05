import os

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        abs_routh: str = os.path.abspath(working_directory)
        target_dir: str = os.path.normpath(os.path.join(abs_routh, directory))
        valid_target_dir = os.path.commonpath([abs_routh, target_dir]) == abs_routh 
        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        archivos: list = os.listdir(target_dir)
        text: list = []
        for archivo in archivos:
            is_dir: bool = os.path.isdir(os.path.join(target_dir, archivo))
            file_size: int = os.path.getsize(os.path.join(target_dir, archivo))
            info_arch: str = f"- {archivo}: file_size={file_size} bytes, is_dir={is_dir}"
            text.append(info_arch)

        files_info: str = "\n".join(text)
        return files_info
    except Exception as e:
        return f'Error: {e}'

scheme_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}
