import os
from google.genai import types
from config import MAX_CHARS


def get_file_content(working_directory, directory):
    try:
        abs_path = os.path.realpath(working_directory)
        target_path = os.path.realpath(os.path.join(abs_path, directory))

        # Ensure the requested file is inside the permitted working directory
        if os.path.commonpath([abs_path, target_path]) != abs_path:
            return f'Error: Cannot read "{directory}" as it is outside the permitted working directory'

        if not os.path.isfile(target_path):
            return f"Error: File not found or is not a regular file: {target_path}"

        with open(target_path, "r", encoding="utf-8") as file:
            content = file.read(MAX_CHARS)
            # If there is more content after reading MAX_CHARS, indicate truncation
            if file.read(1):
                content += (
                    f'[...File "{target_path}" truncated at {MAX_CHARS} characters]'
                )

        return content
    except Exception as e:
        return f"Error: {str(e)}"


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Retrieves the content of a specified file relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="File path to read content from, relative to the working directory",
            ),
        },
        required=["directory"],
    ),
)
