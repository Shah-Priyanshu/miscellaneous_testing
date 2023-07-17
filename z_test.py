import os
import zipfile

def unzip_last_layer(file_path, target_dir):
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        zip_ref.extractall(target_dir)

def unzip_nested_zip(file_path, target_dir,support_list, flag = False):
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        nested_zip_files = [f for f in zip_ref.namelist() if f.endswith('.zip')] # ak, zs
        
        if not flag:
            
           for elem in nested_zip_files:
                support_list.append(elem)
        
        if nested_zip_files:
            unzip_last_layer(file_path, target_dir) 
            nested_zip_path = os.path.join(target_dir, nested_zip_files[0]) # ak.zip
            unzip_nested_zip(nested_zip_path, target_dir,support_list,  True)
        else:
            support_list = support_list[1:]

            if support_list:
                unzip_last_layer(file_path, target_dir)
                unzip_nested_zip("Temp_submissions\\"+support_list[0], target_dir,support_list,  True)

# Path to the main zip file
main_zip_file = 'Submissions.zip'
# Directory to store the temporary folders
temp_dir = 'Temp_submissions'
support_list = []
# Create the target directory if it doesn't exist
os.makedirs(temp_dir, exist_ok=True)

# Unzip the main zip file and its nested zip files
unzip_nested_zip(main_zip_file, temp_dir,support_list)
