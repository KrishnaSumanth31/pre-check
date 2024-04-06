import os
import sys

def check_files(directory, prefix):
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if file.endswith('.py') or file.endswith('.yml'):
                # Check file naming convention here if needed
                if not file_is_valid(file, prefix):
                    print(f"File {file} in {root} does not meet naming convention.")
            else:
                print(f"File {file} in {root} has incorrect extension.")

def file_is_valid(file_name, prefix):
    # Add your file naming convention rules here
    # Example: Check if the file name starts with a specific prefix
    if file_name.startswith(prefix):
        return True
    else:
        return False

if __name__ == "__main__":
    directory = sys.argv[1]
    prefix = sys.argv[2]
    check_files(directory, prefix)
