# Standard library imports
import os

# Third-party library imports

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk


# Local imports
import importlib
from definitions import *


def add_reference():

    def clear_reference_window():
        for child in reference_window.winfo_children():
            child.destroy()

    def on_select_book(event):
        clear_fields()
        create_field("Author's last name, first name:", 0)
        create_field("Title of book:", 1)
        create_field("Publisher:", 2)
        create_field("Year of publication:", 3)

    def on_select_article(event):
        clear_fields()
        create_field("Author's last name, first name:", 0)
        create_field("Title of article:", 1)
        create_field("Title of periodical:", 2)
        create_field("Volume number:", 3)
        create_field("Issue number:", 4)
        create_field("Year of publication:", 5)
        create_field("Page numbers:", 6)

    def on_select_website(event):
        clear_fields()
        create_field("Author's last name, first name (if available):", 0)
        create_field("Title of webpage:", 1)
        create_field("Name of website:", 2)
        create_field("Publisher or sponsor of website:", 3)
        create_field("Date of publication or last update:", 4)
        create_field("URL:", 5)

    def on_select_other_online_source(event):
        clear_fields()
        create_field("Author's last name, first name (if available):", 0)
        create_field("Title of article or page:", 1)
        create_field("Title of website:", 2)
        create_field("Publisher or sponsor of website:", 3)
        create_field("Date of publication or last update:", 4)
        create_field("URL:", 5)

    def on_select_film(event):
        clear_fields()
        create_field("Title of film:", 0)
        create_field("Director's name:", 1)
        create_field("Studio or distributor:", 2)
        create_field("Year of release:", 3)

    def on_select_tv_show(event):
        clear_fields()
        create_field("Title of episode:", 0)
        create_field("Title of TV series:", 1)
        create_field("Created by Creator's name:", 2)
        create_field("Network:", 3)
        create_field("Original broadcast date:", 4)

    def on_select_visual_art(event):
        clear_fields()
        create_field("Artist's last name, first name:", 0)
        create_field("Title of work:", 1)
        create_field("Year of creation:", 2)
        create_field("Medium:", 3)
        create_field("Name of institution or private collection where work is housed:", 4)

    def clear_fields():
        for child in reference_window.winfo_children():
            if isinstance(child, tk.Entry):
                child.delete(0, tk.END)

    def save_and_add_another():
        # Get the data from the fields and add it to the source table
        data = [field.get() for field in fields]
        source_table.insert("", tk.END, values=data)

        # Clear the fields
        clear_fields()

    def reference_window(character_id):
        # Create a window with dropdowns to add reference information
        reference_window = tk.Toplevel(non_fiction_window)
        reference_window.title("Add Reference")

        # Set window size and position
        screen_width = interview_window.winfo_screenwidth()
        screen_height = interview_window.winfo_screenheight()
        window_width = int(screen_width * 0.5)
        window_height = int(screen_height * 0.5)
        x = int((screen_width - window_width) / 2)
        y = int((screen_height - window_height) / 2)
        interview_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Create cited media type dropdown menu
        media_type_label = ttk.Label(reference_window, text="Cited Media Type:")
        media_type_label.grid(row=0, column=0, padx=5, pady=5)

        media_type_options = ["Books", "Website", "Other Online Source", "Article", "Film", "TV Show", "Visual Art"]
        media_type = tk.StringVar(value=media_type_options[0])
        media_type_dropdown = ttk.Combobox(reference_window, textvariable=media_type, values=media_type_options)
        media_type_dropdown.grid(row=0, column=1, padx=5, pady=5)

        # Define a dictionary that maps each option to its corresponding on_select function
        options_dict = {"Books": on_select_book,
                        "Website": on_select_website,
                        "Other Online Source": on_select_other_online_source,
                        "Article": on_select_article,
                        "Film": on_select_film,
                        "TV Show": on_select_tv_show,
                        "Visual Art": on_select_visual_art}

        # Bind the selected function to the ComboboxSelected event
        media_type_dropdown.bind("<<ComboboxSelected>>", lambda event: options_dict[media_type.get()](event))

        # Create a frame to hold the buttons
        button_frame = tk.Frame(reference_window)
        button_frame.grid(row=8, column=1, columnspan=2, pady=10)

        # Create the Cancel button
        cancel_button = ttk.Button(button_frame, text="Cancel", command=reference_window.destroy)
        cancel_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Create the Confirm button
        confirm_button = ttk.Button(button_frame, text="Save", command=lambda: add_reference_confirm(character_id))
        confirm_button.pack(side=tk.RIGHT, padx=5, pady=5)

        # Create the Save and Add Another button
        save_add_another_button = ttk.Button(button_frame, text="Save and Add Another", command=save_and_add_another)
        save_add_another_button.pack(side=tk.RIGHT, padx=5, pady=5)

        # Start the Tkinter event loop
        reference_window.mainloop()
