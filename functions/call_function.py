from .get_files_info import get_files_info, schema_get_files_info
from .get_file_content import get_file_content, schema_get_file_content
from .run_python_file import run_python_file, schema_run_python_file
from .write_file import write_file, schema_write_file
from google.genai import types

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ],
)

function_map = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "run_python_file": run_python_file,
    "write_file": write_file,
}


def call_function(function_call, verbose=False):
    function_name = function_call.name or ""
    if function_name not in function_map:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )
    if verbose:
        # Only print call details when verbose mode is enabled
        print(f" - Calling function: {function_name}({function_call.args})")

    args = dict(function_call.args) if function_call.args else {}

    # Only set a default working directory when one is not provided by the caller.
    # This avoids forcing all operations into a single hard-coded directory while
    # remaining backwards compatible with existing usage.
    if "working_directory" not in args:
        args["working_directory"] = "./calculator"

    function_result = function_map[function_name](**args)

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )
