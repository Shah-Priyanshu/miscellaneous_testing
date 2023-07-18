import subprocess, os, shutil
#import prof_utest


def process_grades(grades):
    grades = grades.split("\n")
    grades = grades[0]
    total_tests = len(grades)
    for i in grades:
        if i == "F":
            total_tests -= 1
        elif i == "E":
            total_tests -= 1
    grades = str(total_tests)
    return grades


print("\nstarts here")

result2 = subprocess.run(['python', 'prof_utest.py'], capture_output=True, text=True)
#std_print = result2.stdout.split("\n")[-2]
std_print = result2.stdout
stderr = result2.stderr
# print(std_print)
# print(stderr)
grades = process_grades(stderr)
print(grades)
# print("just final marks printed:", std_print.split("/")[0].split(" ")[-2])

# print("-"*50)
# print()
# os.remove("student.py")
# shutil.copyfile("copy/student.py", "student.py")

# result = subprocess.run(['python', 'prof_utest.py'], capture_output=True, text=True)
# # std_print = result.stdout.split("\n")[-2]
# std_print = result.stdout
# print(std_print)
# print("just final marks printed:", std_print.split("/")[0].split(" ")[-2],"\n")

print("ends here")

# Get the final grades from unit tests
