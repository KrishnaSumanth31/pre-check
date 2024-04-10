import os
import yaml

def check_sequence(file_path):
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)
        operations = [entry['operation'] for entry in data]
        expected_sequence = ['delete', 'commit', 'insert', 'commit']
        if operations != expected_sequence:
            print(f"Sequence in file {file_path} is incorrect.")
            return False
    print(f"Sequence in file {file_path} is correct.")
    return True

def check_directory(directory):
    files = [file for file in os.listdir(directory) if file.endswith('.yaml')]
    if not files:
        print(f"No .yml files found in {directory}")
        return False
    else:
        print(f"Found .yml files in {directory}: {files}")
        for file in files:
            file_path = os.path.join(directory, file)
            if not check_sequence(file_path):
                # If any file fails sequence check, return False
                return False
        return True

# Directory paths
stg_labtest_dir = "sql/stg/labtest"
trn_labtest_dir = "sql/trn/labtest"

# Perform checks
print("Checking sequence for sql/stg/labtest:")
if check_directory(stg_labtest_dir):
    print("All files in sql/stg/labtest have correct sequence.")
else:
    print("Some files in sql/stg/labtest have incorrect sequence.")

print("\nChecking sequence for sql/trn/labtest:")
if check_directory(trn_labtest_dir):
    print("All files in sql/trn/labtest have correct sequence.")
else:
    print("Some files in sql/trn/labtest have incorrect sequence.")
