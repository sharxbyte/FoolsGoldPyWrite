# Standard library imports
import os
import tkinter as tk
from tkinter import ttk

# Third-party library imports
import openai
from PIL import Image, ImageTk

# Local imports
import importlib
import inspect

# define function to generate summaries and titles
def generate_summary_and_titles(summary_window):
    interview_file = "interview.txt"
    outline_file = "outline.txt"


    # Check if the interview and outline files exist
    if not os.path.isfile(interview_file) or not os.path.isfile(outline_file):
        print("Interview file or outline file not found.")
        return ["Click the button above to generate a summary based on the information provided thus far"], ["No titles generated yet. Please click the button above."]
    
    with open(interview_file, "r") as f_interview, open(outline_file, "r") as f_outline:
        interview = f_interview.read()
        outline = f_outline.read()
        
        show_api_warning(main_window)

        # Generate summaries using GPT API
    with open(outline_file, "r") as f:
        outline = f.read()

    with open(interview_file, "r") as f:
        interview = f.read()

    prompt = (f"Based on this interview, please write a summary of the story. The summary should include the following plot points:\n\n{outline}\n\nPlease limit your summary to 5 paragraphs or 250 words maximum. The summary should be organized with the plot points in mind, hitting the main plot points and giving an accurate and entertaining narrative of the events and characters described in the interview.txt file.\n\n{interview}\n\n")
    completions = openai.Completion.create(engine="davinci", prompt=prompt, max_tokens=1800, n=1, stop=None, temperature=0.5)

    # Parse summary and title choices from API response
    summaries = []
    titles = []
    for choice in completions.choices:
        if choice.text.startswith("Summary:"):
            summary = choice.text.replace("Summary:", "").strip()
            summaries.append(summary)
        elif choice.text.startswith("Title:"):
            title = choice.text.replace("Title:", "").strip()
            titles.append(title)

    if not summaries: # If summaries list is empty
        summaries = ["Click the button above to generate a summary based on the information provided thus far"]

    if not titles: # If titles list is empty
        titles = ["No titles generated yet. Please click the button above."]
 
    # Display summaries
    summary_label = ttk.Label(summary_window, text="Select a summary:")
    summary_label.grid(column=0, row=0, padx=10, pady=10, sticky="w")
    selected_summary = tk.StringVar()
    for i, summary in enumerate(summaries):
        summary_radio = ttk.Radiobutton(summary_window, text=summary, variable=selected_summary, value=summary)
        summary_radio.grid(column=0, row=i+1, padx=10, pady=5, sticky="w")

    # Display titles
    title_label = ttk.Label(summary_window, text="Choose a title or enter a custom one:")
    title_label.grid(column=0, row=len(titles)+1, padx=10, pady=10, sticky="w")
    title_text = tk.Entry(summary_window, width=50)
    title_text.grid(column=0, row=len(titles)+2, padx=10, pady=10, sticky="w")
    for i, title in enumerate(titles):
        title_label = ttk.Label(summary_window, text=title)
        title_label.grid(column=0, row=len(summaries)+3+i, padx=10, pady=5, sticky="w")

    return summaries, titles
