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

def describe_nfhistime(character_id):
    # Define the interview questions
    questions = [
        "How did the historical events, including societal, political, and economic factors, shape the events and characters described in your book?",
        "What kind of research did you conduct to accurately depict the historical context of your book?",
        "Did you uncover any surprising or little-known facts about the time period you were researching?",
        "How does the historical context of your book, including its connection to larger societal or cultural movements, shape the characters and themes explored in your book?",
        "Did you have to make any creative decisions about the historical accuracy of your book?",
        "What impact did the historical events described in your book have on the world at large?",
        "What kind of primary sources or archival materials did you use to research the historical context of your book?",
        "How did you decide which historical events or factors to include in your book?",
        "What is the earliest significant event in the history of your story world?",
        "What other events in the history of your story world have had lasting effects on the present day?",
        "What are some important dates in the history of your story world?",
        "How has the political landscape of your story world changed over time?",
        "What technological advancements have occurred in your story world?",
        "What cultural changes have occurred in your story world?",
        "What significant events have occurred in the lives of your main characters, secondary characters, and antagonists?",
        "What major conflicts have occurred in the history of your story world?",
        "Can you describe the chronological timeline of events covered in your book?",
        "How do the events in your book connect to larger historical or societal trends or movements?",
        "Are there any specific turning points or moments of change in the timeline of your book?",
        "What kind of research did you conduct to accurately depict the timeline of your book?",
        "How do the events in your book build upon one another and contribute to the overall narrative?",
        "How does the timeline of your book influence the behavior or actions of the characters described in it?",
        "Can you describe any cultural or societal elements unique to the time period covered in your book?",
        "What kind of primary sources or archival materials did you use to research the timeline of your book?",
        "How does the timeline of your book connect to larger historical or cultural movements?"
    ]

    # Create a new window to display the interview
    interview_window = tk.Toplevel(non_fiction_window)
    interview_window.title("Non-Fiction History, Background, and Timeline Information")

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
    begin_interview_button = tk.Button(window, text="Non-Fiction History, Background, and Timeline Information", command=lambda: describe_nfhistime(interview_window, character_id))
    begin_interview_button.grid()

    # Start the tkinter event loop
    window.mainloop()
