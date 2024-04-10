import os
import yaml

def validate_yaml_file(file_path, folder_path):
    with open(file_path, 'r') as yaml_file:
        try:
            data = yaml.safe_load(yaml_file)
            if isinstance(data, dict):
                executes = data.get('executes', [])
                if isinstance(executes, list):
                    sql_commands = [item['sql'].strip().lower() for item in executes if 'sql' in item]
                    
                    # Check if there's at least one SQL command
                    if sql_commands:
                        print(f"Valid YAML file with SQL query: {file_path}")
                        # Check for valid sequence for stg and trn folders
                        if folder_path.endswith(('stg', 'trn')):
                            expected_sequence = ['delete', 'commit', 'insert', 'commit']
                            if sql_commands == expected_sequence:
                                print("Valid sequence of SQL commands.")
                            else:
                                print("Invalid sequence of SQL commands.")
                    else:
                        print(f"No SQL query found in YAML file: {file_path}")
                else:
                    raise ValueError("Invalid executes format")
            else:
                raise ValueError("Invalid YAML file format")
        except yaml.YAMLError as e:
            print(f"Error parsing YAML file {file_path}: {e}")
            with open(file_path, 'r') as f:
                print(f"Contents of {file_path}:\n{f.read()}")
        except ValueError as e:
            print(f"Error processing YAML file {file_path}: {e}")
            with open(file_path, 'r') as f:
                print(f"Contents of {file_path}:\n{f.read()}")

def validate_sql_file(file_path, folder_path):
    # Check if the folder is 'trn' or 'stg' and validate SQL commands sequence
    expected_sequence = ['delete', 'commit', 'insert', 'commit']
    sequence = []
    with open(file_path, 'r') as sql_file:
        for line in sql_file:
            if line.strip().startswith(('delete', 'commit', 'insert')):
                sequence.append(line.strip().split()[0])  # Extract the first word as the command
    if sequence == expected_sequence:
        print(f"Valid SQL file: {file_path}")
        return True
    else:
        print(f"Invalid SQL commands sequence in file: {file_path}")
        return False

def validate_folder(folder_path):
    valid_files = []
    files = os.listdir(folder_path)
    
    # Check if there are any files in the directory
    has_files = any(os.path.isfile(os.path.join(folder_path, f)) for f in files)
    if not has_files:
        return valid_files

    for file_name in files:
        file_path = os.path.join(folder_path, file_name)
        if folder_path.endswith(('stg', 'trn')):
            if file_name.endswith('.yaml'):
                validate_yaml_file(file_path, folder_path)
            elif file_name.endswith('.sql'):
                validate_sql_file(file_path, folder_path)
            elif file_name.startswith('insert_script'):
                valid_files.append((file_name, folder_path))
            else:
                print(f"Incorrect naming convention in {folder_path}: {file_name}")
        elif folder_path.endswith('ext'):
            if file_name.endswith('.yaml'):
                validate_yaml_file(file_path, folder_path)
                # Check if the YAML file contains at least one SQL command
                validate_sql = validate_sql_file(file_path, folder_path)
                if not validate_sql:
                    print(f"No SQL query found in YAML file: {file_path}")
            elif file_name.endswith('.sql'):
                validate_sql_file(file_path, folder_path)
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
