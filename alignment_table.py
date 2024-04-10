# Standard library imports
import os
import tkinter as tk

# Third-party library imports
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk

# Local imports
import importlib
from definitions import *

def alignment_table():
    #Create a grid of check boxes for alignment
    alignment_frame = tk.Frame(interview_window)
    alignment_frame.grid(row=3, column=0, padx=25, pady=10, sticky="W")

    alignment_label = tk.Label(alignment_frame, text="Alignment:")
    alignment_label.grid(row=0, column=0)

    alignment_options = [("Good", "G"), ("Neutral", "N"), ("Evil", "E")]
    alignment_vars = {}
    for i, (option, code) in enumerate(alignment_options):
        alignment_vars[code] = tk.BooleanVar(value=False)
        alignment_check = tk.Checkbutton(alignment_frame, text=option, variable=alignment_vars[code])
        alignment_check.grid(row=0, column=i+1)

    #Define a function to update the alignment label
    def update_alignment_label():
        alignment = ""
        if alignment_vars["G"].get():
            alignment += "Good "
        elif alignment_vars["N"].get():
            alignment += "Neutral "
        elif alignment_vars["E"].get():
            alignment += "Evil "

        if alignment_vars["L"].get():
            alignment += "Lawful"
        elif alignment_vars["TN"].get():
            alignment += "True Neutral"
        elif alignment_vars["C"].get():
            alignment += "Chaotic"

        alignment_label.config(text=f"Alignment: {alignment}")

    #Create a grid of check boxes for morality
    morality_frame = tk.Frame(interview_window)
    morality_frame.grid(row=4, column=0, padx=25, pady=10, sticky="W")

    morality_label = tk.Label(morality_frame, text="Morality:")
    morality_label.grid(row=0, column=0)

    morality_options = [("Lawful", "L"), ("True Neutral", "TN"), ("Chaotic", "C")]
    morality_vars = {}
    for i, (option, code) in enumerate(morality_options):
        morality_vars[code] = tk.BooleanVar(value=False)
        morality_check = tk.Checkbutton(morality_frame, text=option, variable=morality_vars[code])
        morality_check.grid(row=0, column=i+1)

    # Define a function to update the morality label
    def update_morality_label():
        morality = ""
        if morality_vars["L"].get():
            morality += "Lawful "
        elif morality_vars["TN"].get():
            morality += "True Neutral "
        elif morality_vars["C"].get():
            morality += "Chaotic "

        if morality_vars["G"].get():
            morality += "Good"
        elif morality_vars["N"].get():
            morality += "Neutral"
        elif morality_vars["E"].get():
            morality += "Evil"

        morality_label.config(text=f"Morality: {morality}")

    # Bind the check boxes to their update functions
    for var in alignment_vars.values():
        var.trace("w", lambda *args: update_alignment_label())

    for var in morality_vars.values():
        var.trace("w", lambda *args: update_morality_label())

    # Create the labels for the alignment/morality definitions
alignment_definitions = {("LG", "A lawful good character acts as a good person is expected or required to act. He combines a commitment to oppose evil with the discipline to fight relentlessly. He tells the truth, keeps his word, helps those in need, and speaks out against injustice. A lawful good character hates to see the guilty go unpunished."),
        ("NG", "A neutral good character does the best that a good person can do. He is devoted to helping others. He works with kings and magistrates but does not feel beholden to them."),
        ("CG", "A chaotic good character acts as his conscience directs him with little regard for what others expect of him. He makes his own way, but he's kind and benevolent. He believes in goodness and right but has little use for laws and regulations. He hates it when people try to intimidate others and tell them what to do."),
        ("LN", "A lawful neutral character is directed by honor and tradition. He believes in order and obedience to authority. He may believe in personal order and live by a code or standard, or he may believe in order for all and favor a strong, organized government."),
        ("TN", "A neutral character does what seems to be a good idea. He doesn't feel strongly one way or the other when it comes to good vs. evil or law vs. chaos. Most neutral characters exhibit a lack of conviction or bias rather than a commitment to neutrality. Such a character thinks of good as better than evil after all, he would rather have good neighbors and rulers than evil ones. Still, he's not personally committed to upholding good in any abstract or universal way."),
        ("CN", "A chaotic neutral character follows his whims. He is an individualist first and last. He values his own liberty but doesn't strive to protect others' freedom. He avoids authority, resents restrictions, and challenges traditions. A chaotic neutral character does not intentionally disrupt organizations as part of a campaign of anarchy. To do so, he would have to be motivated either by good (and a desire to liberate others) or evil (and a desire to make those different from himself suffer)."),
        ("LE", "A lawful evil villain methodically takes what he wants within the limits of his code of conduct without regard for whom it hurts. He cares about tradition, loyalty, and order but not about freedom, dignity, or life. He plays by the rules but without mercy or compassion. He is comfortable in a hierarchy and would like to rule, but is willing to serve. He condemns others not according to their actions but according to race, religion, homeland, or social rank. He is loath to break laws or promises."),
        ("NE", "A neutral evil villain does whatever she can get away with. She is out for herself, pure and simple. She sheds no tears for those she kills, whether for profit, sport, or convenience. She has no love of order and holds no illusion that following laws, traditions, or codes would make her any better or more noble. On the other hand, she doesn't have the restless nature or love of conflict that a chaotic evil villain has."),
        ("CE", "A chaotic evil character does what his greed, hatred, and lust for destruction drive him to do. He is hot-tempered, vicious, arbitrarily violent, and unpredictable. If he is simply out for whatever he can get, he is ruthless and brutal. If he is committed to the spread of evil and chaos, he is even more dangerous. A chaotic evil character will do anything to get what he wants, and feels no compunctions about hurting those who stand in his way. He values his own freedom above everything else, and will do whatever it takes to preserve it.")
    }
