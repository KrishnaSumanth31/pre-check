import os
import yaml

def check_sequence(file_path):
    try:
        with open(file_path, 'r') as file:
            data = yaml.safe_load(file)
            keys = [entry for entry in data]
            expected_keys = ['delete', 'commit', 'insert', 'commit']
            if keys != expected_keys:
                print(f"Sequence in file {file_path} is incorrect.")
                return False
        print(f"Sequence in file {file_path} is correct.")
        return True
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
