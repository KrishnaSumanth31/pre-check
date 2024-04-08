import os
import yaml

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
                        
                        # Extract required values
                        postgre_secret = yaml_data.get("postgre_secret")
                        oracle_secret = yaml_data.get("oracle_secret")
                        
                        # Print extracted values for better understanding
                        print(f"postgre_secret: {postgre_secret}")
                        print(f"oracle_secret: {oracle_secret}")
                        
                        details = yaml_data.get("details")
                        if details:
                            tasks = details.get("task")
                            if tasks:
                                for task in tasks:
                                    postgre_schema = task.get("postgre_schema")
                                    postgre_table_name = task.get("postgre_table_name")
                                    log_bucket = task.get("log_bucket")
                                    
                                    print(f"postgre_schema: {postgre_schema}")
                                    print(f"postgre_table_name: {postgre_table_name}")
                                    print(f"log_bucket: {log_bucket}")
                                    
                                    # Perform validation checks
                                    if not (validate_value(postgre_secret) and
                                            validate_value(oracle_secret) and
                                            validate_value(postgre_schema) and
                                            validate_value(postgre_table_name)):
                                        raise ValueError("One or more required fields are missing or invalid.")
                                    
                                    if not validate_log_bucket(log_bucket):
                                        raise ValueError(f"The log bucket '{log_bucket}' does not match the expected pattern.")
                                        
                                    print("All required values are valid.")
                            else:
                                print("No tasks found.")
                        else:
                            print("No details found.")
                else:
                    print(f"Invalid filename: {file}")
    
    except Exception as e:
        print(f"An error occurred: {e}")

# Path to the raw folder
raw_folder_path = "datamigration/configurations/raw"

# Perform pre-checks on files in the raw folder
pre_checks(raw_folder_path)
