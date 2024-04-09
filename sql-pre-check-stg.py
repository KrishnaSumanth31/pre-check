import os
import glob
import yaml

# Define the base directory
base_dir = "datamigration/sql"

# Function to validate YAML files
def validate_yaml(file_path):
    with open(file_path, 'r') as f:
        try:
            content = yaml.safe_load(f)
            if content and isinstance(content, list):
                sql_statements = [item.get('sql', '').strip() for item in content]
                expected_sequence = [
                    "delete from $mydata_schema.tablename;",
                    "commit;",
                    "insert into $mydata_schema.mytable;",
                    "commit;"
                ]
                if sql_statements == expected_sequence:
                    return True
                else:
                    return False
            else:
                return False
        except yaml.YAMLError as e:
            print(f"Error parsing YAML in {file_path}: {e}")
            return False

# Check file contents
print("\nChecking file contents...")
for root, dirs, files in os.walk(base_dir):
    if root.endswith("sql/ext"):
        continue  # Skip files under the sql/ext directory
    for file in files:
        if file.endswith(".yml") or file.endswith(".yaml"):
            file_path = os.path.join(root, file)
            print(f"File: {file_path}")
            if validate_yaml(file_path):
                print("Sequence matches: delete, commit, insert, commit")
            else:
                print("Sequence doesn't match: delete, commit, insert, commit")
