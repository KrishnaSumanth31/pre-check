import os
import yaml

def check_sequence(file_path):
    try:
        with open(file_path, 'r') as file:
            data = yaml.safe_load(file)
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
                                return True
                            else:
                                print("Invalid sequence of SQL commands.")
                                return False
                    else:
                        print(f"No SQL commands found in {file_path}")
                        return False
                else:
                    print(f"Invalid 'executes' format in {file_path}")
                    return False
            else:
                print(f"Invalid YAML format in {file_path}")
                return False
    except Exception as e:
        print(f"Error occurred while processing file {file_path}: {e}")
        return False

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
