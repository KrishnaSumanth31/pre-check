import os
import glob

# Define the base directory
base_dir = "datamigration/sql"

# Check file names
print("Checking file names...")
insert_script_files = glob.glob(os.path.join(base_dir, "*/insert_script*.yml"))
if not insert_script_files:
    print("No files found with names starting with 'insert_script'.")
else:
    print("Files found:")
    for file in insert_script_files:
        print(file)

# Check file extension and path
print("\nChecking file extensions and paths...")
yml_files = glob.glob(os.path.join(base_dir, "**/*.yml"), recursive=True) + glob.glob(os.path.join(base_dir, "**/*.yaml"), recursive=True)
if not yml_files:
    print("No .yml or .yaml files found.")
else:
    print("YAML files found:")
    for file in yml_files:
        print(file)

# Check file contents
print("\nChecking file contents...")
for file in yml_files:
    print(f"File: {file}")
    with open(file, 'r') as f:
        content = f.read()
        if "executes:" in content:
            print("File contains 'executes' section.")
            if "delete" in content and "commit" in content and "insert" in content and content.index("delete") < content.index("commit") < content.index("insert") < content.index("commit"):
                print("Sequence: delete, commit, insert, commit")
            else:
                print("Sequence doesn't match: delete, commit, insert, commit")
        else:
            print("File does not contain 'executes' section.")
