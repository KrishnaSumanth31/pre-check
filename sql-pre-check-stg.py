import os
import glob
import yaml

def load_yaml(file_path):
    """Load YAML file and return its content."""
    with open(file_path, 'r') as f:
        try:
            return yaml.safe_load(f)
        except yaml.YAMLError as e:
            print(f"Error parsing YAML in {file_path}: {e}")
            return None

def validate_sequence(content):
    """Validate if YAML content contains the required keywords."""
    keywords = ["delete", "commit", "insert", "commit"]
    content_str = yaml.dump(content, default_flow_style=True)
    index = 0
    for keyword in keywords:
        index = content_str.find(keyword, index)
        if index == -1:
            return False
    return True

def check_yaml_files(directory):
    """Check YAML files in the specified directory."""
    for file_path in glob.glob(os.path.join(directory, "**/insert_script*.yml"), recursive=True):
        if os.path.isfile(file_path) and file_path.startswith('datamigration/sql/stg/labtest') or file_path.startswith('datamigration/sql/trn/labtest'):
            print(f"\nValid File: {file_path}")
            content = load_yaml(file_path)
            if content:
                if validate_sequence(content):
                    print("Sequence matches: delete, commit, insert, commit")
                else:
                    print("Sequence doesn't match: delete, commit, insert, commit")
            else:
                print("Error: No valid YAML content found")

def main():
    base_dir = "datamigration/sql"
    check_yaml_files(base_dir)

if __name__ == "__main__":
    main()
