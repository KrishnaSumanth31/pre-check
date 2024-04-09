import os
import glob
import yaml

# Define the base directory
base_dir = "datamigration/sql"

# Load the schema
with open("schema.yml", "r") as schema_file:
    schema = yaml.safe_load(schema_file)

# Check file contents
print("\nChecking file contents...")
for root, dirs, files in os.walk(base_dir):
    for file in files:
        if file.endswith(".yml") or file.endswith(".yaml"):
            file_path = os.path.join(root, file)
            print(f"File: {file_path}")
            with open(file_path, 'r') as f:
                try:
                    content = yaml.safe_load(f)
                    if content == schema:
                        print("Sequence matches: delete, commit, insert, commit")
                    else:
                        print("Sequence doesn't match: delete, commit, insert, commit")
                except yaml.YAMLError as e:
                    print(f"Error parsing YAML: {e}")
