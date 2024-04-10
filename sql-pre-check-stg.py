import os
import glob
import yaml

def check_yaml_files(folder_paths):
    for folder_path in folder_paths:
        yaml_files = glob.glob(os.path.join(folder_path, "insert_script*.yaml")) + glob.glob(os.path.join(folder_path, "insert_script*.yml"))
        for file_path in yaml_files:
            try:
                with open(file_path, 'r') as yaml_file:
                    yaml_data = yaml.safe_load(yaml_file)
                    if isinstance(yaml_data, dict):
                        executes = yaml_data.get('executes', [])
                        if isinstance(executes, list):
                            check_sequence(executes, file_path)
                        else:
                            print(f"Invalid YAML format in file: {file_path}")
                    else:
                        print(f"Invalid YAML format in file: {file_path}")
            except Exception as e:
                print(f"Error processing YAML file {file_path}: {e}")

def check_sequence(executes, file_path):
    expected_sequence = ['delete', 'commit', 'insert', 'commit']
    actual_sequence = [item.get('sql', '').strip().lower() for item in executes]
    
    print(f"Expected Sequence: {expected_sequence}")
    print(f"Actual Sequence: {actual_sequence}")
    
    if actual_sequence == expected_sequence:
        print(f"Sequence is correct in file: {file_path}")
    else:
        print(f"Sequence is incorrect in file: {file_path}")


# Specify the paths of the folders you want to check
folders_to_check = ["datamigration/sql/stg/labtest", "datamigration/sql/trn/labtest"]
check_yaml_files(folders_to_check)
