import os
import yaml

def validate_yaml_file(file_path, folder_path):
    with open(file_path, 'r') as yaml_file:
        try:
            data = yaml.safe_load(yaml_file)
            if isinstance(data, list):
                # Check if the YAML data is a list of dictionaries
                for item in data:
                    if not all(key in item for key in ['sql']):
                        print(f"Missing keys in YAML file: {file_path}")
                        return
                print(f"All keys found in sequence in YAML file: {file_path}")
            else:
                raise ValueError("Invalid YAML file format")
        except yaml.YAMLError as e:
            print(f"Error parsing YAML file {file_path}: {e}")
            with open(file_path, 'r') as f:
                print(f"Contents of {file_path}:\n{f.read()}")
        except ValueError as e:
            print(f"Error processing YAML file {file_path}: {e}")
            with open(file_path, 'r') as f:
                print(f"Contents of {file_path}:\n{f.read()}")

def validate_folder(folder_path):
    valid_files = []
    files = os.listdir(folder_path)
    
    # Check if there are any files in the directory
    has_files = any(os.path.isfile(os.path.join(folder_path, f)) for f in files)
    if not has_files:
        return valid_files

    for file_name in files:
        file_path = os.path.join(folder_path, file_name)
        if folder_path.endswith(('stg/labtest', 'trn/labtest')):
            if file_name.endswith('.yaml'):
                validate_yaml_file(file_path, folder_path)
            elif file_name.startswith('insert_script'):
                valid_files.append((file_name, folder_path))
            else:
                print(f"Incorrect naming convention in {folder_path}: {file_name}")

    return valid_files

def validate_folder_structure(root_path):
    stg_path = os.path.join(root_path, 'stg/labtest')
    trn_path = os.path.join(root_path, 'trn/labtest')
    
    for folder_path in (stg_path, trn_path):
        valid_files = validate_folder(folder_path)
        for file_info in valid_files:
            file_name, folder_path = file_info
            file_path = os.path.join(folder_path, file_name)
            print(f"Valid file: {file_name} | Path: {file_path}")

# Example usage:
root_path = "datamigration/sql"
validate_folder_structure(root_path)
