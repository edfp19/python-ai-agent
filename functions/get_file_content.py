import os
from config import *

def get_file_content(working_directory, directory):
    try: 
        abs_path = os.path.abspath(working_directory)
        target_directory = os.path.normpath(os.path.join(abs_path, directory))
        #   check if target_directory is within absolute path 
        valid_target = os.path.commonpath([abs_path, target_directory]) == abs_path
        if not valid_target:
            raise ValueError(f'Error: Cannot read "{directory}" as it is outside the permitted working directory')
        if not os.path.isfile(target_directory):
            raise ValueError(f'Error: File not found or is not a regular file: {target_directory}')
        with open(target_directory, 'r') as file:
            content = file.read(MAX_CHARS)  # Read first MAX_CHARS characters
            if file.read(1):
                content += f'[...File "{target_directory}" truncated at {MAX_CHARS} characters]'
            print(content)
    except Exception as e:
        print(f'Error: {str(e)}')