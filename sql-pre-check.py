import os
import yaml

def validate_yaml_file(file_path):
    with open(file_path, 'r') as yaml_file:
        try:
            data = yaml.safe_load(yaml_file)
            sql_commands = [item['sql'] for item in data]

            # Check if the required SQL commands are present and in the correct sequence
            expected_commands = ['delete', 'commit', 'insert', 'commit']
            if sql_commands == expected_commands:
                print(f"Valid YAML file: {file_path}")
            else:
                print(f"Invalid sequence of SQL commands in YAML file: {file_path}")
        except yaml.YAMLError as e:
            print(f"Error parsing YAML file {file_path}: {e}")

def validate_sql_file(file_path):
    with open(file_path, 'r') as sql_file:
        # Check if the file contains SQL commands
        if any(line.strip().startswith(('insert', 'delete', 'commit')) for line in sql_file):
            print(f"Valid SQL file: {file_path}")
        else:
            print(f"No SQL commands found in file: {file_path}")

def validate_folder(folder_path):
    valid_files = []
    files = os.listdir(folder_path)
    
    # Check if there are any files in the directory
    has_files = any(os.path.isfile(os.path.join(folder_path, f)) for f in files)
    if not has_files:
        return valid_files

    for file_name in files:
        file_path = os.path.join(folder_path, file_name)
        if folder_path.endswith('stg/labtest') or folder_path.endswith('trn/labtest'):
            if file_name.endswith('.yaml'):
                validate_yaml_file(file_path)
            elif file_name.startswith('insert_script'):
                valid_files.append((file_name, folder_path))
            else:
                print(f"Incorrect naming convention in {folder_path}: {file_name}")
        elif folder_path.endswith('ext'):
            if file_name.endswith('.yaml'):
                validate_sql_file(file_path)
            elif file_name.startswith('ext_script'):
                valid_files.append((file_name, folder_path))
            else:
                print(f"Incorrect naming convention in {folder_path}: {file_name}")

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
