import os

def create_directory(directory_name):
    try:
        os.makedirs(directory_name, exist_ok=True)
        print(f"Created directory '{directory_name}'  created successfully or already exists.")
        return directory_name
    except OSError as e:
        print(f"Error creating directory '{directory_name}': {e}")
        return None

def get_path_os_separator():
    return os.sep

def get_path_os(path):
    str_tmp = path.split(";")
    return get_path_os_separator().join(str_tmp)