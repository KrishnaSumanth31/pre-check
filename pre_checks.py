import os
import yaml  # Import the yaml module for parsing YAML files

def validate_file_name(filename):
    # Check if the filename starts with "data_extract" and has a YAML extension
    return filename.startswith("data_extract") and filename.endswith(".yml")

def validate_value(value):
    # Check if the value is not null or empty
    return value is not None and value.strip() != ""

def validate_log_bucket(log_bucket):
    # Check if the log_bucket matches the naming pattern
    return log_bucket.startswith("my_bucket_config")

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
                    # Load YAML file and perform additional checks
                    with open(file_path, 'r') as f:
                        yaml_data = yaml.safe_load(f)
                        # Perform additional checks on yaml_data
                        postgre_secret = yaml_data.get("postgre_secret")
                        oracle_secret = yaml_data.get("oracle_secret")
                        postgre_schema = yaml_data.get("postgre_schema")
                        postgre_table_name = yaml_data.get("postgre_table_name")
                        log_bucket = yaml_data.get("log_bucket")
                        
                        print(f"postgre_secret: {postgre_secret}")
                        print(f"oracle_secret: {oracle_secret}")
                        print(f"postgre_schema: {postgre_schema}")
                        print(f"postgre_table_name: {postgre_table_name}")
                        print(f"log_bucket: {log_bucket}")
                        
                        if (validate_value(postgre_secret) and
                            validate_value(oracle_secret) and
                            validate_value(postgre_schema) and
                            validate_value(postgre_table_name) and
                            validate_log_bucket(log_bucket)):
                            print("All required values are valid.")
                        else:
                            print("Some required values are missing or invalid.")
                            # Handle the case where some required values are missing or invalid
                            # You can add further actions here if needed
                else:
                    print(f"Invalid filename: {file}")
    
    except Exception as e:
        print(f"An error occurred: {e}")

# Path to the raw folder
raw_folder_path = "datamigration/configurations/raw"

# Perform pre-checks on files in the raw folder
pre_checks(raw_folder_path)
