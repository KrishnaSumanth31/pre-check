import os
import yaml

def check_yaml_files(folder_paths):
    for folder_path in folder_paths:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file.startswith("insert_script") and (file.endswith(".yml") or file.endswith(".yaml")):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r') as yaml_file:
                        try:
                            yaml_data = yaml.safe_load(yaml_file)
                            if isinstance(yaml_data, list):
                                check_sequence(yaml_data, file_path)
                            else:
                                print(f"Invalid YAML format in file: {file_path}")
                        except yaml.YAMLError as e:
                            print(f"Error reading YAML file {file_path}: {e}")

def check_sequence(data, file_path):
    expected_sequence = ['delete', 'commit', 'insert', 'commit']
    actual_sequence = [item.get('sql').strip() for item in data if 'sql' in item]
    if actual_sequence == expected_sequence:
        print(f"Sequence is correct in file: {file_path}")
    else:
        print(f"Sequence is incorrect in file: {file_path}")

# Specify the paths of the folders you want to check
folders_to_check = ["datamigration/sql/stg/labtest", "datamigration/sql/trn/labtest"]
check_yaml_files(folders_to_check)
