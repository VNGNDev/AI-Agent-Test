from functions import get_file_content
from functions.get_files_info import scheme_get_files_info, get_files_info
from functions.get_file_content import scheme_get_file_content, get_file_content
from functions.run_python_file import scheme_run_python_file, run_python_file
from functions.write_file import scheme_write_file, write_file
from collections.abc import Callable
import json

available_functions: list = [
    scheme_get_files_info,
    scheme_get_file_content,
    scheme_run_python_file,
    scheme_write_file
]

function_map: dict[str, Callable[..., str]] = {
    "get_file_content": get_file_content,
    "get_files_info": get_files_info,
    "run_python_file": run_python_file,
    "write_file": write_file
}

def call_function(tool_call, verbose: bool = False) -> dict:
    id_call: int = tool_call.id
    name_function: str = tool_call.function.name
    arg_function: dict = json.loads(tool_call.function.arguments or "{}")
    if verbose:
        print(f" . Calling function: {name_function}({arg_function})")
    else:
        print(f" - Calling function: {name_function}")

    if not name_function in function_map:
        return {
            "role": "tool",
            "tool_call_id": id_call,
            "content": f"Error: Unknown function: {name_function}"
        }

    arg_function['working_directory'] = "./calculator"
    result: str = function_map[name_function](**arg_function)
    return {
            "role": "tool",
            "tool_call_id": id_call,
            "content": result,
    }
