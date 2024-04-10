# Standard library imports
import logging
import tkinter as tk
import time

# Third-party library imports
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk

# Local imports
import importlib

# Initialize logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def open_topic_details(event, logger):

    
    # Get the clicked table widget
    clicked_table = event.widget

    # Get the selected item from the clicked table
    selected_item = clicked_table.selection()

    logger.setLevel(logging.CRITICAL)  # Disable logging


    # Create a new window to display the topic details
    topic_details_window = tk.Toplevel(non_fiction_window)
    topic_details_window.title("Topic Details")

    # Create a button to resume the interview
    resume_interview_button = ttk.Button(character_window, text="Resume Interview", command=lambda: resume_interview(character_id))
    resume_interview_button.grid(side="bottom", pady=10)

    # Set window size and position
    screen_width = topic_details_window.winfo_screenwidth()
    screen_height = topic_details_window.winfo_screenheight()
    window_width = int(screen_width * 0.5)
    window_height = int(screen_height * 0.5)
    x = int((screen_width - window_width) / 2)
    y = int((screen_height - window_height) / 2)
    topic_details_window.geometry(f"{window_width}x{window_height}+{x}+{y}")


    # Retrieve the topic details based on the character_id
    topic_info = get_topic_details(character_id)

    # Create a label and text box for each question and answer
    answer_text_vars = []
    for index, (question, answer) in enumerate(topic_info.items()):
        question_label = tk.Label(topic_details_window, text=question, font=("Arial", 14), wraplength=window_width-50)
        question_label.grid(row=index, column=0, padx=25, pady=10, sticky="W")

        answer_text = tk.StringVar()
        answer_text.set(answer)
        answer_text_vars.append(answer_text)
        answer_entry = tk.Entry(topic_details_window, textvariable=answer_text, font=("Arial", 12))
        answer_entry.grid(row=index, column=1, padx=25, pady=10)

    def save_and_close():
        updated_topic_info = {question: text_var.get() for (question, _), text_var in zip(topic_info.items(), answer_text_vars)}
        update_topic_details(character_id, updated_topic_info)
        topic_details_window.destroy()

    # Create a button to save the changes and close the window
    save_exit_button = tk.Button(topic_details_window, text="Save and Close", command=save_and_close)
    save_exit_button.grid(row=len(topic_info), column=0, columnspan=2, pady=10, sticky="S")

    # Add a "Cancel" button to the frame
    cancel_button = ttk.Button(button_frame, text="Cancel", command=topic_details_window.destroy)
    cancel_button.grid(row=0, column=1, padx=5, pady=10)

    # Start the tkinter event loop
    topic_details_window.mainloop()

logger.setLevel(logging.INFO)  # Enable logging again
