# Standard library imports
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

# Third-party library imports
from tkinter import messagebox
from tkinter import simpledialog

def fiction_window(root, logger):
    fiction_window = tk.Toplevel(root)
    fiction_window.title("Fiction Project")

    # Log opening of fiction window
    logger.info("Fiction window opened")

    # Function to create a table
    def create_table(parent, columns):
        tree = ttk.Treeview(parent, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col.title())
        tree.pack(side=tk.LEFT)

        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tree.configure(yscrollcommand=scrollbar.set)

        return tree

    # Function to create a text box
    def create_textbox(parent, title, default_value):
        label = tk.Label(parent, text=title)
        text_box = tk.Text(parent, height=10)
        text_box.insert(tk.END, default_value)
        label.pack(pady=10)
        text_box.pack()

        def get_value():
            return text_box.get("1.0", tk.END)

        return get_value

    # Create Character table
    fcharacter = create_table(fiction_window, ("Name", "ID"))

    # Create Topic Details table
    ftopic_details = create_table(fiction_window, ("Name", "ID"))

    # Create Reference Table
    fadd_reference = create_table(fiction_window, ("Name", "ID"))

    # Bind checkbox selection to delete button
    def delete_selected(table):
        selected_items = table.selection()
        for item in selected_items:
            table.delete(item)

    fdelete_button = ttk.Button(fiction_window, text="Delete Selected", command=lambda: delete_selected(fcharacter))
    fdelete_button.pack(pady=10)

    # Bind the open_character_bio function to item selection for each table
    # (Implement open_character_bio, open_topic_details, open_reference_info functions)
    # fcharacter.bind("<<TreeviewSelect>>", lambda event: open_character_bio(event, logger))
    # ftopic_details.bind("<<TreeviewSelect>>", lambda event: open_topic_details(event, logger))
    # fadd_reference.bind("<<TreeviewSelect>>", lambda event: open_reference_info(event, logger))

    # Create text boxes
    fsetting_textbox = create_textbox(fiction_window, "Setting:", "")
    fhistime_textbox = create_textbox(fiction_window, "History and Background Information:", "")
    fplot_textbox = create_textbox(fiction_window, "Plot:", "")

    # Start the Tkinter event loop for the fiction window
    fiction_window.mainloop()

# This function can be called from another module where root and logger are defined
# fiction_window(root, logger)
