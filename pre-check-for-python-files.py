import os
import re

def check_file_name(filename):
    """Check if the file name matches the pattern."""
    return re.match(r'testlab_to_me.*\.py', filename)

def check_file_extension(filename):
    """Check if the file extension is '.py'."""
    return filename.endswith('.py')

def check_for_secrets(file_path):
    """Check if any secrets are hardcoded."""
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line_number, line in enumerate(lines, start=1):
            # Example check for 'password' keyword
            if 'password' in line.lower():
                print(f"Hardcoded value found in file: {file_path}, line {line_number}: {line.strip()}")

def perform_pre_checks(directory):
    """Perform pre-checks on Python files within the specified directory."""
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                if check_file_name(file) and check_file_extension(file):
                    print(f"Valid file: {file_path}")
                    check_for_secrets(file_path)
                else:
                    print(f"Invalid file: {file_path}")

# Usage
directory = 'datamigration/glue/scripts'
perform_pre_checks(directory)
