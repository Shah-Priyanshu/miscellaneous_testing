import shutil
import os
import glob
import zipfile
import csv
import re
import unittest
from student import sum

class TestSum(unittest.TestCase):
    # Tests that the function returns the correct sum of two positive integers
    def test_positive_integers_sum(self):
        assert sum(2, 3) == 6

    # Tests that the function returns the correct sum of two negative integers
    def test_negative_integers_sum(self):
        assert sum(-2, -3) == -5

    # Tests that the function returns the correct sum of one positive and one negative integer
    def test_positive_and_negative_integers_sum(self):
        assert sum(2, -3) == -1

    # Tests that the function returns the correct sum of zero and a positive integer
    def test_zero_and_positive_integer_sum(self):
        assert sum(0, 5) == 5

    # Tests that the function returns the correct sum of the maximum possible integer values
    def test_maximum_integer_values_sum(self):
        assert sum(2147483647, 2147483647) == 4294967294
        
    # Tests that the function returns the correct sum of the minimum possible integer values
    def test_minimum_integer_values_sum(self):
        assert sum(-2147483648, -2147483648) == -4294967296
        
def run_unit_tests():
    test_suite = unittest.TestLoader().loadTestsFromTestCase(TestSum)
    return unittest.TextTestRunner().run(test_suite)

def unzip_recursive(zip_file, temp_dir):
    with zipfile.ZipFile(zip_file, "r") as z:
        z.extractall(temp_dir)
        inner_zip_files = []
        for file_info in z.infolist():
            if file_info.is_dir():
                inner_zip_files.append(file_info.filename)
        return inner_zip_files

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
        print(f"Assignment position: {assignment_position}, Assignment name: {header[assignment_position]}")

        # Update the grades for the specific student and assignment
        for row in reader:
            if row[2] == student_name:
                row[assignment_position] = grades[0]
            data.append(row)

    # Write the updated data (including existing data and new grades) to the result CSV file
    with open(results_csv_file, "w", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(header)
        writer.writerows(data)

def generate_custom_output(assignment_name):
    result_directory = "results"
    os.makedirs(result_directory, exist_ok=True)

    student_zips = glob.glob("*.zip")
    print(f"Found {len(student_zips)} student zip files")

    for student_zip in student_zips:
        student_name = find_student_name(student_zip)
        if student_name:
            print(f"Processing student: {student_name}")

            temp_dir = f"temp_{student_name}"
            os.makedirs(temp_dir, exist_ok=True)
            inner_zip_files = unzip_recursive(student_zip, temp_dir)

            while inner_zip_files:
                new_inner_zip_files = []
                for inner_zip_file in inner_zip_files:
                    inner_temp_dir = os.path.join(temp_dir, inner_zip_file)
                    os.makedirs(inner_temp_dir, exist_ok=True)
                    inner_zip_path = os.path.join(temp_dir, inner_zip_file + ".zip")
                    inner_zip_files = unzip_recursive(inner_zip_path, inner_temp_dir)
                    new_inner_zip_files.extend(inner_zip_files)
                inner_zip_files = new_inner_zip_files

            os.chdir(temp_dir)
            print(f"Running unit tests for student: {student_name}")
            result = run_unit_tests()
            os.chdir("..")

            marks = result.testsRun - len(result.failures) - len(result.errors)
            grades = [f"{marks}", ""]  # Grades to be updated in CSV
            print(f"Grades for student {student_name}: {grades[0]}")
            grades_csv_file = "grades.csv"  # Update with the actual name of the CSV file
            update_grades_csv(grades_csv_file, assignment_name, student_name, grades)

            print(f"Results for student {student_name} updated in {grades_csv_file}")
            shutil.rmtree(temp_dir)

def run_code():
    assignment_name = input("Enter assignment name: ")
    generate_custom_output(assignment_name)

run_code()