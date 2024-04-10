import os
import yaml

def check_file(filename):
    with open(filename, 'r') as file:
        data = yaml.safe_load(file)
        expected_keys = ['delete', 'commit', 'insert', 'commit']
        actual_keys = list(data[0].keys()) if isinstance(data, list) and len(data) > 0 else []
        if actual_keys == expected_keys:
            return True
        else:
            return False

def perform_checks(directory):
    for root, dirs, files in os.walk(directory):
        # Skip the 'sql/ext' folder
        if root.endswith('ext'):
            continue
        # Perform checks for files in 'sql/stg' and 'sql/trn' folders
        for file in files:
            if file.startswith('insert_script') and file.endswith('.yaml'):
                filepath = os.path.join(root, file)
                passed = check_file(filepath)
                if passed:
                    print(f"File: {filepath}, Status: Passed pre-checks.")
                else:
                    print(f"File: {filepath}, Status: Failed pre-checks.")

# Specify the directory to perform the checks
directory = 'datamigration/sql'
perform_checks(directory)
