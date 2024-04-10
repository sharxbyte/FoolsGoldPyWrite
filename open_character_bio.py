# Standard library imports
import logging
import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog

# Third-party library imports
from PIL import Image, ImageTk
import tkinter.scrolledtext as tkst

# Local imports
import importlib

def open_character_bio(event):
    # Get the clicked table widget
    clicked_table = event.widget

    # Get the selected item from the clicked table
    selected_item = clicked_table.selection()

    logger.setLevel(logging.CRITICAL)  # Disable logging

    if selected_item:
        # Get the character ID from the selected item
        character_id = clicked_table.item(selected_item, "values")[1]

        # Get the character information from the dictionary
        character_info = get_character_info(character_id)

        # Create a new window to display the character bio
        character_window = tk.Toplevel()
        character_window.title(f"{character_info['name']} ({character_info['character_id']})")

        # Create a button to resume the interview
        resume_interview_button = ttk.Button(character_window, text="Resume Interview", command=lambda: resume_interview(character_id))
        resume_interview_button.grid(side="bottom", pady=10)

        # Center the window on the screen
        screen_width = character_window.winfo_screenwidth()
        screen_height = character_window.winfo_screenheight()
        window_width = character_window.winfo_reqwidth()
        window_height = character_window.winfo_reqheight()
        x = int((screen_width / 2) - (window_width / 2))
        y = int((screen_height / 2) - (window_height / 2))
        character_window.geometry(f"+{x}+{y}")

        # Create labels and editable text entries for each piece of character information
        row = 0
        for key, value in character_info.items():
            if key == 'character_id':
                continue

            label = ttk.Label(character_window, text=f"{key.capitalize()}:")
            label.grid(column=0, row=row, padx=10, pady=10, sticky="w")

            if key == 'narrator':
                narrator_var = tk.BooleanVar()
                narrator_var.set(value)
                entry = ttk.Checkbutton(character_window, text="Is this character a narrator?", variable=narrator_var)
            else:
                entry = ttk.Entry(character_window)
                entry.insert(0, value)

            entry.grid(column=1, row=row, padx=10, pady=10)
            row += 1

        # Create a scrolling text box for the character bio
        bio_text = tkst.ScrolledText(character_window, wrap="word", height=20, font=("Arial", 12))
        bio_text.grid(row=row, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        # Add the remaining character information to the text box
        for key, value in character_info.items():
            if key in ['name', 'age', 'species', 'gender', 'physical description', 'sexuality', 'job title', 'personality type', 'narrator']:
                continue
            if key == 'narrator_check':
                if value:
                    bio_text.insert(tk.END, "- Is this character a narrator? Yes\n")
                else:
                    bio_text.insert(tk.END, "- Is this character a narrator? No\n")
            else:
                bio_text.insert(tk.END, f"- {key.capitalize()}: {value}\n")

        # Add the alignment label
        alignment_label = ttk.Label(character_window, text="Alignment:")
        alignment_label.grid(column=0, row=row + 1, padx=10, pady=10, sticky="w")

        # Create an entry for alignment
        alignment_entry = ttk.Entry(character_window)
        alignment_entry.insert(0, character_info.get("alignment", ""))
        alignment_entry.grid(column=1, row=row + 1, padx=10, pady=10)

        # Create a new frame to hold the buttons
        button_frame = ttk.Frame(character_window)
        button_frame.grid(row=row + 2, column=0, columnspan=2, pady=10)

        # Add a "Save" button to the frame
        save_button = ttk.Button(button_frame, text="Save Character", command=lambda: save_details(character_id, character_text_box.get("1.0", tk.END)))
        save_button.grid(row=0, column=0, padx=5, pady=10)

        # Add a "Cancel" button to the frame
        cancel_button = ttk.Button(button_frame, text="Cancel", command=character_window.destroy)
        cancel_button.grid(row=0, column=1, padx=5, pady=10)

        logger.setLevel(logging.INFO)  # Enable logging again
