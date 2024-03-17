"""files_operations"""
import os
import time
import shutil
from pathlib import Path


# Basic Directory Cleanup: Delete Empty Folders
def delete_empty_folders(path: str):
    """Delete empty folders"""
    for dir in os.listdir(path):
        dir_path = os.path.join(path, dir)
        if os.path.isdir(dir_path) and not os.listdir(dir_path):
            print("Deleting empty folder...", dir)
            os.rmdir(dir_path)
        if os.path.isdir(dir_path) and os.listdir(dir_path):
            delete_empty_folders(dir_path)
    return

# Delete Files older than days
def delete_old_files(path: str, days: int):
    """Delete files older than days"""
    current = time.time()
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        if os.path.isfile(file_path):
            file_age = (current - os.path.getmtime(file_path)) / (24 * 3600)
            if file_age > float(days):
                os.remove(file_path)
                print(f"Deleted {file} as it was older than {days} days")
    return

# Organize files into folders according to their extensions.
def organize_files_extensions(path: str):
    """Organize files into folders according to their extensions."""
    print(f"path: {path}")
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        if os.path.isfile(file_path):
            _, extension = os.path.splitext(file)
            extension_path = os.path.join(path, extension.replace(".", ""))
            print(extension_path)
            if os.path.isdir(extension_path):
                #shutil.move(file_path, extension_path)
                Path(file_path).rename(os.path.join(extension_path, file))
            else:
                os.mkdir(extension_path)
                #shutil.move(file_path, extension_path)
                Path(file_path).rename(os.path.join(extension_path, file))
    
    # files = [file for file in os.listdir(path) if os.path.isfile(os.path.join(path, file))]
    # extensions = (os.path.splitext(file)[1].replace(".", "") for file in os.listdir(path) if os.path.isfile(os.path.join(path, file)))
    # print(extensions)
    # for ext in extensions:
    #     print(ext)
    #     if os.path.isdir(os.path.join(path, ext)):
    #         pass
    #     else:
    #         os.mkdir(os.path.join(path, ext))
    # join_path = lambda file: os.path.splitext(file)[1].replace(".", "")
    # for file in files:
    #     print(file)
    #     print(os.path.join(path, file))
    #     print(os.path.join(path, join_path(file), file))
    #     Path(os.path.join(path, file)).rename(os.path.join(path, join_path(file), file))
    return