# Standard library imports
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

# Third-party library imports
from tkinter import messagebox
from tkinter import simpledialog

def biography_window(root, logger):
    biography_window = tk.Toplevel(root)
    biography_window.title("Biography Project")

    # Log opening of biography window
    logger.info("Biography window opened")

    def create_table(parent, columns):
        tree = ttk.Treeview(parent, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col.title())
        tree.pack(side=tk.LEFT)

        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tree.configure(yscrollcommand=scrollbar.set)

        return tree

    def create_textbox(parent, title, default_value):
        label = tk.Label(parent, text=title)
        text_box = tk.Text(parent, height=10)
        text_box.insert(tk.END, default_value)
        label.pack(pady=10)
        text_box.pack()

        def get_value():
            return text_box.get("1.0", tk.END)

        return get_value

    # Create Main Character table
    biomain_character = create_table(biography_window, ("Name", "ID"))

    # Create Secondary Character table
    biosec_character = create_table(biography_window, ("Name", "ID"))

    # Create Antagonist Character Table
    bioant_character = create_table(biography_window, ("Name", "ID"))

    # Create text boxes
    biosetting_textbox = create_textbox(biography_window, "Setting:", "")
    biohistime_textbox = create_textbox(biography_window, "History and Background Information:", "")
    bioplot_textbox = create_textbox(biography_window, "Plot:", "")

    # Start the Tkinter event loop for the biography window
    biography_window.mainloop()

# This function can be called from another module where root and logger are defined
# biography_window(root, logger)
