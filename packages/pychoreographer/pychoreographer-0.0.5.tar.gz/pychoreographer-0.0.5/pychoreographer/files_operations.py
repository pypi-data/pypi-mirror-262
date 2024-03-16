"""files_operations"""
import os
import time


# Basic Directory Cleanup
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
