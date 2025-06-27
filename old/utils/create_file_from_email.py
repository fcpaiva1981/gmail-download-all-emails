import re
from old.utils.create_directory import get_path_os_separator


def create_file(content, file_path ,file_name):
    try:
        file_name = file_name.replace(' ','_').lower()
        file_name_array = file_name.split('.')
        file_name = re.sub(r'[^a-zA-Z0-9_]', '', file_name_array[0])+"_"+file_name_array[1]+"."+ file_name_array[2]
        path = file_path+get_path_os_separator()+get_path_os_separator() +file_name
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"File '{file_name}' created and written to successfully.")
        return file_name
    except IOError as e:
        print(f"Error creating file: {e}")
        return None
