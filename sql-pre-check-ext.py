import os
import re

def validate_yaml_file(file_path):
    # Check if file name starts with 'ext_script' and has extension .yml or .yaml
    if re.match(r'^ext_script.*\.(yml|yaml)$', os.path.basename(file_path)):
        # Check if the file contains at least one SQL command with $raw_schema
        with open(file_path, 'r') as file:
            content = file.read()
            if re.search(r'\b(SELECT|INSERT|UPDATE|DELETE)\b.*\$raw_schema', content, re.IGNORECASE):
                return True
    return False

def main():
    directory = 'datamigration/sql/ext'  # Path to the directory
    for file_name in os.listdir(directory):
        file_path = os.path.join(directory, file_name)
        if os.path.isfile(file_path):
            is_valid = validate_yaml_file(file_path)
            if is_valid:
                print(f"File: {file_name} | Path: {file_path} | Valid SQL Command with $raw_schema: Yes")
            else:
                print(f"File: {file_name} | Path: {file_path} | Valid SQL Command with $raw_schema: No")

if __name__ == "__main__":
    main()
