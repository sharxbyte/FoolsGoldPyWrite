# Standard library imports
import datetime
import os
import subprocess
import sys
import time

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

def describe_biosetting(character_id):
    # Define the interview questions
    questions = [
        "How does the physical setting of your book, including any landmarks or features, contribute to the events or themes in your book?",
        "How does the setting contribute to the overall mood or tone of your book?",
        "What kind of research did you conduct to accurately depict the setting of your book, and did you draw any inspiration from real-life locations or places?",
        "Did you have to make any creative decisions about the setting that differed from historical or factual accuracy?",
        "How does the setting influence the behavior or actions of the characters in your book?",
        "Can you describe any cultural or societal elements unique to the setting of your book?",
        "How does the setting change over the course of your book?"
    ]

    # Create a new window to display the interview
    interview_window = tk.Toplevel(Biography_window)
    interview_window.title("Biography Setting Information")

    # Set window size and position
    screen_width = interview_window.winfo_screenwidth()
    screen_height = interview_window.winfo_screenheight()
    window_width = int(screen_width * 0.5)
    window_height = int(screen_height * 0.5)
    x = int((screen_width - window_width) / 2)
    y = int((screen_height - window_height) / 2)
    interview_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    # Create a label to display the current question
    current_question_label = tk.Label(interview_window, text=questions[0], font=("Arial", 14), wraplength=window_width-50)
    current_question_label.grid(row=0, column=0, padx=25, pady=25, sticky="W")

    # Create a text box for the user's answer
    answer_text = tk.StringVar()
    answer_entry = tk.Entry(interview_window, textvariable=answer_text, font=("Arial", 12))
    answer_entry.grid(row=1, column=0, padx=25, pady=10)

    # Define a function to go to the next question
    def next_question(current_question):
        # Save the answer to the current question
        character_info[current_question] = answer_text.get()

        # Go to the next question or close the interview if all questions have been asked
        if current_question == questions[-1]:
            # Close the interview window
            interview_window.destroy()

            # Update the character bio with the interview data
            update_character_bio(character_id, character_info)
        else:
            # Move to the next question
            next_question_index = questions.index(current_question) + 1
            current_question_label.config(text=questions[next_question_index])
            answer_text.set(character_info.get(questions[next_question_index], ""))

    # Define a function to go to the previous question
    def prev_question(current_question):
        # Save the answer to the current question
        character_info[current_question] = answer_text.get()

        # Go to the previous question
        prev_question_index = questions.index(current_question) - 1
        current_question_label.config(text=questions[prev_question_index])
        answer_text.set(character_info.get(questions[prev_question_index], ""))

    # Create buttons to navigate the questions
    prev_button = tk.Button(interview_window, text="Back", command=lambda: prev_question(current_question_label.cget("text")))
    prev_button.grid(row=2, column=0, padx=25, pady=10, sticky="W")

    next_button = tk.Button(interview_window, text="Next", command=lambda: next_question(current_question_label.cget("text")))
    next_button.grid(row=2, column=0, padx=25, pady=10, sticky="E")

    save_exit_button = tk.Button(interview_window, text="Save and Exit", command=interview_window.destroy)
    save_exit_button.grid(row=2, column=0, pady=10, sticky="S")

    # Create Begin Interview button
    begin_interview_button = tk.Button(window, text="Biography Setting Information", command=lambda: describe_biosetting(interview_window, character_id))
    begin_interview_button.grid()

    # Start the tkinter event loop
    window.mainloop()
