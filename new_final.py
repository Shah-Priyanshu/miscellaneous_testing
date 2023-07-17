import subprocess, os, shutil
#import prof_utest

print("\nstarts here\n")

result2 = subprocess.run(['python', 'prof_utest.py'], capture_output=True, text=True)
#std_print = result2.stdout.split("\n")[-2]
std_print = result2.stdout

print(std_print)
# print("just final marks printed:", std_print.split("/")[0].split(" ")[-2])

print("-"*50)
print()
os.remove("student.py")
shutil.copyfile("copy/student.py", "student.py")

result = subprocess.run(['python', 'prof_utest.py'], capture_output=True, text=True)
# std_print = result.stdout.split("\n")[-2]
std_print = result.stdout
print(std_print)
# print("just final marks printed:", std_print.split("/")[0].split(" ")[-2],"\n")

print("ends here")