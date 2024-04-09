import os

def validate_folder(folder_path):
    valid_files = []
    files = os.listdir(folder_path)
    
    # Check if there are any files in the directory
    has_files = any(os.path.isfile(os.path.join(folder_path, f)) for f in files)
    if not has_files:
        return valid_files

    for file_name in files:
        if not file_name.endswith('.yaml'):
            print(f"Incorrect file extension in {folder_path}: {file_name}")
            continue
        
        if folder_path.endswith('stg/labtest') or folder_path.endswith('trn/labtest'):
            if not file_name.startswith('insert_script'):
                print(f"Incorrect naming convention in {folder_path}: {file_name}")
            else:
                valid_files.append((file_name, folder_path))
        elif folder_path.endswith('ext'):
            if not file_name.startswith('ext_script'):
                print(f"Incorrect naming convention in {folder_path}: {file_name}")
            else:
                valid_files.append((file_name, folder_path))

    return valid_files

def validate_folder_structure(root_path):
    for root, dirs, files in os.walk(root_path):
        for folder in dirs:
            folder_path = os.path.join(root, folder)
            valid_files = validate_folder(folder_path)
            for file_info in valid_files:
                file_name, folder_path = file_info
                file_path = os.path.join(folder_path, file_name)
                print(f"Valid file: {file_name} | Path: {file_path}")

# Example usage:
root_path = "datamigration/sql"
validate_folder_structure(root_path)
