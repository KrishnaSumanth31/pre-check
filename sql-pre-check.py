import os

def validate_folder(folder_path):
    valid_files = []
    files = os.listdir(folder_path)
    for file_name in files:
        if file_name.endswith('.yaml'):
            if folder_path.endswith('stg') or folder_path.endswith('trn'):
                if file_name.startswith('insert_script'):
                    valid_files.append(os.path.join(folder_path, file_name))
            elif folder_path.endswith('ext'):
                if file_name.startswith('ext_script'):
                    valid_files.append(os.path.join(folder_path, file_name))
    return valid_files

def validate_folder_structure(root_path):
    valid_files = []
    for root, dirs, files in os.walk(root_path):
        for folder in dirs:
            folder_path = os.path.join(root, folder)
            valid_files.extend(validate_folder(folder_path))
    return valid_files

# Example usage:
root_path = "datamigration/sql"
valid_files = validate_folder_structure(root_path)
for file_path in valid_files:
    print("Valid file path:", file_path)
