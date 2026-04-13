import os
from google.genai import types


def get_files_info(working_directory, directory="."):
    try:
        abs_path = os.path.realpath(working_directory)
        target_directory = os.path.realpath(os.path.join(abs_path, directory))

        # Ensure the target is inside the permitted working directory
        if os.path.commonpath([abs_path, target_directory]) != abs_path:
            return f"Error: Cannot list '{directory}' as it is outside the permitted working directory"

        if not os.path.isdir(target_directory):
            return f'Error: "{directory}" is not a directory'

        lines = []
        for fname in os.listdir(target_directory):
            p = os.path.join(target_directory, fname)
            try:
                size = os.path.getsize(p)
            except OSError:
                size = 0
            lines.append(
                f"- {fname}: File Size: {size} bytes, is_dir={os.path.isdir(p)}"
            )
        return "\n".join(lines)
    except Exception as e:
        return f"Error: {str(e)}"


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
        required=["directory"],
    ),
)
