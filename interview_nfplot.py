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


def interview_nfplot(character_id):
    # Define the interview questions
    questions = [
        "What is the genre of the story, and how does it influence the plot?",
        "What is the central conflict of the story?",
        "Who is the protagonist, and what is their goal?",
        "Who or what is the antagonist, and what is their motivation?",
        "What are the stakes for the protagonist if they fail to achieve their goal?",
        "What are the key events that occur in the story, and in what order?",
        "What is the inciting incident that sets the plot in motion?",
        "What are the obstacles the characters face in achieving their goals?",
        "What are the primary conflicts and how do they get resolved?",
        "What are the subplots of the story, and how do they relate to the main plot?",
        "What are the key plot twists or surprises in the story?",
        "What are the key symbols or motifs in the story, and how do they relate to the plot?",
        "What are the themes that the story explores?",
        "What is the pacing of the story, and how does it contribute to the plot?",
        "What is the tone of the story, and how does it change over time?",
        "How does the story begin, and what draws the reader in?",
        "How does the language or writing style of the story contribute to the plot?",
        "How does the point of view (e.g. first person, third person) affect the plot?",
        "What are the character arcs of the main characters, and how do they intersect with the plot?",
        "What makes the protagonist different from other characters?",
        "How does the protagonist change over the course of the story?",
        "What are the cultural or historical contexts of the story, and how do they influence the plot?",
        "What is the backstory of the characters, and how does it affect the plot?",
        "What are the external and internal forces that shape the story's events?",
        "What are the key conflicts between characters, and how do they affect the plot?",
        "What are the moral or ethical questions raised by the story, and how do they affect the plot?",
        "What is the relevance of the story to the contemporary world?",
        "What is the overall message or lesson of the story?",
        "What are the key symbols or motifs in the story, and how do they relate to the plot?",
        "What is the climax of the story, and how does it affect the outcome?",
        "What is the ultimate fate of the characters?",
        "How does the story resolve the central conflict, and is it satisfying?"
    ]

    # Create a new window to display the interview
    interview_window = tk.Toplevel(non_fiction_window)
    interview_window.title("Interview Non-Fiction Plot")

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
    begin_interview_button = tk.Button(window, text="Non-Fiction Plot Interview", command=lambda: interview_nfplot(interview_window, character_id))
    begin_interview_button.grid()

    # Start the tkinter event loop
    window.mainloop()
