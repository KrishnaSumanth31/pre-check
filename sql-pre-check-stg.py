import os
import glob
from ruamel.yaml import YAML
from ruamel.yaml.constructor import SafeConstructor

# Define the base directory
base_dir = "datamigration/sql"

# Function to validate YAML files
def validate_yaml(file_path):
    with open(file_path, 'r') as f:
        try:
            yaml = YAML()
            yaml.Constructor = SafeConstructor
            content = yaml.load(f)
            if content and isinstance(content, list):
                sql_statements = [item.get('sql', '').strip() for item in content]
                expected_sequence = [
                    "delete from $mydata_schema.tablename;",
                    "commit;",
                    "insert into $mydata_schema.mytable;",
                    "commit;"
                ]
                if sql_statements == expected_sequence:
                    return True, None
                else:
                    return False, sql_statements
            else:
                return False, None
        except Exception as e:
            print(f"Error parsing YAML in {file_path}: {e}")
            return False, None

# Check file contents
print("\nChecking file contents...")
for root, dirs, files in os.walk(base_dir):
    if root.endswith("sql/ext"):
        continue  # Skip files under the sql/ext directory
    for file in files:
        if file.endswith(".yml") or file.endswith(".yaml"):
            file_path = os.path.join(root, file)
            print(f"File: {file_path}")
            result, actual_sequence = validate_yaml(file_path)
            if result:
                print("Sequence matches: delete, commit, insert, commit")
            else:
                if actual_sequence is None:
                    print("Error: No valid YAML content found")
                else:
                    print(f"Sequence doesn't match: Expected delete, commit, insert, commit, but found {actual_sequence}")
