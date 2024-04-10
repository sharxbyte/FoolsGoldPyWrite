import tkinter as tk
from tkinter import ttk

class StyleManager:
    def __init__(self, root):
        self.root = root
        self.screen_width = root.winfo_screenwidth()
        self.screen_height = root.winfo_screenheight()
        self.style = ttk.Style()
        self.configure_styles()

    def configure_styles(self):
        # Set the theme
        self.style.theme_use("default")

        # Set the background color for all widgets
        self.style.configure('.', background='#f4ecdf')

        # Set the foreground and highlight colors for all widgets
        self.style.configure('.', foreground='#1f1714', highlightcolor='#1f1714')
        self.style.map('.', foreground=[('disabled', '#a1928c'), ('pressed', '#f4ecdf'), ('active', '#f4ecdf')])

        # Set the scrollbar colors
        self.style.configure('TScrollbar', background='#d9d0bf', troughcolor='#f4ecdf', bordercolor='#f4ecdf')

        # Set the title bar colors
        self.style.configure('TFrame', background='#a1928c')

        # Set the text colors
        self.style.configure('TText', foreground='#1f1714')

        # Calculate proportional font size and padding for buttons
        button_font_size = int(min(self.screen_width, self.screen_height) * 0.015)
        button_padding = int(min(self.screen_width, self.screen_height) * 0.015)

        # Set the button style
        self.style.configure('TButton', font=('Arial', button_font_size), padding=button_padding,
                             foreground='#1f1714', background='#d9d0bf', 
                             activebackground='#a1928c', highlightthickness=0)
        self.style.map('TButton', background=[('active', '#a1928c'), ('disabled', '#f4ecdf'), ('pressed', '#f4ecdf')])

        # Set the entry colors
        self.style.configure('TEntry', foreground='#1f1714', fieldbackground='#f4ecdf', selectbackground='#a1928c')
