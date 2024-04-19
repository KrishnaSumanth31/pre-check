import os
import re

def has_sql_command(content):
    # Check if the content contains any SQL command
    sql_commands = re.findall(r'\b(SELECT|INSERT|UPDATE|DELETE)\b', content, re.IGNORECASE)
    return bool(sql_commands)

def has_trn_schema(content):
    # Check if the content contains the $trn_schema key
    return bool(re.search(r'\$trn_schema', content))

def validate_yaml_file(file_path):
    # Check if file name starts with 'ext_script' and has extension .yml or .yaml
    if re.match(r'^ext_script.*\.(yml|yaml)$', os.path.basename(file_path)):
        # Check if the file contains at least one SQL command and $trn_schema
        with open(file_path, 'r') as file:
            content = file.read()
            return has_sql_command(content), has_trn_schema(content)
    return False, False

def main():
    directory = 'datamigration/sql/ext'  # Path to the directory
    for file_name in os.listdir(directory):
        file_path = os.path.join(directory, file_name)
        if os.path.isfile(file_path):
            has_sql, has_trn = validate_yaml_file(file_path)
            sql_command_msg = "SQL Command: Yes" if has_sql else "SQL Command: No"
            trn_schema_msg = "$trn_schema: Yes" if has_trn else "$trn_schema: No"
            print(f"File: {file_name} | Path: {file_path} | {sql_command_msg} | {trn_schema_msg}")

if __name__ == "__main__":
    main()
