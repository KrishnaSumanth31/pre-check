import os
import yaml

def validate_file_name(filename):
    # Check if the filename starts with "data_extract" and has a YAML extension
    return filename.startswith("data_extract") and filename.endswith(".yml")

def validate_value(value, field_name):
    # Check if the value is not null or empty
    if value is None or value.strip() == "":
        raise ValueError(f"The field '{field_name}' is missing or empty.")

def validate_log_bucket(log_bucket):
    # Check if the log_bucket matches the naming pattern
    if not log_bucket.startswith("my_bucket_config"):
        raise ValueError(f"The log bucket '{log_bucket}' does not match the expected pattern.")

def validate_path_value(path_value, field_name, expected_prefix):
    # Check if the path_value starts with the expected_prefix
    if not path_value.startswith(expected_prefix):
        raise ValueError(f"The {field_name} '{path_value}' does not match the expected pattern '{expected_prefix}*'.")
    
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
                        
                        try:
                            validate_value(postgre_secret, "postgre_secret")
                            validate_value(oracle_secret, "oracle_secret")
                        except ValueError as ve:
                            print(ve)
                            continue
                        
                        details = yaml_data.get("details")
                        if details:
                            tasks = details.get("task")
                            if tasks:
                                for task in tasks:
                                    postgre_schema = task.get("postgre_schema")
                                    postgre_table_name = task.get("postgre_table_name")
                                    log_bucket = task.get("log_bucket")
                                    log_path = task.get("log_path")
                                    raw_bucket = task.get("raw_bucket")
                                    raw_path = task.get("raw_path")
                                    archival_path = task.get("archival_path")
                                    
                                    try:
                                        validate_value(postgre_schema, "postgre_schema")
                                        validate_value(postgre_table_name, "postgre_table_name")
                                    except ValueError as ve:
                                        print(ve)
                                        continue
                                    
                                    try:
                                        validate_log_bucket(log_bucket)
                                    except ValueError as ve:
                                        print(ve)
                                        continue
                                    
                                    try:
                                        validate_path_value(log_path, "log_path", "sql/raw/")
                                        validate_path_value(raw_bucket, "raw_bucket", "az-hbs-bank-dm-eu-west-1-raw")
                                        validate_path_value(raw_path, "raw_path", "hbsbank/data-migration")
                                        validate_path_value(archival_path, "archival_path", "archive/hbsbank/data-migration")
                                    except ValueError as ve:
                                        print(ve)
                                        continue
                                    
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
