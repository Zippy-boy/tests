import os
# a file explorer

files = os.listdir(os.environ["USERPROFILE"])
for file in files:
    print(f"{files.index(file)}: {file}")

