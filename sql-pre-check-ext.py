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
            has_sql = has_sql_command(content)
            has_trn = has_trn_schema(content)
            if has_sql and has_trn:
                return True, "INFO: Valid pre-check"
            else:
                errors = []
                if not has_sql:
                    errors.append("SQL command missing")
                if not has_trn:
                    errors.append("$trn_schema missing")
                return False, "ERROR: " + ', '.join(errors)
    return False, "ERROR: File name or extension invalid"

def main():
    directory = 'datamigration/sql/ext'  # Path to the directory
    all_valid = True
    for file_name in os.listdir(directory):
        file_path = os.path.join(directory, file_name)
        if os.path.isfile(file_path):
            valid, message = validate_yaml_file(file_path)
            print(f"File: {file_name} | Path: {file_path} | {message}")
            if not valid:
                all_valid = False
    if all_valid:
        print("INFO: All files passed pre-check.")
    else:
        print("ERROR: Some files failed pre-check.")

if __name__ == "__main__":
    main()
