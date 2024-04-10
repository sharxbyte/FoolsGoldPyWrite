# Standard library imports
import os
import shutil
import time

def Emergency_backup():
    try:
        # Back up all data to an "emergency backups" directory
        backup_directory_name = "emergency backups"
        if not os.path.exists(backup_directory_name):
            os.mkdir(backup_directory_name)

        timestamped_backup_dir = os.path.join(backup_directory_name, time.strftime('%Y-%m-%d %H-%M-%S'))
        os.mkdir(timestamped_backup_dir)

        files_to_backup = ["interview.txt", "log.txt", "outline.txt", "author_style.txt"]
        for file in files_to_backup:
            if os.path.exists(file):
                shutil.copyfile(file, os.path.join(timestamped_backup_dir, file))

    except Exception as e:
        # You can either handle the exception internally or re-raise it for the calling module to handle
        # For now, I'm re-raising the exception after printing an error message
        print(f"Error occurred during emergency backup: {e}")
        raise
