import os
import zipfile

def unzip_last_layer(file_path, target_dir):
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        zip_ref.extractall(target_dir)

counter = 0
def unzip_nested_zip(file_path, target_dir, flag = False):
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        nested_zip_files = [f for f in zip_ref.namelist() if f.endswith('.zip')] # ak, zs
        
        if not flag:
            support_list = []
            for elem in nested_zip_files:
                support_list.append(elem)
        
        if nested_zip_files:
            unzip_last_layer(file_path, target_dir) 
            nested_zip_path = os.path.join(target_dir, nested_zip_files[0]) # ak.zip
            unzip_nested_zip(nested_zip_path, target_dir, True)
            counter += 1
        else:
            support_list = support_list[1:]
            support_list[0]
            unzip_last_layer(file_path, target_dir)
            unzip_nested_zip(support_list[0], target_dir, True)

# Path to the main zip file
main_zip_file = 'Submissions.zip'
# Directory to store the temporary folders
temp_dir = 'Temp_submissions'

# Create the target directory if it doesn't exist
os.makedirs(temp_dir, exist_ok=True)

# Unzip the main zip file and its nested zip files
unzip_nested_zip(main_zip_file, temp_dir)
