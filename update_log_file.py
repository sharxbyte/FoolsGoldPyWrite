# Standard library imports
import os
import logging
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk





def update_log_file(work_type):
    logger.setLevel(logging.CRITICAL)  # Disable logging
    # Open log file in read mode and read all the lines
    with open("log.txt", "r") as f:
        lines = f.readlines()

    # Update the first line and add a break after it
    lines[0] = f"{lines[0].strip()}\n\n"
    # Update the second line with the new work_type
    lines[1] = f"Work type: {work_type}\n"

    # Open log file in write mode and write the updated lines
    with open("log.txt", "w") as f:
        f.writelines(lines)
    logger.setLevel(logging.INFO)  # Enable logging again
