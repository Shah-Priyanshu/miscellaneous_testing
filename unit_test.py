import shutil
import os
import glob
import zipfile
import csv
import re
import sys
import importlib

sys.dont_write_bytecode = True

def some_function():

    from prof_utest import run_unit_tests
    result = run_unit_tests()
    marks = result.testsRun - len(result.failures) - len(result.errors)
    grades = [f"{marks}", ""]  # Grades to be updated in CSV
    return grades   



# class TestSum(unittest.TestCase):
#     # Tests that the function returns the correct sum of two positive integers
#     def test_positive_integers_sum(self):
#         assert sum(2, 3) == 6

#     # Tests that the function returns the correct sum of two negative integers
#     def test_negative_integers_sum(self):
#         assert sum(-2, -3) == -5

#     # Tests that the function returns the correct sum of one positive and one negative integer
#     def test_positive_and_negative_integers_sum(self):
#         assert sum(2, -3) == -1

#     # Tests that the function returns the correct sum of zero and a positive integer
#     def test_zero_and_positive_integer_sum(self):
#         assert sum(0, 5) == 5

#     # Tests that the function returns the correct sum of the maximum possible integer values
#     def test_maximum_integer_values_sum(self):
#         assert sum(2147483647, 2147483647) == 4294967294
        
#     # Tests that the function returns the correct sum of the minimum possible integer values
#     def test_minimum_integer_values_sum(self):
#         assert sum(-2147483648, -2147483648) == -4294967296
        
        
# def run_unit_tests():
#     test_suite = unittest.TestLoader().loadTestsFromTestCase(TestSum)
#     return unittest.TextTestRunner().run(test_suite)
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
            
def return_main_dir():
    os.chdir("..")
    files = glob.glob("*.py")
    if files == []:
        return_main_dir()
    
    

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
    
def find_student_name(zip_file):
    student_name = None
    zip_file_basename = os.path.basename(zip_file)
    matches = re.findall(r"[A-Z][a-z]+", zip_file_basename)
    if len(matches) >= 2:
        student_name = " ".join(matches[:2])
    return student_name

def update_grades_csv(grade_csv_file, assignment_name, student_name, grades):
    results_directory = "results"
    os.makedirs(results_directory, exist_ok=True)
    results_csv_file = os.path.join(results_directory, "results.csv")
    if not os.path.exists(results_csv_file):
        shutil.copy2(grade_csv_file, results_csv_file)

    header = []
    data = []

    with open(results_csv_file, "r") as csv_file:
        reader = csv.reader(csv_file)
        header = next(reader)
        assignment_position = None

        # Find the position of the assignment column
        for idx, col in enumerate(header):
            if assignment_name.lower() in col.lower():
                assignment_position = idx
                break

        if assignment_position is None:
            print("Assignment name not found.")
            return

        # Update the grades for the specific student and assignment
        for row in reader:
            name = row[2] + " " + row[1]
            if name == student_name:
                row[assignment_position] = grades[0]
            data.append(row)

    # Write the updated data (including existing data and new grades) to the result CSV file
    with open(results_csv_file, "w", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(header)
        writer.writerows(data)

def bring_files_to_root_dir():
    return
def generate_custom_output(assignment_name):
    root_destination_dir = os.getcwd()
    submission_directory = glob.glob("*.zip")
    temp_dir = "Temp_submissions"
    os.makedirs(temp_dir, exist_ok=True)
    
    unzip_nested_zip(submission_directory[0], temp_dir)
    
    print(os.getcwd() )
    
    delete_zips(temp_dir)

    student_folders = glob.glob("*")
    
    destination_list = []
    for student_folder in student_folders:
        get_student_file(student_folder)
        destination_list.append(os.getcwd())
        print(os.getcwd())   
        print(f"Running unit tests for student: {student_folder}")
        sys.path.append(os.getcwd()) # Temp_submissions\Arslan Khan\khan4587
        
        source_dir = os.getcwd()
        file_list = os.listdir(source_dir)
        for file_name in file_list:
            source_file = os.path.join(source_dir, file_name)
            destination_file = os.path.join(root_destination_dir, file_name)
            shutil.copy(source_file, destination_file)
        print("1",os.getcwd())
        return_main_dir()
        print("2",os.getcwd())
        grades = some_function()
        print(f"Grades for student {student_folder}: {grades[0]}")
        print("3",os.getcwd())
        
        grades_csv_file = "grades.csv"  # Update with the actual name of the CSV file
        update_grades_csv(grades_csv_file, assignment_name, student_folder, grades)

        print(f"Results for student {student_folder} updated in {grades_csv_file}")
        for file_name in file_list:
            os.remove(file_name)
            print(file_name)
        # os.remove("prof_utest.py")
        # shutil.copy("backup\prof_utest.py","prof_utest.py")
        os.chdir(temp_dir)        
        # shutil.rmtree(temp_dir)


def run_code():
    assignment_name = input("Enter assignment name: ")
    generate_custom_output(assignment_name)

run_code()