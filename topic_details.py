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

def topic_details(character_id):
    # Define the interview questions
    questions = [
        "What inspired you to write about this particular topic?",
        "What motivated you to write this book on this particular topic?",
        "What qualifications and experience do you have in the field related to the topic of your book?",
        "How did you become interested in this particular area of study?",
        "Have you published any other books, articles, or research papers in this field?",
        "Have you worked with or collaborated with any other experts in this field?",
        "How do you stay up-to-date with the latest developments and research in this field?",
        "What unique perspective or insights do you bring to the topic that others may not have?",
        "Have you presented your work at conferences or to other academic audiences?",
        "Have you received any awards or recognition for your work in this field?",
        "Have you worked in any related fields or industries outside of academia?",
        "What kind of research did you conduct before writing this book?",
        "Who is the intended audience for your book?",
        "What do you hope readers will take away from your book?",
        "What makes your perspective on this topic unique?",
        "What are some common misconceptions about this topic that you hope to correct in your book?",
        "What are some of the key historical events that shaped the topic you are writing about?",
        "Who are some of the key figures that have influenced this topic?",
        "What are some of the current issues or debates surrounding this topic?",
        "How does your book address these issues or debates?",
        "What are some of the most important findings or insights you uncovered during your research?",
        "How does your book contribute to the larger conversation around this topic?",
        "What are some potential implications of your book for policymakers or the general public?",
        "Are there any key sources or references that you relied on heavily during your research?",
        "How did your own personal experiences or perspectives shape the way you approached this topic?",
        "Are there any particular stories or anecdotes you uncovered during your research that you think readers will find particularly interesting or surprising?",
        "What was the biggest challenge you faced while writing this book and how did you overcome it?",
        "How does your book differ from other books written on this topic?",
        "Did you have to make any difficult decisions about what to include or leave out in your book?",
        "What are some additional resources you recommend to readers who want to learn more about this topic?",
        "What are you working on next? Do you have plans to write any other books on this topic or related topics in the future?"
    ]

    # Create a new window to display the interview
    interview_window = tk.Toplevel(non_fiction_window)
    interview_window.title("Interview topic details")

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
    begin_interview_button = tk.Button(window, text="Topic Interview", command=lambda: topic_details(interview_window, character_id))
    begin_interview_button.grid()

    # Start the tkinter event loop
    window.mainloop()
