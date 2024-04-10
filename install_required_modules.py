#Standard library imports:
import csv
import datetime
import json
import logging
import os
import re
import shutil
import subprocess
import sys
import time
import webbrowser

#Third-party library imports:
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk

#Local imports:
import importlib
import inspect
from definitions import *


def install_required_modules():
    required_modules = ["openai"]
    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            print(f"{module} module is not installed. Installing...")
            os.system(f"{sys.executable} -m pip install {module}")
