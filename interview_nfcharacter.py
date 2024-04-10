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

def interview_nfcharacter(character_id):
    create_name_window()
    # Define the interview questions
    questions = [
        "What was the character's family like when they were growing up?",
        "Can you tell me about the character's early life?",
        "Did/does the character have any siblings? If so, what were they like?",
        "What is the character's age?",
        "What is the character's species?",
        "What is the character's gender?",
        "Please describe the character's physical appearance.",
        "What is the character's sexuality?",
        "Enter the character's job title:",
        "Describe the character's personality type, along with any distinctive traits",
        "Is this character a narrator?",
        "How does the character change over the course of the story?",
        "What is the character's role in the story?",
        "What is the character's relationship with other characters?",
        "What is the character's worldview?",
        "What is the character's moral code?",
        "What are the character's hobbies or interests?",
        "What is the character's preferred style of communication?"
        "What were the character's parents like?",
        "Describe the relationship of the character with each parent",
        "What was the character's family like when they were growing up?",
        "Can you tell me about the character's early life?",
        "Did/does the character have any siblings? If so, what were they like?",
        "Did/does the character have any other family members who were important to them?",
        "Did/does the character have any pets?",
        "Who was the character's childhood hero?",
        "What was the character's family's financial situation like?",
        "What was discipline like within the character's household?",
        "Did the character's parents have any separations or divorces?",
        "Did anyone in the character's family struggle with substance abuse?",
        "Did the character witness violence in the neighborhood(s) where they grew up?",
        "Have they experienced any other traumatic events in their childhood?",
        "Does the character have any fun or exciting stories from their childhood?",
        "What about stories involving their parents, siblings, or cousins?",
        "Describe a time or times when the character got in trouble, and what they learned from it?",
        "What is the character's religious affiliation, if any?",
        "How devout is the character in their religious practices?",
        "What is the character's political affiliation, if any?",
        "How often does the character vote or participate in other civic duties?",
        "Has the character participated in any protests, canvassing, or other activism? If so, please describe.",
        "What were the most significant events or experiences in the character's teens, and how did they shape their character and values?",
        "Who would the character say had the biggest positive impact on their life? Why?",
        "If the character could meet any 3 people or groups, living or dead, who would they be and why?",
        "Who else does the character look up to as an adult?",
        "Describe the character's education, including any influential teachers or mentors who played a significant role in their intellectual or personal growth?",
        "What is the character's understanding of racial relations on a global scale?",
        "What is the character's understanding of racial relations on a local scale?",
        "What are the character's most significant personal and professional relationships? How have they influenced their life and career?",
        "Does the character have a core philosophy or motto that guides their actions and decisions?",
        "If the character had a week with no responsibilities and a significant stipend to spend on experiences (not possessions), how would they spend it? With whom?",
        "What are the character's passions and interests outside of their career? How have they contributed to their personal growth and well-being?",
        "What subjects fascinate the character? Why?",
        "What items, foods, musical groups, fandoms, etc. does the character feel like they couldn't live without?",
        "What does the character absolutely hate?",
        "What things or people motivate the character in life?",
        "What would the character do if they lost one of the things that motivate them?",
        "What other fears does the character have?",
        "What would the character consider to be their biggest triumph?",
        "What other successes bring the character joy to think about?",
        "What would the character consider their biggest failure?",
        "What other things does the character wish they'd done better on?",
        "Describe any public or private struggles the character has faced, such as health issues, personal loss, or other hardships, and how they coped with them?",
        "What advice would the character give to others who aspire to follow a similar path or achieve similar success?",
        "Is there anything else you'd like to add about the character?"
    ]


    # Create a new window to display the interview
    interview_window = tk.Toplevel(non_fiction_window)
    interview_window.title("Non-Fiction Character interview")

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

    # Create Begin interview button
    begin_interview_button = tk.Button(window, text="Main Character interview", command=lambda: interview_nfcharacter(interview_window, character_id))
    begin_interview_button.grid()

    # Start the tkinter event loop
    window.mainloop()
