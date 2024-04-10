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
    # Implement your logic here, such as scanning for keywords like 'password', 'secret', etc.
    # You might also want to consider using a more robust method like regular expressions or
    # integrating a static code analysis tool.

def perform_pre_checks(directory):
    """Perform pre-checks on Python files within the specified directory."""
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                if not check_file_name(file):
                    print(f"Invalid file name: {file_path}")
                if not check_file_extension(file):
                    print(f"Invalid file extension: {file_path}")
                check_for_secrets(file_path)

# Usage
directory = 'datamigration/glue/scripts'
perform_pre_checks(directory)
