# Standard library imports
import csv
import datetime
import logging
import os
import shutil
import subprocess
import sys
import time
import webbrowser

# Third-party library imports
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import simpledialog

# Local imports
import importlib
import inspect
from definitions import *

def get_bio_text(character_id):
    # Read the log file and find all lines containing the character ID
    with open("log.txt", "r") as log_file:
        matching_lines = [line for line in log_file if character_id in line]

    # Join the matching lines together as a string
    bio_text = "".join(matching_lines)

    return bio_text
