import os
import yaml

def check_file_structure(file_path):
    # Check if file exists
    if not os.path.exists(file_path):
        return False

    # Check if file extension is YAML or YML
    if not file_path.lower().endswith(('.yaml', '.yml')):
        return False

    # Check if file name contains "data_extract"
    if "data_extract" not in os.path.basename(file_path):
        return False

    return True

def check_configurations(config_data):
    required_fields = ['postgre_secret', 'oracle_secret', 'details']

    for field in required_fields:
        if field not in config_data:
            return False

    details = config_data.get('details', {})
    tasks = details.get('task', [])

    for task in tasks:
        if not all(task.get(key) for key in ['postgre_schema', 'postgre_table_name']):
            return False
        
        # Check naming convention for log_bucket
        if 'log_bucket' in task:
            log_bucket_value = task['log_bucket']
            if not log_bucket_value.startswith("my_bucket_config"):
                return False

    return True

def main():
    file_path = "pre-check/datamigration/configurations/raw/data_extract.yml"  # Example file name

    if not check_file_structure(file_path):
        print("File does not meet the required structure.")
        return

    with open(file_path, 'r') as file:
        try:
            config_data = yaml.safe_load(file)
            if check_configurations(config_data):
                print("Pre-checks passed successfully.")
            else:
                print("Pre-checks failed. Check your configurations.")
        except yaml.YAMLError as e:
            print("Error loading YAML file:", e)

if __name__ == "__main__":
    main()
