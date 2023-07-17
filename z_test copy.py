import os
import zipfile,re,glob,shutil

def find_student_name(zip_file):
    student_name = None
    zip_file_basename = os.path.basename(zip_file)
    matches = re.findall(r"[A-Z][a-z]+", zip_file_basename)
    if len(matches) >= 2:
        student_name = " ".join(matches[:2])
    return student_name

def delete_zips(dir):
    #delete all .zip files in the directory
    os.chdir(dir)
    student_zips = glob.glob("*.zip")
    for student_zip in student_zips:  
        os.remove(student_zip)      



def get_student_file(dir):
    os.chdir(dir) # temp
    files = glob.glob("*")
    for i in files: # arsalan khan
        if i.endswith(".py"):
            print("found")
            print(os.getcwd())
            # copy the file to the main directory
        if os.path.isdir(i):
            get_student_file(i)
            #os.chdir(i) # arsalan khan
                    
    

def unzip_last_layer(file_path, target_dir):
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        zip_ref.extractall(target_dir)

def unzip_nested_zip(file_path, target_dir):
    counter = 0
    flag = False
    support_list = []
    
    while True:
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            nested_zip_files = [f for f in zip_ref.namelist() if f.endswith('.zip')]
            
            if not flag:
                support_list.extend(nested_zip_files)
                    
            
            if nested_zip_files:
                unzip_last_layer(file_path, target_dir)
                nested_zip_path = os.path.join(target_dir, nested_zip_files[0])
                file_path = nested_zip_path
                flag = True
                counter += 1
            else:
                student_name = find_student_name(support_list[0])
                target_dir_stud = os.path.join(target_dir, student_name)
                unzip_last_layer(file_path, target_dir_stud)
                support_list = support_list[1:]
                if support_list:
                    file_path = "Temp_submissions\\"+support_list[0]
                    flag = True
                else:
                    break
    delete_zips(target_dir)
    os.chdir("..")
    get_student_file(target_dir)

# Path to the main zip file
main_zip_file = 'Submissions.zip'
# Directory to store the temporary folders
temp_dir = 'Temp_submissions'

# Create the target directory if it doesn't exist
os.makedirs(temp_dir, exist_ok=True)

# Unzip the main zip file and its nested zip files
unzip_nested_zip(main_zip_file, temp_dir)