import os
import glob
import yaml

# Define the folder path
folder_path = "pre-check/datamigration/configurations/raw"

# Function to perform pre-checks
def perform_prechecks():
    # Check if every file starts with 'data_extract_' and has a YAML extension
    files = glob.glob(os.path.join(folder_path, "data_extract_*.yml"))
    for file_path in files:
        file_name = os.path.basename(file_path)
        if not file_name.startswith("data_extract_"):
            print(f"Warning: File '{file_name}' does not follow naming convention (should start with 'data_extract_').")
        if not file_name.endswith(".yml"):
            print(f"Warning: File '{file_name}' does not have a YAML extension.")

    # Load the YAML file
    yaml_file = os.path.join(folder_path, "data_extract*.yml")
    with open(yaml_file, "r") as f:
        data = yaml.safe_load(f)

    # Check if the details section is properly formatted
    if "details" in data:
        for task in data["details"]["task"]:
            if "postgre_schema" not in task or "postgre_table_name" not in task:
                print("Error: 'postgre_schema' or 'postgre_table_name' is missing in details.")
            if "log_bucket" not in task:
                print("Warning: 'log_bucket' is missing in details.")
            if "log_bucker" in task:  # Typo in the YAML file ("log_bucker" instead of "log_bucket")
                print("Warning: Typo in key name ('log_bucker' instead of 'log_bucket').")
    else:
        print("Error: 'details' section is missing in YAML file.")

# Perform pre-checks
perform_prechecks()
