import os
def check_files(directory):
    prefix = os.environ.get('FILE_PREFIX')
    for root, dirs, files in os.walk(directory):
       for file in files:
           file_path = os.path.join(root, file)
           if file.endswith('.py') or file.endswith('.yml'):
              if not file_is_valid(file, prefix):
                  print(f"File {file} in {root} does not meet naming convention.")
           else:
              print(f"File {file} in {root} has incorrect extension.")

def file_is_valid(file_name, prefix):
   if file_name.startswith(prefix):
       return True
   else:
       return False

if __name__ == "__main__":
  directory = os.environ.get('DIRECTORY')
  prefix = os.environ.get('PREFIX')
  check_files(directory, prefix)
