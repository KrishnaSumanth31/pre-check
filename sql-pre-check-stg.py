import os
import glob
import yaml

# Define the base directory
base_dir = "datamigration/sql"

# Define the expected structure and sequence
expected_structure = [
    {'sql': 'delete*;'},
    {'sql': 'commit;'},
    {'sql': 'insert*;'},
    {'sql': 'commit;'}
]

# Function to validate YAML files
def validate_yaml(file_path):
    with open(file_path, 'r') as f:
        try:
            content = yaml.safe_load(f)
            if content == expected_structure:
                return True
            else:
                return False
        except yaml.YAMLError as e:
            print(f"Error parsing YAML in {file_path}: {e}")
            return False

# Check file contents
print("\nChecking file contents...")
for root, dirs, files in os.walk(base_dir):
    for file in files:
        if file.endswith(".yml") or file.endswith(".yaml"):
            file_path = os.path.join(root, file)
            print(f"File: {file_path}")
            if validate_yaml(file_path):
                print("Sequence matches: delete, commit, insert, commit")
            else:
                print("Sequence doesn't match: delete, commit, insert, commit")
