import os

def validate_folder(folder_path):
    valid_files = []
    files = os.listdir(folder_path)
    for file_name in files:
        if not file_name.endswith('.yaml'):
            continue
        
        if folder_path.endswith('stg') or folder_path.endswith('trn'):
            if file_name.startswith('insert_script'):
                valid_files.append((file_name, os.path.join(folder_path, file_name)))
        elif folder_path.endswith('ext'):
            if file_name.startswith('ext_script'):
                valid_files.append((file_name, os.path.join(folder_path, file_name)))

    return valid_files

def validate_folder_structure(root_path):
    for root, dirs, files in os.walk(root_path):
        for folder in dirs:
            folder_path = os.path.join(root, folder)
            valid_files = validate_folder(folder_path)
            for file_name, file_path in valid_files:
                print(f"Valid file: {file_name} | Path: {file_path}")

# Example usage:
root_path = "artifacts-dev/sql"
validate_folder_structure(root_path)
