import os
import glob
import yaml

def check_yaml_files(folder_paths):
    for folder_path in folder_paths:
        for file_path in glob.glob(os.path.join(folder_path, "insert_script*.yaml")) + glob.glob(os.path.join(folder_path, "insert_script*.yml")):
            try:
                with open(file_path, 'r') as yaml_file:
                    yaml_data = yaml.safe_load(yaml_file)
                    if isinstance(yaml_data, list):
                        check_sequence(yaml_data, file_path)
                    else:
                        print(f"Invalid YAML format in file: {file_path}")
            except yaml.YAMLError as e:
                print(f"Error reading YAML file {file_path}: {e}")

def check_sequence(yaml_data, file_path):
    sql_commands = [item.get('sql', '').strip().lower() for item in yaml_data if 'sql' in item]
    expected_sequence = ['delete', 'commit', 'insert', 'commit']
    if sql_commands == expected_sequence:
        print(f"Sequence is correct in file: {file_path}")
    else:
        print(f"Sequence is incorrect in file: {file_path}")

# Specify the paths of the folders you want to check
folders_to_check = ["datamigration/sql/stg/labtest", "datamigration/sql/trn/labtest"]
check_yaml_files(folders_to_check)
