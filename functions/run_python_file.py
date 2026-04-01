import os 
import subprocess
from google.genai import types


def run_python_file(working_directory, file_path, args=None):
    try: 
        #  get absolute paths
        abs_path = os.path.abspath(working_directory)
        #  determine target file path
        target_file = os.path.normpath(os.path.join(abs_path, file_path))
        #   check if target_file is within absolute path 
        valid_target = os.path.commonpath([abs_path, target_file]) == abs_path
        if not valid_target:
            return  f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        # check if file exists and is a file
        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        #  ensure it's a .py file
        if not target_file.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file'
        command = ['python', target_file]
        if args: 
            command.extend(args)
        completed_process = subprocess.run(command, cwd=abs_path, capture_output=True, text=True, timeout=30)
        output = ''
        if completed_process.stdout:
            output += completed_process.stdout
        if completed_process.stderr:
            output += completed_process.stderr
        if completed_process.returncode != 0:
            return f"Process exited with code {completed_process.returncode}." + f" STDERR: {completed_process.stderr}"
        elif output.strip() == "":
            return "No output produced"
        else: 
            return (
                    #f"Process exited with code {completed_process.returncode}\n"
                    output
                    # f"STDERR: {completed_process.stderr}\n"
                    # f"STDOUT: {completed_process.stdout}"
                    )
    except Exception as e:
        return f"Error: executing Python file: {e}"

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file with optional arguments",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file to execute, relative to the working directory",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="Optional arguments for the Python file",
                items=types.Schema(type=types.Type.STRING),
            ),
        },
        required=['file_path'],
    ),
)