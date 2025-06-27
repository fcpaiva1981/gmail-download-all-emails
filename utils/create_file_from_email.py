

def create_file(content, file_path ,file_name):
    try:
        path = file_path+file_name
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"File '{file_name}' created and written to successfully.")
    except IOError as e:
        print(f"Error creating file: {e}")
