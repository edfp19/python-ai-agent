import os
from google.genai import types


def write_file(working_directory, directory, content):
    try:
        abs_path = os.path.realpath(working_directory)
        target_path = os.path.realpath(os.path.join(abs_path, directory))

        # check that the target is inside the permitted working directory
        if os.path.commonpath([abs_path, target_path]) != abs_path:
            return f'Error: Cannot write to "{directory}" as it is outside the permitted working directory'

        if os.path.isdir(target_path):
            return f"Error: Target path is a directory, not a file: {target_path}"

        # ensure the containing directory exists
        parent_dir = os.path.dirname(target_path)
        if parent_dir:
            os.makedirs(parent_dir, exist_ok=True)

        # write file using a deterministic encoding
        with open(target_path, "w", encoding="utf-8") as file:
            file.write(content)

        return (
            f'Successfully wrote to "{target_path}" ({len(content)} characters written)'
        )
    except Exception as e:
        return f"Error: {str(e)}"


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a specified file relative to the working directory, creating directories as needed",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="File path to write content to, relative to the working directory",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to write to the file",
            ),
        },
        required=["directory", "content"],
    ),
)
