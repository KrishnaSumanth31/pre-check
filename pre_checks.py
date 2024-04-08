import os

def validate_file_name(filename):
    # Check if the filename starts with "data_extract" and has a YAML extension
    return filename.startswith("data_extract") and filename.endswith(".yml")

def pre_checks(folder_path):
    try:
        # Check if the folder exists
        if not os.path.exists(folder_path):
            raise FileNotFoundError(f"The folder '{folder_path}' does not exist.")
        
        # Get all files in the folder
        files = os.listdir(folder_path)
        
        # Perform pre-checks for each file
        for file in files:
            file_path = os.path.join(folder_path, file)
            if os.path.isfile(file_path):
                if validate_file_name(file):
                    print(f"Valid filename: {file} - Valid file path: {file_path}")
                else:
                    print(f"Invalid filename: {file}")
    
    except Exception as e:
        print(f"An error occurred: {e}")

# Path to the raw folder
raw_folder_path = "datamigration/configurations/raw"

# Perform pre-checks on files in the raw folder
pre_checks(raw_folder_path)
