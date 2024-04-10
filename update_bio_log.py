# Standard library imports
import csv
import datetime
import logging
import os

# Third-party library imports
import tkinter as tk
from tkinter import messagebox

# Local imports
import importlib

def update_bio_log(character_id, new_info):
    logger.setLevel(logging.CRITICAL)  # Disable logging
    # Read the log file and store the contents as a list of lines
    with open("log.txt", "r") as f:
        lines = f.readlines()

    # Find all the lines that contain the character ID
    matching_lines = []
    for i, line in enumerate(lines):
        if character_id in line:
            matching_lines.append(i)

    # Delete the matching lines from the list
    for i in reversed(matching_lines):
        del lines[i]

    # Write the updated character information to the log file
    with open("log.txt", "a") as f:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"{timestamp} {character_id}\n")
        for key, value in new_info.items():
            f.write(f"{key}: {value}\n")
        f.write("\n")
    logger.setLevel(logging.INFO)  # Enable logging again
