import os
import glob
import yaml
import re

def check_yaml_files(folder_paths):
    for folder_path in folder_paths:
        # Find YAML files matching the criteria
        yaml_files = glob.glob(os.path.join(folder_path, "insert_script*.yaml")) + glob.glob(os.path.join(folder_path, "insert_script*.yml"))
        for file_path in yaml_files:
            # Check if file name starts with "insert_script" and extension is ".yaml" or ".yml"
            if os.path.basename(file_path).startswith("insert_script") and file_path.lower().endswith(('.yaml', '.yml')):
                print(f"INFO: Valid file: {file_path}")
                try:
                    with open(file_path, 'r') as yaml_file:
                        yaml_data = yaml.safe_load(yaml_file)
                        if isinstance(yaml_data, dict):
                            executes = yaml_data.get('executes', [])
                            if isinstance(executes, list):
                                check_sequence_and_schema(executes, file_path)
                            else:
                                print(f"ERROR: Invalid YAML format in file: {file_path}")
                        else:
                            print(f"ERROR: Invalid YAML format in file: {file_path}")
                except Exception as e:
                    print(f"ERROR: Error processing YAML file {file_path}: {e}")
            else:
                print(f"INFO: Ignored file: {file_path}. File name does not start with 'insert_script' or has invalid extension.")

def check_sequence_and_schema(executes, file_path):
    expected_sequence = ['delete', 'commit', 'insert', 'commit']
    
    # Extracting SQL commands
    actual_sql_commands = [item.get('sql', '').lower() for item in executes if 'sql' in item]
    
    # Check if all expected keywords appear in the SQL commands
    is_correct_sequence = all(keyword in ' '.join(actual_sql_commands) for keyword in expected_sequence)
    
    # Check for $*_schema pattern in delete and insert SQL commands
    delete_contains_schema_pattern = any(re.search(r'\$\w+_schema', command) for command in actual_sql_commands if 'delete' in command)
    insert_contains_schema_pattern = any(re.search(r'\$\w+_schema', command) for command in actual_sql_commands if 'insert' in command)
    
    # Print the results for sequence correctness and schema pattern presence
    if is_correct_sequence:
        print(f"INFO: Sequence is correct in file: {file_path}")
    else:
        print(f"ERROR: Sequence is incorrect in file: {file_path}")
    
    if delete_contains_schema_pattern and insert_contains_schema_pattern:
        print(f"INFO: $*_schema pattern is present in both delete and insert commands in file: {file_path}")
    else:
        if not delete_contains_schema_pattern:
            print(f"ERROR: $*_schema pattern is missing in delete command in file: {file_path}")
        if not insert_contains_schema_pattern:
            print(f"ERROR: $*_schema pattern is missing in insert command in file: {file_path}")

# Specify the paths of the folders you want to check
folders_to_check = ["datamigration/sql/stg/labtest", "datamigration/sql/trn/labtest"]
check_yaml_files(folders_to_check)
