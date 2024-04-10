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
                        if folder_path.endswith(('stg/labtest', 'trn/labtest')):
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

def check_directory(directory):
    files = [file for file in os.listdir(directory) if file.endswith('.yaml')]
    if not files:
        print(f"No .yaml files found in {directory}")
        return False
    else:
        print(f"Found .yaml files in {directory}: {files}")
        for file in files:
            file_path = os.path.join(directory, file)
            if not check_sequence(file_path):
                # If any file fails sequence check, return False
                return False
        return True

# Directory paths
stg_labtest_dir = "datamigration/sql/stg/labtest"
trn_labtest_dir = "datamigration/sql/trn/labtest"

# Perform checks
print("Checking sequence for datamigration/sql/stg/labtest:")
if check_directory(stg_labtest_dir):
    print("All files in datamigration/sql/stg/labtest have correct sequence.")
else:
    print("Some files in datamigration/sql/stg/labtest have incorrect sequence.")

print("\nChecking sequence for datamigration/sql/trn/labtest:")
if check_directory(trn_labtest_dir):
    print("All files in datamigration/sql/trn/labtest have correct sequence.")
else:
    print("Some files in datamigration/sql/trn/labtest have incorrect sequence.")
