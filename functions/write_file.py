import os 

def write_file(working_directory, directory, content):
    try: 
        abs_path = os.path.abspath(working_directory)
        target_directory = os.path.normpath(os.path.join(abs_path, directory))
        #   check if target_directory is within absolute path 
        valid_target = os.path.commonpath([abs_path, target_directory]) == abs_path
        if not valid_target:
            raise ValueError(f'Error: Cannot write to "{directory}" as it is outside the permitted working directory')
        if os.path.isdir(target_directory):
            raise ValueError(f'Error: Target path is a directory, not a file: {target_directory}')
        #   ensure the directory exists
        os.makedirs(os.path.dirname(target_directory), exist_ok=True)
        with open(target_directory, 'w') as file:
            file.write(content)
        print(f'Success: Content written to "{target_directory}"')
    except Exception as e:
        print(f'Error: {str(e)}')