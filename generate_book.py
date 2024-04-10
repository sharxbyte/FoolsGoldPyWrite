# Standard library imports
import os
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

# Third-party library imports
import openai
from PIL import Image, ImageTk

# Local imports
import importlib
import inspect
from definitions import *

def generate_book():
    # load interview from file
    with open("interview.txt", "r") as f:
        interview = f.read()
    
    # load outline from file
    with open("outline.txt", "r") as f:
        outline = f.read()
        
    # read author style from file
    with open("author_style.txt", "r") as f:
        author_style = f.read()

    # combine interview, outline, and author style to create prompt
    prompt = f"Based on the following interview, outline, and author style, write a book that captures the spirit and themes of the interview and adheres to the outline. Make sure to use the provided information and only the provided information. Your book should be engaging, informative, and consistent with the author's style.\n\nINTERVIEW:\n{interview}\n\nOUTLINE:\n{outline}\n\nAUTHOR STYLE:\n{author_style}\n\nPlease write a {work_type.lower()} book that follows a logical timeline, so that events take place in order, except when describing a flashback or similar memory. As you write, keep in mind the following tips: \n\n- Focus on creating a compelling story arc that will keep readers engaged from beginning to end. \n\n- Develop interesting and relatable characters that readers will care about. \n\n- Use vivid and descriptive language to paint a picture of the world you are creating. \n\n- Show, don't tell. Use scenes and dialogue to advance the plot and reveal character. \n\n- Be sure to proofread your work carefully and ensure that it flows smoothly and makes sense. \n\nWhen you're ready to begin, start writing below: \n"

    # initialize book and remaining length
    generated_book = ""
    remaining_length = max_length

    with open("selected_title.txt", "a") as f:
        while True:
            # generate next part
            next_part = openai.Completion.create(
                engine="selected_model",
                prompt=prompt,
                max_tokens=remaining_length,
                temperature=0.7,
                n_gen=1,
                stop=None,
            ).choices[0].text.strip()

            # find closest paragraph to remaining length
            paragraphs = next_part.split("\n\n")
            closest_paragraph = ""
            for paragraph in paragraphs:
                if len(paragraph) <= remaining_length:
                    closest_paragraph = paragraph
                else:
                    break

            # add closest paragraph to book
            generated_book += closest_paragraph

            # subtract length of closest paragraph from remaining length
            remaining_length -= len(closest_paragraph)

            # check if book generation is complete
            if remaining_length < 250:
                break

            # write generated book to file
            f.write(generated_book)
            f.write("\n")

            # prompt author to continue or stop
            prompt = input("Press enter to continue generating or type 'stop' to finish book generation\n")
            if prompt.lower() == "stop":
                break

        # write final generated book to file
        f.write(generated_book)
        f.write("\n")

    # output book
    print("Generated book:")
    print(generated_book)
