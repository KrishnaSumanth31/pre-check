import os
import yaml

def check_yaml_files(folder_paths):
    for folder_path in folder_paths:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file.startswith("insert_script") and (file.endswith(".yml") or file.endswith(".yaml")):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r') as yaml_file:
                        yaml_content = yaml_file.read()
                        print(f"Contents of YAML file {file_path}:\n{yaml_content}")  # Print YAML content
                        try:
                            yaml_data = yaml.safe_load(yaml_content)
                            if isinstance(yaml_data, list):
                                check_sequence(yaml_data, file_path, folder_path)
                            else:
                                print(f"Invalid YAML format in file: {file_path}")
                        except yaml.YAMLError as e:
                            print(f"Error reading YAML file {file_path}: {e}")

def check_sequence(data, file_path, folder_path):
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
                        if folder_path.endswith(('stg/labtest', 'trn/labtest')):
                            expected_sequence = ['delete', 'commit', 'insert', 'commit']
                            if sql_commands == expected_sequence:
                                print(f"Sequence is correct in file: {file_path}")
                            else:
                                print(f"Sequence is incorrect in file: {file_path}")
                        else:
                            print(f"Folder path doesn't end with 'stg/labtest' or 'trn/labtest': {folder_path}")
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

# Specify the paths of the folders you want to check
folders_to_check = ["datamigration/sql/stg/labtest", "datamigration/sql/trn/labtest"]
check_yaml_files(folders_to_check)
