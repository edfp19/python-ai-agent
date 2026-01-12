import os 

def get_files_info(working_directory, directory="."):
    try: 
        abs_path = os.path.abspath(working_directory)
        target_directory = os.path.normpath(os.path.join(abs_path, directory))
        # check if target_directory is within absolute path 
        valid_target = os.path.commonpath([abs_path, target_directory]) == abs_path
        if not valid_target:
            raise ValueError(f"Error: Cannot list '{directory}' as it is outside the permitted working directory")
        if not target_directory: 
            raise ValueError(f'Error: "{directory}" is not a directory')
        for file in os.listdir(target_directory):
            print(f'- {file}: File Size: {os.path.getsize(os.path.join(target_directory, file))} bytes, is_dir={os.path.isdir(os.path.join(target_directory, file))}')
    except Exception as e:
        print(f'Error: {str(e)}')