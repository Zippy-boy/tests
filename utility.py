import getpass
import os

def get_username():
    return getpass.getuser()

def delete_file(file_path):
    os.remove(file_path)