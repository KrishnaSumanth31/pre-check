import os

def validate_file_name(filename):
    # Check if the filename starts with "data_extract" and has a YAML extension
    return filename.startswith("data_extract") and filename.endswith(".yml")

def pre_checks(folder_path):
    # Get all files in the folder
    files = os.listdir(folder_path)
    
    # Perform pre-checks for each file
    for file in files:
        if os.path.isfile(os.path.join(folder_path, file)):
            if not validate_file_name(file):
                print(f"Invalid filename: {file}")
            else:
                print(f"Valid filename: {file}")

# Path to the raw folder
raw_folder_path = "pre-check/datamigration/configurations/raw"

# Perform pre-checks on files in the raw folder
pre_checks(raw_folder_path)
