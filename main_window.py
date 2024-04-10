import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
import webbrowser
import sys
from definitions.convert_log_to_interview import convert_log_to_interview
from definitions.restore_data import restore_data
from definitions.generate_outlines import generate_outlines
from definitions.upload_samples_window import upload_samples_window
from definitions.generate_book import generate_book
from definitions.generate_screenplay import generate_screenplay
from definitions.load_api_window import load_api_window
from definitions.generate_summary_and_titles import generate_summary_and_titles


# Create the main window
def main_window(root, definitions, logger):
  
    # Initial state of the title
    title_parts = {
        'work_type': ' ',
        'author_name': '  ',
        'work_title': 'Untitled',
        'year': '   '
    }
    # Function to update the title
    def update_title():
        root.title(f"{title_parts['work_type']} - {title_parts['author_name']} - {title_parts['work_title']} - {title_parts['year']}")

    # Update the title initially
    update_title()
    global work_type

    def update_work_type(work_type):
        title_parts['work_type'] = work_type
        update_title()
    def update_author_name(author_name):
        title_parts['author_name'] = author_name
        update_title()
    def update_work_title(work_title):
        title_parts['work_title'] = work_title
        update_title()
    def update_year(year):
        title_parts['year'] = year
        update_title()
        

    # UX elements table:
    # Create a style object
    style = ttk.Style()

    # Configure a style for the buttons
    style.configure('Custom.TButton', font=('Arial', 18, 'bold'))
    
    # Bind title bar motion to root window motion
    def move_window(event):
        root.geometry(f"+{event.x_root}+{event.y_root}")
        title_bar.bind("<B1-Motion>", move_window)
    def on_closing():
        # This function will be called when the 'x' (close) button of the root window is clicked
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            # Close the root window and exit the application
            root.destroy()
            sys.exit()  # Ensure that the application exits completely
            root.protocol("WM_DELETE_WINDOW", on_closing)

    # Get the screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Calculate padding values based on the screen size
    padding_close = int(screen_width * 0.88)  # Adjust the factor (0.88) as needed
    padding_x = int(screen_height * 0.10)  # Adjust the factor (0.10) as needed
    padding_y = int(screen_height * 0.10)  # Adjust the factor (0.10) as needed

    # Configure grid weights
    root.grid_columnconfigure(0, weight=5)  # Give more weight to the title label column
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)  # Second column
    root.grid_rowconfigure(1, weight=3)
    root.grid_columnconfigure(2, weight=1)  # Third column
    root.grid_rowconfigure(2, weight=3)
    root.grid_columnconfigure(3, weight=1)  # Fourth column
    root.grid_rowconfigure(3, weight=3)
    root.grid_columnconfigure(4, weight=1)  # Fifth column
    root.grid_rowconfigure(4, weight=3)
    root.grid_columnconfigure(5, weight=1)  # Sixth column
    root.grid_rowconfigure(5, weight=3)
    root.grid_columnconfigure(6, weight=1)  # Seventh column
    root.grid_rowconfigure(6, weight=3)
    root.grid_columnconfigure(7, weight=1)  # Eighth column
    root.grid_rowconfigure(7, weight=3)
    root.grid_columnconfigure(8, weight=1)  # Ninth column
    root.grid_rowconfigure(8, weight=3)
    root.grid_columnconfigure(9, weight=0)  # Minimal weight for close button column
    root.grid_rowconfigure(9, weight=3)



    # Create custom title bar and disable default title bar
    root.overrideredirect(True)
    title_bar = tk.Frame(root, bg='#a1928c', relief='raised', bd=0)
    title_bar.grid(row=0, column=0, columnspan=10, sticky='new')

    # Add a title label to the title bar
    title_label = tk.Label(title_bar, text='FoolsGold PyWriter', bg='#a1928c', fg='#1f1714', font=('Arial', 20, 'bold'))
    title_label.grid(row=0, column=0, padx=825, pady=1, sticky='w')  # Align left

    # Create the close button
    close_button = tk.Button(title_bar, text='˟', bg='#b03e05', fg='#f5ceba', relief='flat', font=('Arial', 25, 'bold'), command=on_closing)
    close_button.configure(width=3, height=1)
    close_button.grid(row=0, column=9, padx=75, pady=2, sticky='e')  # Align right

    # create a button to select the genre "Fiction"
    def fiction_action():
        from definitions.fiction_window import fiction_window
        fiction_window(root)
        update_work_type("Fiction")

    fiction_button = ttk.Button(root, text="Fiction", style='Custom.TButton', command=fiction_action)
    fiction_button.grid(column=4, columnspan=2, row=1, pady=50)

    # create a button to select the genre "Non-Fiction"
    def non_fiction_action():
        from definitions.non_fiction_window import non_fiction_window
        non_fiction_window(root)
        update_work_type("Non-fiction")

    non_fiction_button = ttk.Button(root, text="Non-Fiction", style='Custom.TButton', command=non_fiction_action)
    non_fiction_button.grid(column=6, row=1, pady=50)

    # create a button to select the genre "biography"
    def biography_action():
        from definitions.biography_window import biography_window
        biography_window(root)
        update_work_type("Biography")

    biography_button = ttk.Button(root, text="Biography", style='Custom.TButton', command=biography_action)
    biography_button.grid(column=7, columnspan=2, row=1, pady=50)

    #create a button to convert the log file to an interview.txt file
    convert_log_button = ttk.Button(root, text="Convert Log to Interview", style='Custom.TButton', command=convert_log_to_interview)
    convert_log_button.grid(column=1, columnspan=3, row=2, padx=50, pady=10)

    #create a button to restore information from a previous session
    restore_button = ttk.Button(root, text="Restore Data", style='Custom.TButton', command=lambda: restore_data(logger))
    restore_button.grid(column=0, columnspan=3, row=1, padx=50, pady=10)

    #create a button to link to a page to tip Alex (sharxbyte) the dev
    tip_button = ttk.Button(root, text="Tip the Dev", style='Custom.TButton', command= lambda: webbrowser.open('https://www.paypal.com/donate/?business=7CC79V49FXXHN&no_recurring=0&item_name=If+my+writing+tool+helped+you+to+get+your+project+off+the+ground%2C+please+consider+donating+to+help+me+pay+my+bills%21+Thanks%21&currency_code=USD'))
    tip_button.grid(column=6, columnspan=2, row=20, padx=50, pady=10)

    #create a button to generate an set of outlines to choose from
    generate_outlines_button = ttk.Button(root, text="Create Outline", style='Custom.TButton', command=generate_outlines)
    generate_outlines_button.grid(column=0, columnspan=3, row=4, padx=50, pady=10)

    # create a window for uploading and analyzing samples
    upload_samples_button = ttk.Button(root, text="Upload Writing Samples", style='Custom.TButton', command=upload_samples_window)
    upload_samples_button.grid(column=1, columnspan=3, row=3, padx=50, pady=10)
    

    # returned summary and title if available
    try:
        summaries, titles = generate_summary_and_titles(root)
    except Exception as e:
        logger.error(f"Error generating summary and titles: {e}")
        summaries = ["Click the button above to generate a summary based on the information provided thus far."]
        titles = ["Untitled"]


    # Display the summary text box
    summary_text = tk.Text(root, height=35, width=160)
    summary_text.grid(column=5, columnspan=3, row=3, padx=10, pady=10, sticky='sw')
    summary_text.insert(tk.END, "\n".join(summaries))  # Display the summaries in the text box

    # create summary window button on the main page
    summary_button = ttk.Button(root, text="Generate a Summary and Title", style='Custom.TButton', command=lambda: generate_summary_and_titles(root))
    summary_button.grid(column=6, row=2, padx=50, pady=10)

    # create a button to generate the book based on the information provided
    generate_book_button = ttk.Button(root, text="Generate Book", style='Custom.TButton', command=generate_book)
    generate_book_button.config(width=20)
    generate_book_button.grid(row=5, column=3, padx=50, pady=10)

    # create a button to generate a screenplay based off the information provided
    generate_screenplay_button = ttk.Button(root, text="Generate Screenplay", style='Custom.TButton', command=generate_screenplay)
    generate_screenplay_button.config(width=20)
    generate_screenplay_button.grid(row=5, column=5, columnspan=2, padx=50)

    # Add a button to call the load_api_window function
    api_key_button = ttk.Button(root, text="Enter API Key", style='Custom.TButton', command=load_api_window)
    api_key_button.grid(column=2, columnspan=2, row=20, padx=10, pady=50)
