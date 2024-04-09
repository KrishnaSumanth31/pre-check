import os
import yaml

def validate_yaml_content(file_path):
    with open(file_path, 'r') as file:
        try:
            yaml_content = yaml.safe_load(file)
        except yaml.YAMLError as exc:
            print(f"Error parsing YAML file {file_path}: {exc}")
            return False

    if not isinstance(yaml_content, list):
        print(f"Invalid YAML structure in {file_path}. Expected a list of dictionaries.")
        return False

    expected_statements = ['delete', 'commit', 'insert', 'commit']
    for idx, statement in enumerate(expected_statements):
        if idx >= len(yaml_content) or 'sql' not in yaml_content[idx] or yaml_content[idx]['sql'] != f"{statement} from $mydata_schema.tablename;":
            print(f"Expected SQL statement '{statement}' not found in {file_path}.")
            return False

    for entry in yaml_content:
        if '$mydata_schema' in entry['sql']:
            print(f"Found invalid schema reference in {file_path}.")
            return False

    return True

def validate_folder(folder_path):
    valid_files = []
    for file_name in os.listdir(folder_path):
        if not file_name.endswith('.yaml'):
            continue
        file_path = os.path.join(folder_path, file_name)
        if validate_yaml_content(file_path):
            valid_files.append((file_name, folder_path))
    return valid_files

def validate_folder_structure(root_path):
    for root, dirs, _ in os.walk(root_path):
        for folder in dirs:
            folder_path = os.path.join(root, folder)
            valid_files = validate_folder(folder_path)
            for file_info in valid_files:
                file_name, folder_path = file_info
                file_path = os.path.join(folder_path, file_name)
                print(f"Valid file: {file_name} | Path: {file_path}")

# Example usage:
root_path = "datamigration/sql"
validate_folder_structure(root_path)
