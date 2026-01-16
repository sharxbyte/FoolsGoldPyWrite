"""
PyWriter Complete
-----------------

This script builds upon the initial PyWriter prototype by adding a more
comprehensive set of interview options, distraction‑free mode, and
optional hands‑free input/output.  It supports four project types –
fiction, non‑fiction, biography (auto‑biographical), and screenplay –
each with tailored questionnaires for characters, settings, timelines
and topics.  An embedded notebook view organises your work into
separate tabs so that you can easily reference and edit each element.

Voice features are implemented using two optional third‑party
libraries: `pyttsx3` for text‑to‑speech and `speech_recognition` for
speech‑to‑text.  If these libraries are not available, the buttons
for speaking and listening will alert the user to install them.

The distraction‑free mode toggles the main window into full screen,
minimising UI clutter.  Saving and loading uses a JSON file to
preserve structure along with a human‑readable text backup.  A
simple logging mechanism writes activity to a log file in the
project directory whenever a project is saved or loaded.

Usage:
    python3 pywriter_complete.py

Dependencies:
    - Python 3.9 or newer with Tkinter.
    - Optional: pyttsx3 (for text‑to‑speech) – install via
          pip install pyttsx3
    - Optional: SpeechRecognition and a recogniser backend like Vosk
      or PocketSphinx (for speech‑to‑text) – install via
          pip install SpeechRecognition
      plus one of the extra packages listed in the SpeechRecognition
      documentation (e.g. SpeechRecognition[vosk]).

Note: This script is intended to demonstrate key features and
architecture.  It does not implement every possible question from
the provided files; however, it lays out the structure for adding
more in the future.
"""

import json
import logging
import os
import sys
import platform
import importlib
import importlib.util
import importlib.metadata
import webbrowser
import uuid
import datetime
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
from typing import Dict, List, Optional, Callable, Any, Set
import threading

# -----------------------------------------------------------------------------
# Dependency detection
#
# The application uses optional third‑party libraries for text‑to‑speech (pyttsx3),
# speech recognition (speech_recognition) and image handling (Pillow).  These
# imports are wrapped in a central audit so that missing dependencies never
# produce unhandled ImportErrors on import.  Hard requirements are checked
# during startup and the application exits gracefully if they are unavailable.

# Attempt to import voice libraries.  We defer creating engines until we
# validate dependencies in PyWriterAdvanced.
try:
    import pyttsx3  # type: ignore
except Exception:
    pyttsx3 = None  # type: ignore

try:
    import speech_recognition as sr  # type: ignore
except Exception:
    sr = None  # type: ignore

try:
    from PIL import Image, ImageTk  # type: ignore
except Exception:
    Image = None  # type: ignore
    ImageTk = None  # type: ignore

# Globals for voice engines; initialised after dependency audit
tts_engine: Optional[Any] = None  # pyttsx3.Engine
recognizer: Optional[Any] = None  # speech_recognition.Recognizer
microphone: Optional[Any] = None  # speech_recognition.Microphone

# -----------------------------------------------------------------------------
# Question packs
#
# To provide comprehensive and tailored interviews for each project type, the
# application embeds a set of default question packs directly in the code.  Each
# project type (Fiction, Non-Fiction, Biography) defines question lists for
# characters, settings, history/timeline and topics.  These lists are designed
# to cover a broad range of story elements, research considerations and
# biographical details.  Duplicate prompts are avoided and questions are
# phrased generically so that they can be reused across different projects.  If
# future versions support loading external packs, these defaults will act as a
# fallback.

# Each list contains eight or more prompts to ensure sufficient depth of
# interrogation.  Additional categories such as arcs, conflicts, themes and
# relationships are folded into the existing four categories to avoid expanding
# the UI at this stage.

QUESTION_PACKS: Dict[str, Dict[str, List[str]]] = {
    "Fiction": {
        # Character interviews focus on detailed, narrative prompts covering identity,
        # appearance, personality, motivations, relationships and growth.  Each list
        # contains fifteen questions for comprehensive coverage.
        "characters": [
            "What is the character’s full name and nickname?",
            "What is their role or occupation in the story?",
            "Please describe the character’s physical appearance, including height, build, hair, clothing and any distinguishing features.",
            "What is the character’s age, origin and family background?",
            "What are the character’s personality traits, strengths and weaknesses?",
            "What motivates the character and what are their goals?",
            "What skills or talents does the character possess?",
            "What fears or vulnerabilities affect them?",
            "How does the character relate to other main characters?",
            "What internal conflicts or secrets do they struggle with?",
            "How does the character’s past influence their present actions?",
            "What external conflicts does the character face throughout the story?",
            "How does the character grow or change by the end of the story?",
            "What relationships are most important to this character and why?",
            "What obstacles stand between the character and their goals?"
        ],
        # Settings interviews include a scale qualifier and detailed inquiries into
        # environment, society, politics, economy, technology and hazards.  Question 2
        # asks about scale (single town vs multiple locations); if the answer
        # indicates a single location, the next question (planet/universe) may be
        # skipped by the dynamic interview logic.
        "settings": [
            "What is the primary location’s name or description?",
            "Does the story take place in a single village/town/city, multiple locations, or across worlds?",
            "If the story spans multiple places or worlds, please describe the overarching planet, country or universe.",
            "What type of environment is it (urban, rural, natural, alien, etc.)?",
            "Describe the physical landscape and notable landmarks.",
            "What social and cultural climate defines this place?",
            "What economic or resource conditions exist here?",
            "Who governs or controls this place? Describe the political structure.",
            "What is the level of technology or magic present?",
            "What traditions, customs or laws influence life here?",
            "How is this location important to the story?",
            "What key events occur here within the story?",
            "Who or what lives here? Describe the species or inhabitants.",
            "Describe the typical weather, climate or other environmental conditions.",
            "What dangers, conflicts or hazards does this place present to the characters?"
        ],
        # History/timeline interviews begin with a qualifier about linear vs time‑travel
        # narratives.  If the answer indicates a single linear timeline, the time
        # travel question (index 10) may be skipped.  The remaining questions
        # guide the author through major events, consequences, turning points and
        # thematic reflections.
        "history": [
            "Does the story follow a single linear timeline or involve time travel or multiple timelines?",
            "Describe the first major event or catalyst in the story and its circumstances.",
            "Who is involved in this event and how do they react?",
            "What are the immediate and long-term consequences of this event?",
            "Describe the second major event or turning point.",
            "What leads up to this second event, and how is it connected to the first?",
            "Who is involved in the second event and what conflicts arise?",
            "What are the outcomes or resolutions of the second event?",
            "How does the timeline progress from these events toward the climax?",
            "What flashbacks, time-travel elements or alternate timelines influence these events?",
            "What is the climax of the story and why is it significant?",
            "How are loose ends and subplots resolved?",
            "How do these events affect the arcs of major characters?",
            "What themes are reflected through these timeline events?",
            "What is the final resolution and how does the story conclude?"
        ],
        # Topic interviews outline the overarching narrative: theme, plot, conflict,
        # turning points, subplots and thematic devices.  They help authors
        # articulate the structure and emotional impact of their stories.
        "topics": [
            "What is the overarching theme or message of your story?",
            "Summarize the main plot or central narrative.",
            "What is the inciting incident that sets the story in motion?",
            "What primary conflict drives the story forward?",
            "What are the major turning points or plot twists?",
            "Describe the climax or peak of tension.",
            "How is the primary conflict resolved?",
            "What subplots or secondary storylines intertwine with the main plot?",
            "How do the subplots complement or contrast with the main story?",
            "What secondary conflicts arise and how are they resolved?",
            "How do characters’ arcs intersect with the main plot?",
            "What themes or messages are explored through the story’s events?",
            "What symbolism or motifs recur throughout the story?",
            "How does the story’s resolution provide closure or open possibilities?",
            "What emotions or reactions do you want readers to experience?"
        ]
    },
    "Non-Fiction": {
        # Stakeholder interviews gather detailed profiles of people involved in the
        # topic: roles, expertise, biases, contributions, relationships and
        # influences.  Fifteen questions encourage a well-rounded analysis.
        "characters": [
            "Who are the key individuals or stakeholders related to this topic?",
            "What roles or responsibilities does each person have?",
            "What is each person’s expertise or background relevant to the topic?",
            "What perspective or bias might each individual bring to the narrative?",
            "How has each person contributed to the development of the topic?",
            "What conflicts of interest or controversies surround these individuals?",
            "In what ways have these people influenced the outcome or public perception of the topic?",
            "What relationships exist among these stakeholders?",
            "How do these individuals communicate or collaborate?",
            "What challenges do these individuals face within the topic’s context?",
            "How do these people’s experiences illustrate broader patterns or trends?",
            "How does the involvement of each person progress over time?",
            "Are there opposing or supporting coalitions among the stakeholders?",
            "How have personal values or ethics shaped their actions?",
            "What impact will these individuals have on the future of the topic?"
        ],
        # Setting interviews identify the environmental, cultural, economic and political
        # context of the non-fiction topic.  Fifteen questions unpack how place
        # and time influence the subject.
        "settings": [
            "What is the primary geographical or institutional setting for this topic?",
            "What cultural or societal factors influence this setting?",
            "What time period or era does this topic occur in?",
            "How does the historical context shape the topic’s development?",
            "What physical characteristics of the setting are relevant (e.g., climate, urban/rural)?",
            "What economic or resource conditions affect the topic?",
            "Who controls or governs the setting and what political structures are involved?",
            "What technological or infrastructural factors are significant?",
            "What traditions, customs or laws shape the context?",
            "How does this setting impact the stakeholders or subject of the topic?",
            "Are there notable events or incidents associated with the setting?",
            "How has the setting changed over time?",
            "Are there regional variations or comparative contexts that matter?",
            "What external environments or settings interact with this primary setting?",
            "How does the setting enhance or constrain the topic's evolution?"
        ],
        # History interviews map the chronological development of the topic: key
        # events, participants, controversies and consequences.  Fifteen
        # questions guide authors through a comprehensive timeline analysis.
        "history": [
            "What is the earliest relevant event or milestone for this topic?",
            "When did this event occur, and what circumstances led to it?",
            "Who were the key players involved in this event?",
            "What were the immediate outcomes or consequences?",
            "What other significant events followed, and how are they linked?",
            "Who participated in the subsequent events and how did their roles evolve?",
            "What evidence and sources support accounts of these events?",
            "What controversies, debates or differing interpretations exist?",
            "How have these events influenced the current state of the topic?",
            "How does the timeline progress toward the present situation?",
            "What turning points or critical decisions changed the topic’s direction?",
            "How have the events impacted the stakeholders and society at large?",
            "What narratives or themes emerge from these historical events?",
            "How are the causes and effects interconnected across the timeline?",
            "What unresolved questions or debates persist about the topic’s history?"
        ],
        # Topic interviews examine the purpose, structure, arguments, evidence and
        # implications of the non-fiction subject.  Fifteen questions ensure
        # thorough coverage of analytical and contextual aspects.
        "topics": [
            "What is the exact title or subject of this topic?",
            "What is the purpose or objective of exploring this topic?",
            "What key questions does this topic seek to answer?",
            "What are the main arguments or claims presented?",
            "What evidence or data supports each claim?",
            "What counterarguments or alternative viewpoints exist?",
            "Who is the target audience and why is this topic relevant to them?",
            "How is the topic structured or organized (outline)?",
            "What methodologies or approaches are used to investigate the topic?",
            "How does this topic relate to broader themes or disciplines?",
            "What historical background informs the topic?",
            "How do current events or recent developments affect the topic?",
            "What ethical, social or political considerations arise?",
            "How might this topic influence future research, policy or practice?",
            "What conclusions or recommendations can be drawn?"
        ]
    },
    "Biography": {
        # Biography character interviews chronicle a person’s identity, background,
        # achievements, challenges and legacy.  These questions are ordered to
        # follow the arc of a life story.
        "characters": [
            "What is the person’s full name (including any titles or nicknames)?",
            "When and where were they born?",
            "What was their family background and early upbringing like?",
            "What were their formative experiences during childhood?",
            "What education and training did they receive?",
            "What were their early careers or first notable accomplishments?",
            "What are the significant achievements or contributions they are known for?",
            "What personal or professional challenges did they face?",
            "How did they respond to and overcome these challenges?",
            "What relationships (family, mentors, allies) were most influential?",
            "What controversies or conflicts surrounded their life?",
            "What personal qualities or values defined them?",
            "How did their work impact society or their field?",
            "What were their later years like and how did their views evolve?",
            "What legacy did they leave and how are they remembered today?"
        ],
        # Biography settings explore the places and contexts shaping a person’s life.
        "settings": [
            "What geographical places were central to this person’s life?",
            "What historical periods did they live through, and how did these shape them?",
            "How did cultural or societal norms influence their choices?",
            "What economic or political conditions affected their opportunities?",
            "What institutions or organizations were significant in their life?",
            "How did the environments they lived in change over time?",
            "What social or community contexts were they a part of?",
            "How did travel or migration impact their life story?",
            "How did their surroundings influence their worldview?",
            "How did the places they lived reflect or contrast with the story's broader themes?",
            "Were there any key locations where turning points occurred?",
            "What were the conditions of these locations (climate, resources)?",
            "How did the person interact with or shape these environments?",
            "How are these locations remembered or preserved today?",
            "What symbolic or emotional significance did these places hold?"
        ],
        # Biography history lists significant events in chronological order and
        # examines their causes, participants and consequences.
        "history": [
            "What are the major events in this person’s life (chronological)?",
            "At what age or stage did each event occur?",
            "What circumstances or choices led up to each event?",
            "Who else was involved or affected by these events?",
            "What were the immediate results of each event?",
            "What long-term effects did each event have on the person and others?",
            "What lessons or changes came from these experiences?",
            "How were these events perceived by society at the time?",
            "What were the public or historical significance of these events?",
            "How did the person’s responses shape their trajectory?",
            "What patterns or themes appear across these events?",
            "How did the person’s personal history intersect with larger historical forces?",
            "What contradictions or surprising turns did their life take?",
            "What unresolved questions or mysteries remain about their life?",
            "How does the timeline of their life inform their legacy?"
        ],
        # Biography topics explore relationships, influences and social dynamics.
        "topics": [
            "Who were the key relationships in the person's life (family, friends, mentors)?",
            "How did their family background influence their development?",
            "What friendships shaped their character or choices?",
            "Who were their professional partners or adversaries?",
            "How did romantic relationships affect their personal and professional life?",
            "What mentors guided their growth and decisions?",
            "Did they mentor others and how?",
            "How did their relationships evolve over time?",
            "What conflicts or alliances defined their social interactions?",
            "How did public perception shape these relationships?",
            "What values or lessons did they impart to others?",
            "How did the person’s social network influence their legacy?",
            "Were there notable betrayals or reconciliations?",
            "How did their relationships reflect the cultural norms of their time?",
            "What overarching narrative or theme emerges from their relationships?"
        ]
    }
}



def parse_fiction_questions(path: str) -> Dict[str, List[str]]:
    """Parse fiction and auto‑biographical questions from questions.txt.

    Returns a dictionary with keys 'Fiction' and 'Biography', each
    containing a list of unique questions.  Duplicate questions and
    empty strings are discarded.  If the file does not exist or
    parsing fails, an empty dict is returned.
    """
    sections: Dict[str, List[str]] = {"Fiction": [], "Biography": []}
    if not os.path.isfile(path):
        return sections
    current: Optional[str] = None
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        # Detect section headings: a line of underscores followed by a title
        if line == "_____":
            # Next non‑blank line is the section name
            j = i + 1
            while j < len(lines) and not lines[j].strip():
                j += 1
            if j < len(lines):
                name = lines[j].strip()
                if name.lower().startswith("fiction"):
                    current = "Fiction"
                elif "bio" in name.lower() or "auto" in name.lower():
                    current = "Biography"
                else:
                    current = None
            i = j
        elif current and line.startswith("\""):
            # Extract question text between quotes
            q = line.strip().strip(",")
            q = q.strip('"')
            if q and q not in sections[current]:
                sections[current].append(q)
        i += 1
    return sections


def parse_nonfiction_questions(path: str) -> List[str]:
    """Extract question list from Non-Fiction Topic Interview file.

    Searches for a list named 'questions' in the python source and
    returns its elements.  If parsing fails or file is missing,
    returns an empty list.
    """
    if not os.path.isfile(path):
        return []
    questions: List[str] = []
    reading = False
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            stripped = line.strip()
            if stripped.startswith("questions = ["):
                reading = True
                # Remove bracket
                stripped = stripped[len("questions = ["):]
            if reading:
                # Remove trailing brackets or commas
                if stripped.endswith("]"):
                    stripped = stripped[:-1]
                    reading = False
                # Remove trailing comma
                stripped = stripped.rstrip(',')
                # Remove quotes
                stripped = stripped.strip().strip('"')
                if stripped:
                    questions.append(stripped)
    return questions


def parse_setting_history_questions(path: str) -> Dict[str, List[str]]:
    """Parse questions for setting, history and timeline from the given file.

    The file is expected to have section headings like 'Setting:',
    'Background/Historical Information:' and 'Timeline:'.  Returns a
    dict mapping each heading to its list of questions.  If the file
    does not exist, returns an empty dict.
    """
    result: Dict[str, List[str]] = {}
    if not os.path.isfile(path):
        return result
    current: Optional[str] = None
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            stripped = line.strip()
            if not stripped:
                continue
            if stripped.endswith(":"):
                current = stripped[:-1]
                result[current] = []
                continue
            if current and stripped.startswith("\""):
                q = stripped.strip().strip(",")
                q = q.strip('"')
                result[current].append(q)
    return result


def default_screenplay_questions() -> Dict[str, List[str]]:
    """Return a default set of questions for screenplay elements."""
    return {
        "Screenplay": [
            "Working title?",
            "Genre?",
            "Logline (one sentence summary)?",
            "Main protagonist name?",
            "Main antagonist name?",
            "Premise or inciting incident?",
            "Key turning point in Act I?",
            "Midpoint revelation?",
            "Climax or final confrontation?",
            "Resolution or ending?"
        ]
    }


class InterviewWindow(tk.Toplevel):
    """A modal dialog for answering a sequence of questions.

    Displays one question at a time with Next/Back navigation.  Answers
    are stored internally and returned via a callback when the user
    finishes.  Voice buttons allow listening to the question or
    recording an answer if the optional libraries are available.
    """

    def __init__(self, master: tk.Widget, title: str, questions: List[str],
                 on_complete: Callable[[Dict[str, str]], None],
                 tts_available: bool = False, stt_available: bool = False):
        super().__init__(master)
        self.title(title)
        self.configure(background="#f4ecdf")
        self.questions = questions
        self.on_complete = on_complete
        self.answers: Dict[str, str] = {q: "" for q in questions}
        self.index = 0
        # Widgets
        self.question_label = tk.Label(self, text="", wraplength=500,
                                       bg="#f4ecdf", fg="#1f1714",
                                       font=("Arial", 14))
        self.question_label.pack(padx=10, pady=(10, 4), anchor="w")
        self.answer_var = tk.StringVar()
        self.answer_entry = tk.Entry(self, textvariable=self.answer_var,
                                     width=60)
        self.answer_entry.pack(padx=10, pady=(0, 10), fill="x")
        # Voice buttons: appear only if dependencies are present.  The
        # ``_tts_engine`` and ``_recognizer`` variables are set during
        # dependency audit in PyWriterAdvanced.  If unavailable, the
        # buttons will be disabled.
        voice_frame = tk.Frame(self, bg="#f4ecdf")
        self.listen_btn = tk.Button(voice_frame, text="🔊 Read", command=self._speak_question)
        self.speak_btn = tk.Button(voice_frame, text="🎤 Speak", command=self._record_answer)
        self.listen_btn.pack(side="left", padx=2)
        self.speak_btn.pack(side="left", padx=2)
        voice_frame.pack(padx=10, pady=(0, 10), anchor="w")
        # Navigation buttons
        nav_frame = tk.Frame(self, bg="#f4ecdf")
        self.prev_btn = tk.Button(nav_frame, text="Back", command=self.prev_question)
        self.next_btn = tk.Button(nav_frame, text="Next", command=self.next_question)
        self.save_btn = tk.Button(nav_frame, text="Finish", command=self.finish)
        self.prev_btn.pack(side="left", padx=5)
        self.next_btn.pack(side="left", padx=5)
        self.save_btn.pack(side="left", padx=5)
        nav_frame.pack(pady=(0, 10))
        self.update_question()
        # Make modal
        self.transient(master)
        self.grab_set()
        # Configure voice buttons based on availability
        self.set_voice_enabled(tts_available, stt_available)
        self.wait_window(self)

    # Utility to configure voice buttons based on capabilities
    def set_voice_enabled(self, tts_available: bool, stt_available: bool) -> None:
        """Enable or disable voice buttons depending on capability flags."""
        if not tts_available:
            self.listen_btn.config(state="disabled")
        if not stt_available:
            self.speak_btn.config(state="disabled")

    def update_question(self) -> None:
        """Update the display based on the current index."""
        q = self.questions[self.index]
        self.question_label.config(text=q)
        self.answer_var.set(self.answers.get(q, ""))
        # Disable Prev button at start
        self.prev_btn.config(state="normal" if self.index > 0 else "disabled")
        # Switch Next to Finish at end
        if self.index < len(self.questions) - 1:
            self.next_btn.config(state="normal")
            self.save_btn.config(state="disabled")
        else:
            self.next_btn.config(state="disabled")
            self.save_btn.config(state="normal")

    def prev_question(self) -> None:
        """Go back to the previous question."""
        # Save current answer
        self.answers[self.questions[self.index]] = self.answer_var.get().strip()
        if self.index > 0:
            self.index -= 1
            self.update_question()

    def next_question(self) -> None:
        """Advance to the next question."""
        # Save current answer
        self.answers[self.questions[self.index]] = self.answer_var.get().strip()
        if self.index < len(self.questions) - 1:
            self.index += 1
            self.update_question()

    def finish(self) -> None:
        """Finish the interview and return answers via callback."""
        # Save final answer
        self.answers[self.questions[self.index]] = self.answer_var.get().strip()
        self.on_complete(self.answers)
        self.destroy()

    def _speak_question(self) -> None:
        """Use text‑to‑speech to read the current question aloud."""
        # Reference the module‑level voice engine.  Globals are defined in
        # this module during dependency audit.
        global tts_engine
        if tts_engine:
            q = self.questions[self.index]
            tts_engine.say(q)
            try:
                tts_engine.runAndWait()
            except Exception as e:
                messagebox.showerror("TTS Error", str(e))
        else:
            messagebox.showinfo("TTS unavailable", "Text‑to‑speech library not installed or failed to initialise.")

    def _record_answer(self) -> None:
        """Use speech recognition to record an answer and insert it."""
        global sr, recognizer, microphone
        if sr and recognizer and microphone:
            messagebox.showinfo("Listening", "Please speak your answer after clicking OK…")
            try:
                with microphone as source:
                    recognizer.adjust_for_ambient_noise(source)
                    audio = recognizer.listen(source, timeout=5)
                try:
                    # Use default recognizer (could specify language)
                    text = recognizer.recognize_google(audio)
                except sr.RequestError:
                    text = ""
                except sr.UnknownValueError:
                    text = ""
                if text:
                    # Append or replace
                    current = self.answer_var.get().strip()
                    if current:
                        self.answer_var.set(current + " " + text)
                    else:
                        self.answer_var.set(text)
            except Exception as e:
                messagebox.showerror("Speech Recognition Error", str(e))
        else:
            messagebox.showinfo(
                "Speech recognition unavailable",
                "SpeechRecognition library, recogniser or microphone not installed or failed to initialise."
            )


class AdvancedInterviewWindow(tk.Toplevel):
    """A reusable dialog for answering a sequence of questions with resume, autosave and notes.

    The window displays one question at a time using a multi‑line text box for answers.
    Progress is saved on each navigation and via a periodic autosave.  The
    underlying entry dictionary passed in is updated in place with the
    latest answers, progress index and notes.  When the user finishes,
    the entry is marked complete and the parent tree view row is updated.
    Voice buttons allow listening to the question or recording an answer if
    optional libraries are available.
    """

    def __init__(self, master: tk.Widget, title: str, questions: List[str], entry: Dict[str, Any],
                 tree: Optional[ttk.Treeview] = None, row_id: Optional[str] = None,
                 tts_available: bool = False, stt_available: bool = False) -> None:
        super().__init__(master)
        self.title(title)
        self.configure(background="#f4ecdf")
        self.questions = questions
        self.entry = entry
        self.tree = tree
        self.row_id = row_id
        # Dynamic interview logic: identify qualifier and skip questions for scale
        # and timeline.  skip_indices will hold indices to skip based on answers.
        self.skip_indices: Set[int] = set()
        # Determine qualifier positions and target indices for skipping.  The
        # questions list may vary by project type and section.  For fiction
        # settings, the scale qualifier is the question that contains
        # "single village/town/city"; the next question (index+1) is skipped if the
        # answer indicates a single location.  For fiction history, the timeline
        # qualifier contains "single linear timeline" and the time‑travel
        # question contains "flashbacks" or "time-travel".
        self.scale_qualifier: Optional[int] = None
        self.scale_skip: Optional[int] = None
        self.timeline_qualifier: Optional[int] = None
        self.timeline_skip: Optional[int] = None
        for i, q in enumerate(self.questions):
            lower_q = q.lower()
            if "single village" in lower_q or "single village/town" in lower_q:
                self.scale_qualifier = i
                if i + 1 < len(self.questions):
                    self.scale_skip = i + 1
            if "single linear timeline" in lower_q:
                self.timeline_qualifier = i
            # Identify the time‑travel specific question
            if ("time-travel" in lower_q or "time travel" in lower_q or "alternate timelines" in lower_q) and self.timeline_skip is None:
                self.timeline_skip = i
        # Start at saved progress index or 0
        self.index = entry.get("progress_index", 0)
        # Autosave interval in ms
        self.autosave_interval = 10000
        self.autosave_id: Optional[str] = None
        # Question label
        self.question_label = tk.Label(self, text="", wraplength=500,
                                       bg="#f4ecdf", fg="#1f1714",
                                       font=("Arial", 14))
        self.question_label.pack(padx=10, pady=(10, 4), anchor="w")
        # Multi‑line answer text
        self.answer_text = tk.Text(self, height=4, wrap="word", width=60)
        self.answer_text.pack(padx=10, pady=(0, 10), fill="both", expand=False)
        # Autosave when typing in answer
        self.answer_text.bind("<KeyRelease>", lambda e: self._autosave_keystroke())
        # Notes area
        notes_frame = tk.Frame(self, bg="#f4ecdf")
        tk.Label(notes_frame, text="Notes:", bg="#f4ecdf").pack(anchor="w")
        self.notes_text = tk.Text(notes_frame, height=3, wrap="word", width=60)
        self.notes_text.pack(fill="both", expand=True)
        tk.Button(notes_frame, text="Add Note", command=self._add_note).pack(anchor="e", pady=(2, 4))
        notes_frame.pack(padx=10, pady=(0, 10), fill="both", expand=False)
        # Autosave on note typing
        self.notes_text.bind("<KeyRelease>", lambda e: self._autosave_keystroke())
        # Voice controls
        voice_frame = tk.Frame(self, bg="#f4ecdf")
        self.listen_btn = tk.Button(voice_frame, text="🔊 Read", command=self._speak_question)
        self.speak_btn = tk.Button(voice_frame, text="🎤 Speak", command=self._record_answer)
        self.listen_btn.pack(side="left", padx=2)
        self.speak_btn.pack(side="left", padx=2)
        # Narration toggle: provide a checkbutton for hands‑free mode
        self.narration_var = tk.BooleanVar(value=False)
        self.narration_toggle = tk.Checkbutton(
            voice_frame,
            text="Narration",
            variable=self.narration_var,
            command=self._toggle_narration,
            bg="#f4ecdf"
        )
        self.narration_toggle.pack(side="left", padx=2)
        voice_frame.pack(padx=10, pady=(0, 10), anchor="w")
        # Navigation buttons
        nav_frame = tk.Frame(self, bg="#f4ecdf")
        self.prev_btn = tk.Button(nav_frame, text="Back", command=self.prev_question)
        self.next_btn = tk.Button(nav_frame, text="Next", command=self.next_question)
        self.save_btn = tk.Button(nav_frame, text="Finish", command=self.finish)
        self.prev_btn.pack(side="left", padx=5)
        self.next_btn.pack(side="left", padx=5)
        self.save_btn.pack(side="left", padx=5)
        nav_frame.pack(pady=(0, 10))
        # Populate initial question
        self.update_question()
        # Schedule autosave
        self._schedule_autosave()
        # Centre the interview window on the screen with a sensible default size
        try:
            self._centre_window()
        except Exception:
            pass
        # Make modal
        self.transient(master)
        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", self._on_close)
        # Disable narration toggle if either TTS or STT is unavailable
        if not (tts_available and stt_available):
            self.narration_toggle.config(state="disabled")
        # Initialise narration state
        self.narration_mode = False
        self.stop_narration = False
        self.narration_thread: Optional[threading.Thread] = None
        self.set_voice_enabled(tts_available, stt_available)
        self.wait_window(self)

    def _centre_window(self, width_fraction: float = 0.5, height_fraction: float = 0.5) -> None:
        """Centre this window on the screen with relative sizing.

        Chooses a size based on fractions of the screen dimensions and ensures a
        minimum size for readability.
        """
        try:
            sw = self.winfo_screenwidth()
            sh = self.winfo_screenheight()
            width = max(int(sw * width_fraction), 600)
            height = max(int(sh * height_fraction), 400)
            x = (sw - width) // 2
            y = (sh - height) // 2
            self.geometry(f"{width}x{height}+{x}+{y}")
        except Exception:
            # If screen info unavailable, fallback to default geometry
            self.geometry("800x600")

    def set_voice_enabled(self, tts_available: bool, stt_available: bool) -> None:
        if not tts_available:
            self.listen_btn.config(state="disabled")
        if not stt_available:
            self.speak_btn.config(state="disabled")

    def _toggle_narration(self) -> None:
        """Toggle hands‑free narration mode on or off.

        When enabled, the current question is read aloud and the system starts
        listening for a spoken answer. Disabling narration stops any active
        listening thread.
        """
        self.narration_mode = bool(self.narration_var.get())
        # Stop any ongoing listening if narration is turned off
        if not self.narration_mode:
            self.stop_narration = True
            if self.narration_thread and self.narration_thread.is_alive():
                try:
                    self.narration_thread.join(timeout=0.1)
                except Exception:
                    pass
        else:
            # Narration turned on: speak the question and start listening
            self._narrate_question()

    def _narrate_question(self) -> None:
        """Speak the current question and initiate listening for an answer.

        Uses the existing TTS engine to read the question aloud, then spawns
        a daemon thread to capture spoken input. Only effective when narration
        mode is enabled.
        """
        if not self.narration_mode:
            return
        try:
            self._speak_question()
        except Exception:
            pass
        # Stop previous listening thread if running
        self.stop_narration = True
        if self.narration_thread and self.narration_thread.is_alive():
            try:
                self.narration_thread.join(timeout=0.1)
            except Exception:
                pass
        # Start listening in a new thread
        self.stop_narration = False
        self.narration_thread = threading.Thread(target=self._listen_for_narration, daemon=True)
        self.narration_thread.start()

    def _listen_for_narration(self) -> None:
        """Background thread function to capture spoken answers.

        Listens via the speech recogniser with a 10‑second time limit. After
        recognition, schedules processing on the main thread. Terminates early
        if narration is stopped.
        """
        global sr, recognizer, microphone
        if not (sr and recognizer and microphone):
            return
        try:
            with microphone as source:
                recognizer.adjust_for_ambient_noise(source)
                try:
                    audio = recognizer.listen(source, timeout=10, phrase_time_limit=10)
                except Exception:
                    return
            if self.stop_narration:
                return
            try:
                text = recognizer.recognize_google(audio)
            except Exception:
                text = ""
            if self.stop_narration:
                return

            def process_text(t=text) -> None:
                self._process_narrated_answer(t)

            try:
                self.after(1, process_text)
            except Exception:
                pass
        except Exception:
            pass

    def _process_narrated_answer(self, text: str) -> None:
        """Handle recognised speech in narration mode.

        Appends the spoken content to the current answer field, then checks
        for command phrases like 'finish' or 'next question' combined with
        confirmation words (confirm/yes/ok/okay). If detected, invokes the
        corresponding navigation action.
        """
        if not self.narration_mode or not text:
            return
        lower = text.lower().strip()
        has_finish = "finish" in lower or "finished" in lower
        has_next = "next question" in lower or "proceed" in lower or "continue" in lower
        has_confirm = any(word in lower for word in ["confirm", "yes", "okay", "ok"])
        # Extract answer text up to the first command keyword
        answer_only = lower
        for kw in ["finish", "finished", "next question", "proceed", "continue", "confirm", "yes", "okay", "ok"]:
            if kw in answer_only:
                answer_only = answer_only.split(kw)[0].strip()
                break
        if answer_only:
            current = self.answer_text.get("1.0", "end").strip()
            new_text = answer_only if not current else (current + " " + answer_only)
            self.answer_text.delete("1.0", "end")
            self.answer_text.insert("1.0", new_text)
            try:
                self._save_current_answer()
                self.master.autosave()
            except Exception:
                pass
        if has_finish and has_confirm:
            try:
                self.finish()
            except Exception:
                pass
            return
        if has_next and has_confirm:
            try:
                self.next_question()
            except Exception:
                pass
            return

    def update_question(self) -> None:
        q = self.questions[self.index]
        self.question_label.config(text=q)
        ans = self.entry.setdefault("answers", {}).get(q, "")
        self.answer_text.delete("1.0", "end")
        self.answer_text.insert("1.0", ans)
        # Buttons
        self.prev_btn.config(state="normal" if self.index > 0 else "disabled")
        if self.index < len(self.questions) - 1:
            self.next_btn.config(state="normal")
            self.save_btn.config(state="disabled")
        else:
            self.next_btn.config(state="disabled")
            self.save_btn.config(state="normal")
        # Automatically narrate the new question when narration mode is active
        try:
            if getattr(self, "narration_mode", False):
                self._narrate_question()
        except Exception:
            pass

    def prev_question(self) -> None:
        self._save_current_answer()
        if self.index > 0:
            new_index = self.index - 1
            # Skip backward over indices flagged for skipping
            while new_index in self.skip_indices and new_index > 0:
                new_index -= 1
            self.index = new_index
            self.entry["progress_index"] = self.index
            self.update_question()
        # Trigger autosave on navigating questions
        try:
            self.master.autosave()
        except Exception:
            pass

    def next_question(self) -> None:
        self._save_current_answer()
        if self.index < len(self.questions) - 1:
            new_index = self.index + 1
            # Skip forward over indices flagged for skipping
            while new_index in self.skip_indices and new_index < len(self.questions) - 1:
                new_index += 1
            if new_index < len(self.questions):
                self.index = new_index
                self.entry["progress_index"] = self.index
                self.update_question()
        # Trigger autosave on navigating questions
        try:
            self.master.autosave()
        except Exception:
            pass

    def finish(self) -> None:
        self._save_current_answer()
        self.entry["complete"] = True
        # Update tree row name
        if self.tree is not None and self.row_id is not None:
            name = next((v for v in self.entry.get("answers", {}).values() if v), "Untitled")
            self.tree.item(self.row_id, values=(name,))
        # Cancel autosave
        if self.autosave_id:
            try:
                self.after_cancel(self.autosave_id)
            except Exception:
                pass
        self.destroy()
        # Trigger autosave on finishing interview
        try:
            self.master.autosave()
        except Exception:
            pass

    def _speak_question(self) -> None:
        global tts_engine
        if tts_engine:
            q = self.questions[self.index]
            tts_engine.say(q)
            try:
                tts_engine.runAndWait()
            except Exception as e:
                messagebox.showerror("TTS Error", str(e))
        else:
            messagebox.showinfo("TTS unavailable", "Text‑to‑speech library not installed or failed to initialise.")

    def _record_answer(self) -> None:
        global sr, recognizer, microphone
        if sr and recognizer and microphone:
            messagebox.showinfo("Listening", "Please speak your answer after clicking OK…")
            try:
                with microphone as source:
                    recognizer.adjust_for_ambient_noise(source)
                    audio = recognizer.listen(source, timeout=5)
                try:
                    text = recognizer.recognize_google(audio)
                except sr.RequestError:
                    text = ""
                except sr.UnknownValueError:
                    text = ""
                if text:
                    current = self.answer_text.get("1.0", "end").strip()
                    if current:
                        self.answer_text.delete("1.0", "end")
                        self.answer_text.insert("1.0", current + " " + text)
                    else:
                        self.answer_text.insert("1.0", text)
            except Exception as e:
                messagebox.showerror("Speech Recognition Error", str(e))
        else:
            messagebox.showinfo(
                "Speech recognition unavailable",
                "SpeechRecognition library, recogniser or microphone not installed or failed to initialise."
            )

    def _save_current_answer(self) -> None:
        q = self.questions[self.index]
        ans = self.answer_text.get("1.0", "end").rstrip()
        self.entry.setdefault("answers", {})[q] = ans
        self.entry["progress_index"] = self.index
        # Apply dynamic skip logic based on qualifiers
        ans_lower = ans.lower()
        # Scale qualifier: if answer indicates single location, skip the next question
        if self.scale_qualifier is not None and self.index == self.scale_qualifier and self.scale_skip is not None:
            if any(word in ans_lower for word in ["single", "village", "town", "city"]):
                self.skip_indices.add(self.scale_skip)
            else:
                self.skip_indices.discard(self.scale_skip)
        # Timeline qualifier: if answer indicates a linear timeline, skip the time travel question
        if self.timeline_qualifier is not None and self.index == self.timeline_qualifier and self.timeline_skip is not None:
            if any(word in ans_lower for word in ["single", "linear"]):
                self.skip_indices.add(self.timeline_skip)
            else:
                self.skip_indices.discard(self.timeline_skip)

    def _autosave(self) -> None:
        try:
            self._save_current_answer()
        except Exception:
            pass
        self._schedule_autosave()

    def _autosave_keystroke(self) -> None:
        """
        Autosave handler for key release events on text widgets.  Saves
        the current answer but does not advance questions.  Called on
        every key release in the answer or notes text boxes.
        """
        try:
            self._save_current_answer()
            self.master.autosave()
        except Exception:
            pass

    def _schedule_autosave(self) -> None:
        if self.autosave_interval > 0:
            self.autosave_id = self.after(self.autosave_interval, self._autosave)

    def _add_note(self) -> None:
        note = self.notes_text.get("1.0", "end").strip()
        if note:
            ts = datetime.datetime.utcnow().isoformat()
            self.entry.setdefault("notes", []).append({"timestamp": ts, "content": note})
            self.notes_text.delete("1.0", "end")
            # Autosave when a note is added
            try:
                self.master.autosave()
            except Exception:
                pass

    def _on_close(self) -> None:
        self._save_current_answer()
        if self.autosave_id:
            try:
                self.after_cancel(self.autosave_id)
            except Exception:
                pass
        if self.tree is not None and self.row_id is not None:
            name = next((v for v in self.entry.get("answers", {}).values() if v), "Untitled")
            self.tree.item(self.row_id, values=(name,))
        self.destroy()
        # Trigger autosave on closing interview window
        try:
            self.master.autosave()
        except Exception:
            pass
        # Stop narration thread if running
        try:
            self.stop_narration = True  # type: ignore[attr-defined]
            if hasattr(self, "narration_thread") and self.narration_thread and self.narration_thread.is_alive():  # type: ignore[attr-defined]
                self.narration_thread.join(timeout=0.1)  # type: ignore[attr-defined]
        except Exception:
            pass


class DetailWindow(tk.Toplevel):
    """Display and edit details of an entry, with cross‑linking and notes.

    This window shows all questions and answers for a given entry in a
    single view.  Answers can be edited directly in multi‑line text
    boxes.  Notes can be added using a simple text field.  Existing
    links to other entries are displayed and can be removed.  A list
    of available entries allows new links to be added.  Changes are
    committed to the underlying entry when the user clicks Save.

    Args:
        master: The parent PyWriterAdvanced instance.
        section: The data section ("characters", "settings", "history", "topics").
        entry: The entry dictionary being edited.
        questions: The list of questions relevant to this section.
        tree: The Treeview widget containing the row for this entry.
        row_id: The item ID of the row in the Treeview (used to update the display name).
    """

    def __init__(self, master: "PyWriterAdvanced", section: str, entry: Dict[str, Any],
                 questions: List[str], tree: ttk.Treeview, row_id: str) -> None:
        super().__init__(master)
        self.master = master
        self.section = section
        self.entry = entry
        self.questions = questions
        self.tree = tree
        self.row_id = row_id
        self.title(f"{section[:-1].capitalize()} Details")
        self.configure(background="#f4ecdf")
        # Container for scrollable content
        canvas = tk.Canvas(self, background="#f4ecdf", borderwidth=0, highlightthickness=0)
        frame = tk.Frame(canvas, background="#f4ecdf")
        vsb = tk.Scrollbar(self, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        canvas.create_window((0, 0), window=frame, anchor="nw")

        def on_frame_configure(event: tk.Event) -> None:
            canvas.configure(scrollregion=canvas.bbox("all"))
        frame.bind("<Configure>", on_frame_configure)

        # Store answer widgets keyed by question
        self.answer_widgets: Dict[str, tk.Text] = {}
        for q in self.questions:
            lbl = tk.Label(frame, text=q, bg="#f4ecdf", anchor="w", wraplength=600, justify="left")
            lbl.pack(fill="x", padx=10, pady=(8, 0))
            txt = tk.Text(frame, height=3, wrap="word", width=60)
            txt.pack(fill="x", padx=10, pady=(0, 4))
            ans = self.entry.setdefault("answers", {}).get(q, "")
            txt.insert("1.0", ans)
            # Autosave on modification
            txt.bind("<KeyRelease>", lambda e: self._on_edit())
            self.answer_widgets[q] = txt

        # Notes section
        notes_label = tk.Label(frame, text="Notes:", bg="#f4ecdf", anchor="w")
        notes_label.pack(fill="x", padx=10, pady=(8, 0))
        # Display existing notes as a listbox
        self.notes_listbox = tk.Listbox(frame, height=4)
        self.notes_listbox.pack(fill="x", padx=10, pady=(0, 2))
        for note in self.entry.get("notes", []):
            ts = note.get("timestamp", "")
            content = note.get("content", "")
            self.notes_listbox.insert(tk.END, f"[{ts}] {content}")
        # Entry for new note
        self.new_note_text = tk.Text(frame, height=2, wrap="word")
        self.new_note_text.pack(fill="x", padx=10, pady=(0, 2))
        add_note_btn = tk.Button(frame, text="Add Note", command=self._add_note)
        add_note_btn.pack(padx=10, pady=(0, 6), anchor="e")

        # Links section
        links_frame = tk.Frame(frame, bg="#f4ecdf")
        tk.Label(links_frame, text="Links:", bg="#f4ecdf").grid(row=0, column=0, sticky="w")
        tk.Label(links_frame, text="Available:", bg="#f4ecdf").grid(row=0, column=2, sticky="w")
        # Listbox for existing links
        self.links_listbox = tk.Listbox(links_frame, height=5)
        self.links_listbox.grid(row=1, column=0, sticky="nsew", padx=(0, 5))
        # Buttons for link operations
        btn_frame = tk.Frame(links_frame, bg="#f4ecdf")
        add_link_btn = tk.Button(btn_frame, text="→", command=self._add_link)
        remove_link_btn = tk.Button(btn_frame, text="←", command=self._remove_link)
        add_link_btn.pack(pady=2)
        remove_link_btn.pack(pady=2)
        btn_frame.grid(row=1, column=1, sticky="ns")
        # Listbox for available entries
        self.available_listbox = tk.Listbox(links_frame, height=5)
        self.available_listbox.grid(row=1, column=2, sticky="nsew")
        # Configure resizing
        links_frame.grid_columnconfigure(0, weight=1)
        links_frame.grid_columnconfigure(2, weight=1)
        links_frame.pack(fill="both", padx=10, pady=(4, 8))
        # Populate lists
        self._refresh_links_display()

        # Action buttons
        btn_row = tk.Frame(frame, bg="#f4ecdf")
        save_btn = tk.Button(btn_row, text="Save", command=self._save)
        reinterview_btn = tk.Button(btn_row, text="Re‑interview", command=self._reinterview)
        cancel_btn = tk.Button(btn_row, text="Close", command=self._close)
        save_btn.pack(side="left", padx=4)
        reinterview_btn.pack(side="left", padx=4)
        cancel_btn.pack(side="left", padx=4)
        btn_row.pack(pady=(4, 8), padx=10, anchor="e")

        # Modal behaviour
        self.transient(master)
        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", self._close)

    def _on_edit(self) -> None:
        """Trigger autosave when any answer text is edited."""
        try:
            self.master.autosave()
        except Exception:
            pass

    def _add_note(self) -> None:
        """Add the text from the new note field as a timestamped note."""
        note = self.new_note_text.get("1.0", "end").strip()
        if note:
            ts = datetime.datetime.utcnow().isoformat()
            self.entry.setdefault("notes", []).append({"timestamp": ts, "content": note})
            self.notes_listbox.insert(tk.END, f"[{ts}] {note}")
            self.new_note_text.delete("1.0", "end")
            # Autosave when note is added
            try:
                self.master.autosave()
            except Exception:
                pass

    def _refresh_links_display(self) -> None:
        """Refresh the lists of existing and available links."""
        # Populate existing links list
        self.links_listbox.delete(0, tk.END)
        # Build mapping of id to display name and section
        id_to_name = {}
        for sec in ["characters", "settings", "history", "topics"]:
            for ent in self.master.data.get(sec, []):
                name = next((v for v in ent.get("answers", {}).values() if v), ent.get("id"))
                id_to_name[ent.get("id")] = f"{name} ({sec[:-1]})"
        for lid in self.entry.get("links", []):
            display = id_to_name.get(lid, lid)
            self.links_listbox.insert(tk.END, display)
        # Populate available list
        self.available_listbox.delete(0, tk.END)
        self.available_ids: List[str] = []
        for sec in ["characters", "settings", "history", "topics"]:
            for ent in self.master.data.get(sec, []):
                eid = ent.get("id")
                if eid and eid != self.entry.get("id") and eid not in self.entry.get("links", []):
                    name = next((v for v in ent.get("answers", {}).values() if v), eid)
                    self.available_listbox.insert(tk.END, f"{name} ({sec[:-1]})")
                    self.available_ids.append(eid)

    def _add_link(self) -> None:
        """Add selected entry from available list to the links list."""
        sel = self.available_listbox.curselection()
        if not sel:
            return
        index = sel[0]
        target_id = self.available_ids[index]
        if target_id not in self.entry.get("links", []):
            self.entry.setdefault("links", []).append(target_id)
        self._refresh_links_display()
        # Autosave
        try:
            self.master.autosave()
        except Exception:
            pass

    def _remove_link(self) -> None:
        """Remove selected link from the entry."""
        sel = self.links_listbox.curselection()
        if not sel:
            return
        index = sel[0]
        try:
            # Determine id from current list by mapping names to ids
            display = self.links_listbox.get(index)
            # id is part before parenthesis or find by mapping
            # Rebuild mapping
            id_map = {}
            for sec in ["characters", "settings", "history", "topics"]:
                for ent in self.master.data.get(sec, []):
                    name = next((v for v in ent.get("answers", {}).values() if v), ent.get("id"))
                    id_map[f"{name} ({sec[:-1]})"] = ent.get("id")
            lid = id_map.get(display)
            if lid and lid in self.entry.get("links", []):
                self.entry["links"].remove(lid)
        except Exception:
            pass
        self._refresh_links_display()
        # Autosave
        try:
            self.master.autosave()
        except Exception:
            pass

    def _save(self) -> None:
        """Commit changes to the entry and close the window."""
        # Update answers
        for q, widget in self.answer_widgets.items():
            ans = widget.get("1.0", "end").rstrip()
            self.entry.setdefault("answers", {})[q] = ans
        # Entry already has updated notes and links
        # Update tree display name
        if self.tree is not None and self.row_id is not None:
            name = next((v for v in self.entry.get("answers", {}).values() if v), "Untitled")
            self.tree.item(self.row_id, values=(name,))
        # Trigger autosave
        try:
            self.master.autosave()
        except Exception:
            pass
        self.destroy()

    def _reinterview(self) -> None:
        """Reopen the interview dialog for this entry with existing answers prefilled."""
        # Commit current edits to entry before re‑interview
        for q, widget in self.answer_widgets.items():
            ans = widget.get("1.0", "end").rstrip()
            self.entry.setdefault("answers", {})[q] = ans
        try:
            # Determine appropriate tree for this section
            tree = None
            if self.section == "characters":
                tree = self.master.char_tree
            elif self.section == "settings":
                tree = self.master.set_tree
            elif self.section == "history":
                tree = self.master.hist_tree
            elif self.section == "topics":
                tree = self.master.topic_tree
            self.master._start_interview(self.section, self.questions, tree, entry=self.entry, item_id=self.row_id)
        except Exception:
            pass
        # After re‑interview, update tree row name via refresh
        try:
            self.master.autosave()
        except Exception:
            pass
        self.destroy()

    def _close(self) -> None:
        """Close the detail window without committing further edits."""
        # Do not commit unsaved changes; but update tree display name just in case
        if self.tree is not None and self.row_id is not None:
            name = next((v for v in self.entry.get("answers", {}).values() if v), "Untitled")
            self.tree.item(self.row_id, values=(name,))
        try:
            self.master.autosave()
        except Exception:
            pass
        self.destroy()


class PyWriterAdvanced(tk.Tk):
    """Comprehensive GUI for writing projects."""

    def __init__(self) -> None:
        super().__init__()
        self.title("FoolsGold PyWriter – Complete")
        self.configure(background="#f4ecdf")
        # Size and centre the main window relative to the screen
        self._centre_main_window()

        # Run a dependency audit before initialising the rest of the application.
        # This sets flags for optional capabilities (e.g. voice features) and
        # verifies that hard requirements are available.  If a hard
        # requirement is missing, a user‑friendly error will be shown and the
        # application will exit gracefully.
        self.capabilities: Dict[str, Any] = self._perform_dependency_audit()

        # Logging
        self.logger = logging.getLogger("pywriter")
        self.logger.setLevel(logging.INFO)
        # Logging handler will be configured on a per-project basis.  For now, attach
        # a NullHandler until a project is created.  Once a project directory is
        # established, _setup_logging() will replace this handler with a file
        # handler in the project logs directory.
        self.logger.addHandler(logging.NullHandler())

        # Project metadata: name and root folder.  These are set when the user
        # chooses a project type and enters a project name.  The directory
        # structure will be created at that time (see _create_new_project()).
        self.project_name: Optional[str] = None
        self.project_root: Optional[str] = None
        self.data_dir: Optional[str] = None
        self.log_dir: Optional[str] = None
        self.backup_dir: Optional[str] = None

        # Data store
        # Contains summary (string) and categories mapping type to a list of entry dicts.
        # Each entry dict has the shape {
        #   "id": unique_id,
        #   "created": ISO timestamp,
        #   "answers": {question: answer, ...}
        # }
        self.data: Dict[str, Any] = {
            "project_type": "Fiction",
            "summary": "",
            "characters": [],
            "settings": [],
            "history": [],
            "topics": []
        }

        # Question packs
        # Use the embedded question packs as the primary source of interview prompts.
        # External question files are no longer read at runtime.  The parse_* functions
        # remain available for future extensions or fallback behaviour but are not
        # invoked here.  Each project type maps to a dictionary of section names
        # ('characters', 'settings', 'history', 'topics') containing lists of
        # questions defined in QUESTION_PACKS.
        self.question_packs: Dict[str, Dict[str, List[str]]] = QUESTION_PACKS

        # UI variables
        self.project_type = tk.StringVar(value=self.data["project_type"])
        self.distraction_mode = False

        # Build UI
        self._create_widgets()
        # Show splash
        self.withdraw()
        self.after(10, self._show_splash)
        # Bind close event to autosave
        self.protocol("WM_DELETE_WINDOW", self._on_close_app)

    # --- UI Setup ---
    def _show_splash(self) -> None:
        splash = tk.Toplevel(self)
        splash.overrideredirect(True)
        w = self.winfo_screenwidth()
        h = self.winfo_screenheight()
        splash.geometry(f"{w}x{h}+0+0")
        # Display splash image if possible
        if Image and ImageTk:
            try:
                img_path = self._resource_path("splash.png")
                img = Image.open(img_path)
                # Scale image to fit screen
                img = img.resize((w, h), Image.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                lbl = tk.Label(splash, image=photo)
                lbl.image = photo
                lbl.pack(fill="both", expand=True)
            except Exception:
                splash.configure(background="#f4ecdf")
        else:
            splash.configure(background="#f4ecdf")
        splash.after(2500, lambda: (splash.destroy(), self.deiconify()))

    def _create_widgets(self) -> None:
        # Top bar for project type and distraction free toggle
        self.top_frame = tk.Frame(self, bg="#f4ecdf")
        tk.Label(self.top_frame, text="Project type:", bg="#f4ecdf").pack(side="left", padx=(10, 4))
        type_menu = ttk.Combobox(self.top_frame, textvariable=self.project_type,
                                 values=["Fiction", "Non-Fiction", "Biography"],
                                 state="readonly")
        type_menu.pack(side="left")
        type_menu.bind("<<ComboboxSelected>>", self._on_type_changed)
        df_btn = tk.Button(self.top_frame, text="Distraction Free", command=self._toggle_distraction)
        df_btn.pack(side="right", padx=10)
        self.top_frame.pack(fill="x", pady=(5, 0))

        # Notebook
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=5)
        # Bind tab changed event to autosave
        self.notebook.bind("<<NotebookTabChanged>>", lambda e: self.autosave())
        # Summary tab
        summary_frame = tk.Frame(self.notebook, bg="#f4ecdf")
        tk.Label(summary_frame, text="Summary:", bg="#f4ecdf").pack(anchor="w", pady=(5, 0))
        self.summary_text = tk.Text(summary_frame, height=5, wrap="word", bg="#faf5e9")
        self.summary_text.pack(fill="both", expand=True, pady=(0, 5))
        # Bind key release to autosave (cursor movement in summary triggers save)
        self.summary_text.bind("<KeyRelease>", lambda e: self.autosave())
        self.notebook.add(summary_frame, text="Summary")

        # Characters tab
        char_frame = tk.Frame(self.notebook, bg="#f4ecdf")
        self.char_tree = ttk.Treeview(char_frame, columns=("Name"), show="headings")
        self.char_tree.heading("Name", text="Name")
        self.char_tree.pack(fill="both", expand=True, pady=(0, 5))
        # Double click opens detail view
        self.char_tree.bind("<Double-1>", lambda e: self._open_detail("characters", self.char_tree, e))
        char_btn_frame = tk.Frame(char_frame, bg="#f4ecdf")
        tk.Button(char_btn_frame, text="Add Character", command=self._add_character).pack(side="left", padx=2)
        tk.Button(char_btn_frame, text="Edit", command=lambda: self._edit_item("characters", self.char_tree)).pack(side="left", padx=2)
        tk.Button(char_btn_frame, text="Delete", command=lambda: self._delete_item("characters", self.char_tree)).pack(side="left", padx=2)
        char_btn_frame.pack()
        self.notebook.add(char_frame, text="Characters")

        # Settings tab
        set_frame = tk.Frame(self.notebook, bg="#f4ecdf")
        self.set_tree = ttk.Treeview(set_frame, columns=("Name"), show="headings")
        self.set_tree.heading("Name", text="Location")
        self.set_tree.pack(fill="both", expand=True, pady=(0, 5))
        self.set_tree.bind("<Double-1>", lambda e: self._open_detail("settings", self.set_tree, e))
        set_btn_frame = tk.Frame(set_frame, bg="#f4ecdf")
        tk.Button(set_btn_frame, text="Add Setting", command=self._add_setting).pack(side="left", padx=2)
        tk.Button(set_btn_frame, text="Edit", command=lambda: self._edit_item("settings", self.set_tree)).pack(side="left", padx=2)
        tk.Button(set_btn_frame, text="Delete", command=lambda: self._delete_item("settings", self.set_tree)).pack(side="left", padx=2)
        set_btn_frame.pack()
        self.notebook.add(set_frame, text="Settings")

        # History/Timeline tab
        hist_frame = tk.Frame(self.notebook, bg="#f4ecdf")
        self.hist_tree = ttk.Treeview(hist_frame, columns=("Title"), show="headings")
        self.hist_tree.heading("Title", text="Event / Period")
        self.hist_tree.pack(fill="both", expand=True, pady=(0, 5))
        self.hist_tree.bind("<Double-1>", lambda e: self._open_detail("history", self.hist_tree, e))
        hist_btn_frame = tk.Frame(hist_frame, bg="#f4ecdf")
        tk.Button(hist_btn_frame, text="Add Event", command=self._add_history).pack(side="left", padx=2)
        tk.Button(hist_btn_frame, text="Edit", command=lambda: self._edit_item("history", self.hist_tree)).pack(side="left", padx=2)
        tk.Button(hist_btn_frame, text="Delete", command=lambda: self._delete_item("history", self.hist_tree)).pack(side="left", padx=2)
        hist_btn_frame.pack()
        self.notebook.add(hist_frame, text="Timeline")

        # Topics/References tab for Non‑Fiction projects
        topic_frame = tk.Frame(self.notebook, bg="#f4ecdf")
        self.topic_tree = ttk.Treeview(topic_frame, columns=("Title"), show="headings")
        self.topic_tree.heading("Title", text="Topic / Reference")
        self.topic_tree.pack(fill="both", expand=True, pady=(0, 5))
        self.topic_tree.bind("<Double-1>", lambda e: self._open_detail("topics", self.topic_tree, e))
        topic_btn_frame = tk.Frame(topic_frame, bg="#f4ecdf")
        tk.Button(topic_btn_frame, text="Add Topic", command=self._add_topic).pack(side="left", padx=2)
        tk.Button(topic_btn_frame, text="Edit", command=lambda: self._edit_item("topics", self.topic_tree)).pack(side="left", padx=2)
        tk.Button(topic_btn_frame, text="Delete", command=lambda: self._delete_item("topics", self.topic_tree)).pack(side="left", padx=2)
        topic_btn_frame.pack()
        self.notebook.add(topic_frame, text="Topics")

        # Screenplay functionality removed.  Screenplay projects are not supported in this version.

        # Bottom bar for save/load and other actions
        self.bottom_frame = tk.Frame(self, bg="#f4ecdf")
        # Left side: project operations
        tk.Button(self.bottom_frame, text="Save", command=self.save_project).pack(side="left", padx=4)
        tk.Button(self.bottom_frame, text="Load", command=self.load_project).pack(side="left", padx=4)
        # Right side: external actions and diagnostics
        tk.Button(self.bottom_frame, text="Diagnostics", command=self.show_diagnostics).pack(side="right", padx=4)
        tk.Button(self.bottom_frame, text="Report Bug", command=lambda: self._external_action("bug")).pack(side="right", padx=4)
        tk.Button(self.bottom_frame, text="Feedback", command=lambda: self._external_action("feedback")).pack(side="right", padx=4)
        tk.Button(self.bottom_frame, text="Donate", command=lambda: self._external_action("donate")).pack(side="right", padx=4)
        self.bottom_frame.pack(fill="x", pady=(0, 5), padx=10)

    # --- Event handlers ---
    def _on_type_changed(self, event: tk.Event) -> None:
        """Handle changes to the project type.

        When the user selects a new project type, prompt for a project name
        and root directory, create the necessary folder structure and reset
        existing data.  If a project is already open, confirm before
        discarding unsaved changes.  The selected type is stored in
        self.data["project_type"].
        """
        new_type = self.project_type.get()
        # If there is existing data or a project name is set, warn the user
        if any(self.data.get(key) for key in ["characters", "settings", "history", "topics"]) or self.project_name:
            if not messagebox.askyesno(
                "Change project type",
                "Changing the project type will clear current data and close the current project. Continue?"
            ):
                # Revert selection and return
                self.project_type.set(self.data.get("project_type", new_type))
                return
        # Update project type immediately so that subsequent dialogs refer to the new type
        self.data["project_type"] = new_type
        # Create a new project: ask for name and directory
        if not self._create_new_project():
            # User cancelled or invalid name: revert selection
            self.project_type.set(self.data.get("project_type", new_type))
            return
        # Clear current data and UI
        for key in ["characters", "settings", "history", "topics"]:
            self.data[key] = []
        self._refresh_all()
        self.summary_text.delete("1.0", "end")

    def _toggle_distraction(self) -> None:
        """Toggle distraction‑free mode.

        When enabled, hides the top and bottom UI bars, enters full‑screen mode
        and binds the Escape key to exit.  When disabled, restores the window
        decorations and shows the hidden UI bars.
        """
        self.distraction_mode = not self.distraction_mode
        if self.distraction_mode:
            # Hide UI elements
            try:
                self.top_frame.pack_forget()
                self.bottom_frame.pack_forget()
            except Exception:
                pass
            # Enter fullscreen mode
            self.attributes("-fullscreen", True)
            # Bind Escape to exit distraction mode
            self.bind("<Escape>", lambda e: self._exit_distraction())
        else:
            self._exit_distraction()

    def _exit_distraction(self) -> None:
        """Exit distraction‑free mode and restore the UI."""
        try:
            # Exit fullscreen mode
            self.attributes("-fullscreen", False)
        except Exception:
            pass
        # Repack the previously hidden bars
        try:
            self.top_frame.pack(fill="x", pady=(5, 0))
            self.bottom_frame.pack(fill="x", pady=(0, 5), padx=10)
        except Exception:
            pass
        # Reset mode and unbind Escape
        self.distraction_mode = False
        try:
            self.unbind("<Escape>")
        except Exception:
            pass

    # --- CRUD for characters ---
    def _add_character(self) -> None:
        """Start a new character interview using the advanced interview engine."""
        ptype = self.data["project_type"]
        # Determine questions by project type using question packs
        packs = self.question_packs.get(ptype, {})
        questions = packs.get("characters") or [
            "Name?", "Role in story?", "Background?", "Motivation?", "Strengths?", "Weaknesses?"
        ]
        # Create entry and launch advanced interview
        self._start_interview("characters", questions, self.char_tree)

    # --- CRUD for settings ---
    def _add_setting(self) -> None:
        """Start a new setting interview using the advanced interview engine."""
        ptype = self.data["project_type"]
        packs = self.question_packs.get(ptype, {})
        questions = packs.get("settings") or [
            "Location name?",
            "Time period or era?",
            "Physical description?",
            "Cultural and societal context?",
            "Key landmarks?",
            "Geography and climate?",
            "Historical background?",
            "Symbolic meaning?"
        ]
        self._start_interview("settings", questions, self.set_tree)

    # --- CRUD for history / timeline ---
    def _add_history(self) -> None:
        """Start a new history/timeline interview using the advanced interview engine."""
        ptype = self.data["project_type"]
        packs = self.question_packs.get(ptype, {})
        questions = packs.get("history") or [
            "Event name?",
            "Time period?",
            "Description of the event?",
            "Major characters involved?",
            "Impact on plot or subject?",
            "Causes and consequences?",
            "Related conflicts/resolutions?",
            "Historical significance?"
        ]
        self._start_interview("history", questions, self.hist_tree)

    # --- CRUD for topics (non‑fiction) ---
    def _add_topic(self) -> None:
        """Start a new non‑fiction topic interview using the advanced interview engine."""
        ptype = self.data["project_type"]
        packs = self.question_packs.get(ptype, {})
        # For non‑fiction projects, topics represent research areas or reference materials.  For
        # other types, the topics tab may still be used for thematic or relational
        # exploration (e.g. arcs or relationships).  If no questions are available, use
        # a generic fallback list.
        if not packs:
            messagebox.showinfo("Not applicable", "Topics tab is not available for this project type.")
            return
        questions = packs.get("topics") or [
            "Name of topic or relationship?",
            "Purpose or significance?",
            "Key points or features?",
            "Evidence or sources?",
            "Conflicts or controversies?",
            "Target audience or stakeholders?",
            "Outcomes or conclusions?",
            "Broader implications?"
        ]
        self._start_interview("topics", questions, self.topic_tree)

    # --- Screenplay CRUD removed ---
    def _add_screenplay(self) -> None:
        messagebox.showinfo("Not applicable", "Screenplay projects are not supported in this version.")

    # --- Save entry callback ---
    def _save_entry(self, section: str, answers: Dict[str, str], tree: ttk.Treeview) -> None:
        """Append the interview answers to the data and refresh tree.

        Wrap the raw answers in a structured dict with a stable unique id
        and creation timestamp.  Then insert a summary row in the tree view.
        """
        # Generate a unique id using section prefix and uuid4
        uid = f"{section[:-1]}-{uuid.uuid4().hex[:8]}"
        timestamp = datetime.datetime.utcnow().isoformat()
        entry = {
            "id": uid,
            "created": timestamp,
            "answers": answers
        }
        # Append to data store
        self.data[section].append(entry)
        # Derive a display name: first non‑empty answer
        name = next((v for v in answers.values() if v), "Untitled")
        tree.insert("", "end", values=(name,))
        self.logger.info(f"Added {section[:-1]}: {name}")

    def _edit_item(self, section: str, tree: ttk.Treeview) -> None:
        selection = tree.selection()
        if not selection:
            return
        item = selection[0]
        index = tree.index(item)
        data_entry = self.data[section][index]
        # Use the keys of the answers dict to preserve question order
        answers_dict = data_entry.get("answers", {})
        questions = list(answers_dict.keys()) or ["Question?", "Answer?"]
        # Launch advanced interview window for editing, passing the existing entry and tree row
        self._start_interview(section, questions, tree, entry=data_entry, item_id=item)

    def _delete_item(self, section: str, tree: ttk.Treeview) -> None:
        selection = tree.selection()
        if not selection:
            return
        if messagebox.askyesno("Delete", "Are you sure you want to delete this entry?"):
            item = selection[0]
            index = tree.index(item)
            tree.delete(item)
            del self.data[section][index]
            self.logger.info(f"Deleted {section[:-1]}")

    def _open_detail(self, section: str, tree: ttk.Treeview, event: tk.Event) -> None:
        """Open the detail view for the selected entry on double‑click."""
        # Identify row under pointer
        item_id = tree.identify_row(event.y)
        if not item_id:
            return
        try:
            index = tree.index(item_id)
        except Exception:
            return
        # Get entry and corresponding questions
        try:
            entry = self.data.get(section, [])[index]
        except Exception:
            return
        # Determine question list for this project type and section
        qpacks = self.question_packs.get(self.data.get("project_type", "Fiction"), {})
        questions = qpacks.get(section, [])
        # Open detail window
        try:
            DetailWindow(self, section, entry, questions, tree, item_id)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ---------------------------------------------------------------------
    # Interview orchestration
    #
    def _create_entry(self, section: str, questions: List[str]) -> Dict[str, Any]:
        """Create a new entry with id, timestamp, blank answers and notes."""
        uid = f"{section[:-1]}-{uuid.uuid4().hex[:8]}"
        created = datetime.datetime.utcnow().isoformat()
        answers = {q: "" for q in questions}
        entry = {
            "id": uid,
            "created": created,
            "answers": answers,
            "notes": [],
            "progress_index": 0,
            "complete": False,
            # Links to other entities (by ID).  Used for cross‑reference between characters,
            # settings, events and topics.  Initially empty; populated via the detail view.
            "links": []
        }
        self.data[section].append(entry)
        return entry

    def _start_interview(self, section: str, questions: List[str], tree: ttk.Treeview, entry: Optional[Dict[str, Any]] = None, item_id: Optional[str] = None) -> None:
        """Create or resume an interview for a section.

        If entry is None, a new entry is created and added to self.data.  A row is
        inserted into the tree view immediately to reflect the new entry.  The
        AdvancedInterviewWindow manages autosave and resume by updating the
        entry in place.
        """
        # Create a new entry if needed
        if entry is None:
            entry = self._create_entry(section, questions)
            # Insert a new row into the tree view with a placeholder name
            item_id = tree.insert("", "end", values=("Untitled",))
        # Launch the advanced interview window
        AdvancedInterviewWindow(self, f"{section[:-1].capitalize()} Interview", questions, entry,
                                tree=tree, row_id=item_id,
                                tts_available=self.capabilities.get("tts_available", False),
                                stt_available=self.capabilities.get("stt_available", False))

    def _refresh_all(self) -> None:
        """Refresh tree views from data store."""
        # Clear all trees
        for tree_widget in [self.char_tree, self.set_tree, self.hist_tree, self.topic_tree]:
            tree_widget.delete(*tree_widget.get_children())
        # Repopulate characters
        for i, entry in enumerate(self.data.get("characters", [])):
            answers = entry.get("answers", {})
            name = next((v for v in answers.values() if v), f"Character {i+1}")
            self.char_tree.insert("", "end", values=(name,))
        # Repopulate settings
        for i, entry in enumerate(self.data.get("settings", [])):
            answers = entry.get("answers", {})
            name = next((v for v in answers.values() if v), f"Setting {i+1}")
            self.set_tree.insert("", "end", values=(name,))
        # Repopulate history/timeline
        for i, entry in enumerate(self.data.get("history", [])):
            answers = entry.get("answers", {})
            title = next((v for v in answers.values() if v), f"Event {i+1}")
            self.hist_tree.insert("", "end", values=(title,))
        # Repopulate topics
        for i, entry in enumerate(self.data.get("topics", [])):
            answers = entry.get("answers", {})
            title = next((v for v in answers.values() if v), f"Topic {i+1}")
            self.topic_tree.insert("", "end", values=(title,))

    # ------------------------------------------------------------------
    # Project management and saving
    #
    def _create_new_project(self) -> bool:
        """
        Prompt the user for a project name and base directory, validate
        the input, create the project folder and subdirectories, and
        initialise logging.  Returns True on success or False if the
        operation is cancelled.
        """
        # Ask for a project name
        name = simpledialog.askstring("Project Name", "Enter a name for your project:")
        if not name:
            return False
        # Sanitize: replace invalid characters with underscores
        import re
        sanitized = re.sub(r"[^A-Za-z0-9 _-]", "_", name).strip()
        if not sanitized:
            messagebox.showerror("Invalid name", "Project name must contain at least one alphanumeric character.")
            return False
        # Ask for directory
        base_dir = filedialog.askdirectory(title="Select project directory")
        if not base_dir:
            return False
        # Define project root and subdirectories
        proj_root = os.path.join(base_dir, sanitized)
        data_dir = os.path.join(proj_root, "data")
        log_dir = os.path.join(proj_root, "logs")
        backup_dir = os.path.join(proj_root, "backups")
        try:
            os.makedirs(data_dir, exist_ok=True)
            os.makedirs(log_dir, exist_ok=True)
            os.makedirs(backup_dir, exist_ok=True)
        except Exception as exc:
            messagebox.showerror("Directory Error", f"Failed to create project directories:\n{exc}")
            return False
        # Set project attributes
        self.project_name = sanitized
        self.project_root = proj_root
        self.data_dir = data_dir
        self.log_dir = log_dir
        self.backup_dir = backup_dir
        # Set up logging for this project
        self._setup_logging()
        # Write initial log entry
        self.logger.info(f"New project created: {sanitized} at {proj_root}")
        return True

    def _setup_logging(self) -> None:
        """
        Configure the logger to write to a new log file in the project's
        log directory.  Closes any existing file handlers and creates a
        timestamped log file.  Subsequent autosaves will rotate the log
        file as needed.
        """
        # Remove existing file handlers
        for handler in list(self.logger.handlers):
            if isinstance(handler, logging.FileHandler):
                try:
                    handler.close()
                except Exception:
                    pass
                self.logger.removeHandler(handler)
        if not self.project_name or not self.log_dir:
            # No project context yet
            self.logger.addHandler(logging.NullHandler())
            return
        # Determine log file name using UTC timestamp
        ts = datetime.datetime.utcnow().strftime("%Y%m%d%H%M%S")
        log_path = os.path.join(self.log_dir, f"{self.project_name}_{ts}.log")
        handler = logging.FileHandler(log_path, mode="a", encoding="utf-8")
        handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
        self.logger.addHandler(handler)

    def _rotate_log(self) -> None:
        """
        Rotate the current log file by closing the existing handler and
        creating a new one with a fresh timestamp.  This is invoked
        on each save to ensure versioned logs are maintained.  The
        previous log file remains in place and is not overwritten.
        """
        # Determine backup path of current log file and copy it
        # to the backups directory.  Then create a new log file.
        if not self.log_dir or not self.project_name:
            return
        # Copy current log handler file to backups if exists
        current_handler = None
        for handler in self.logger.handlers:
            if isinstance(handler, logging.FileHandler):
                current_handler = handler
                break
        if current_handler is not None:
            try:
                current_path = current_handler.baseFilename
                # Construct backup filename with timestamp
                ts = datetime.datetime.utcnow().strftime("%Y%m%d%H%M%S")
                backup_log = os.path.join(self.backup_dir, os.path.basename(current_path))
                # If backup already exists, append timestamp
                if os.path.exists(backup_log):
                    backup_log = os.path.join(self.backup_dir, f"{self.project_name}_{ts}.log")
                import shutil
                shutil.copy2(current_path, backup_log)
                # Write to current log that it was backed up
                current_handler.close()
            except Exception:
                pass
            finally:
                # Remove current handler
                try:
                    self.logger.removeHandler(current_handler)
                except Exception:
                    pass
        # Create a new log file
        ts = datetime.datetime.utcnow().strftime("%Y%m%d%H%M%S")
        new_log_path = os.path.join(self.log_dir, f"{self.project_name}_{ts}.log")
        new_handler = logging.FileHandler(new_log_path, mode="a", encoding="utf-8")
        new_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
        self.logger.addHandler(new_handler)
        # Inform in the new log about the backup
        self.logger.info(f"Previous log backed up to {self.backup_dir}")

    def autosave(self) -> None:
        """Automatically save the current project without prompting the user."""
        try:
            self.save_project(auto=True)
        except Exception:
            pass

    def _on_close_app(self) -> None:
        """Handle closing the main application window."""
        try:
            # Save changes before exiting
            self.autosave()
        finally:
            self.destroy()

    # --- Window positioning and sizing ---
    def _centre_main_window(self) -> None:
        """Centre the main application window on the primary display.

        Computes half of the screen width and height (with minimum widths/heights) and
        positions the window accordingly.  Sets a minimum size to prevent collapsing.
        """
        try:
            screen_w = self.winfo_screenwidth()
            screen_h = self.winfo_screenheight()
            width = max(int(screen_w * 0.5), 800)
            height = max(int(screen_h * 0.5), 600)
            x = (screen_w - width) // 2
            y = (screen_h - height) // 2
            self.geometry(f"{width}x{height}+{x}+{y}")
            self.minsize(800, 600)
        except Exception:
            # Fallback to a fixed size if screen info cannot be obtained
            self.geometry("1000x700")
            self.minsize(800, 600)

    def _resource_path(self, filename: str) -> str:
        """Return absolute path to resource, handling PyInstaller's bundle mode.

        When the application is frozen by PyInstaller, data files are stored in
        a temporary directory accessible via `sys._MEIPASS`.  Otherwise,
        files are located relative to the current file's directory.
        """
        try:
            base_path = getattr(sys, '_MEIPASS', os.path.dirname(__file__))
        except Exception:
            base_path = os.path.dirname(__file__)
        return os.path.join(base_path, filename)

    # --- File operations ---
    def save_project(self, auto: bool = False) -> None:
        """
        Save current project to the project's data directory and write a plain
        text backup.  If auto is False and no project is defined, prompt
        the user for a location.  On auto save with a defined project,
        the user is not prompted and no message box is shown.
        """
        # Update summary
        self.data["summary"] = self.summary_text.get("1.0", "end").strip()
        # Determine save paths
        if self.project_root and self.project_name:
            json_path = os.path.join(self.data_dir, f"{self.project_name}.json")
            txt_path = os.path.join(self.data_dir, f"{self.project_name}.txt")
        else:
            if auto:
                # No project context; skip auto save
                return
            # Manual save: ask user for file path
            json_path = filedialog.asksaveasfilename(
                defaultextension=".json", title="Save Project",
                filetypes=[("JSON", "*.json"), ("All files", "*.*")]
            )
            if not json_path:
                return
            txt_path = os.path.splitext(json_path)[0] + ".txt"
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(json_path), exist_ok=True)
            # Write JSON
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)
            # Write plain text backup
            with open(txt_path, "w", encoding="utf-8") as f:
                f.write("PYWRITER_BACKUP_VERSION:1\n")
                f.write(f"Project Type: {self.data['project_type']}\n\n")
                # Summary
                f.write("Summary:\n")
                f.write(self.data.get("summary", "") + "\n\n")
                # Write each section
                def write_section(label: str, entries: List[Dict[str, Any]]) -> None:
                    if not entries:
                        return
                    for entry in entries:
                        ent_id = entry.get("id", "")
                        created = entry.get("created", "")
                        f.write(f"#ENTITY:{label} id={ent_id} created={created}\n")
                        for q, a in entry.get("answers", {}).items():
                            a_clean = a.replace("\n", " ").strip()
                            f.write(f"{q}: {a_clean}\n")
                        if "progress_index" in entry:
                            f.write(f"ProgressIndex: {entry.get('progress_index')}\n")
                        if "complete" in entry:
                            f.write(f"Complete: {bool(entry.get('complete'))}\n")
                        notes = entry.get("notes")
                        if notes:
                            f.write("Notes:\n")
                            for note in notes:
                                ts = note.get("timestamp", "")
                                content = note.get("content", "")
                                f.write(f"[{ts}] {content}\n")
                        # Write links if present
                        links = entry.get("links")
                        if links:
                            f.write("Links:\n")
                            for lid in links:
                                f.write(f"{lid}\n")
                        f.write("\n")
                write_section("Character", self.data.get("characters", []))
                write_section("Setting", self.data.get("settings", []))
                write_section("History", self.data.get("history", []))
                write_section("Topic", self.data.get("topics", []))
            # Rotate log if we have a project
            if self.project_root and self.project_name:
                self._rotate_log()
                self.logger.info(f"Project autosaved to {json_path}")
            if not auto:
                messagebox.showinfo("Saved", f"Project saved to:\n{json_path}\nBackup saved to:\n{txt_path}")
        except Exception as exc:
            if not auto:
                messagebox.showerror("Save failed", str(exc))

    def load_project(self) -> None:
        """Load project from a JSON file."""
        fpath = filedialog.askopenfilename(
            title="Load Project",
            filetypes=[("JSON and Text", "*.json *.txt"), ("All files", "*.*")]
        )
        if not fpath:
            return
        try:
            # Autosave current project if any
            if self.project_root and any(self.data.get(key) for key in ["characters", "settings", "history", "topics"]):
                self.autosave()
            # Determine format
            if fpath.lower().endswith(".txt"):
                # Loading from plain text backup; project name is derived from filename
                base_name = os.path.splitext(os.path.basename(fpath))[0]
                project_name = base_name
                proj_root = os.path.dirname(os.path.dirname(fpath))
                # If the parent directory is not 'data', use the file's directory as project root
                if os.path.basename(os.path.dirname(fpath)) != "data":
                    proj_root = os.path.dirname(fpath)
                self.project_name = project_name
                self.project_root = proj_root
                self.data_dir = os.path.join(proj_root, "data")
                self.log_dir = os.path.join(proj_root, "logs")
                self.backup_dir = os.path.join(proj_root, "backups")
                # Ensure directories exist
                os.makedirs(self.data_dir, exist_ok=True)
                os.makedirs(self.log_dir, exist_ok=True)
                os.makedirs(self.backup_dir, exist_ok=True)
                # Rotate existing logs
                self._setup_logging()
                self._rotate_log()
                # Load from backup file
                self._load_from_backup(fpath)
            else:
                # Loading from JSON; determine project root and name
                project_name = os.path.splitext(os.path.basename(fpath))[0]
                proj_root = os.path.dirname(os.path.dirname(fpath))
                if os.path.basename(os.path.dirname(fpath)) != "data":
                    proj_root = os.path.dirname(fpath)
                self.project_name = project_name
                self.project_root = proj_root
                self.data_dir = os.path.join(proj_root, "data")
                self.log_dir = os.path.join(proj_root, "logs")
                self.backup_dir = os.path.join(proj_root, "backups")
                os.makedirs(self.data_dir, exist_ok=True)
                os.makedirs(self.log_dir, exist_ok=True)
                os.makedirs(self.backup_dir, exist_ok=True)
                # Rotate logs
                self._setup_logging()
                self._rotate_log()
                # Load JSON
                with open(fpath, "r", encoding="utf-8") as f:
                    loaded = json.load(f)
                # Normalise structure
                self.data = self._normalise_structure(loaded)
            # Set project type variable
            self.project_type.set(self.data.get("project_type", "Fiction"))
            # Update summary
            self.summary_text.delete("1.0", "end")
            self.summary_text.insert("1.0", self.data.get("summary", ""))
            # Refresh trees
            self._refresh_all()
            self.logger.info(f"Loaded project from {fpath}")
            messagebox.showinfo("Loaded", f"Project loaded from {fpath}")
        except Exception as exc:
            messagebox.showerror("Load failed", str(exc))

    def _load_from_backup(self, txt_path: str) -> None:
        """Load project data from a plain text backup file.

        This parser expects a deterministic format created by save_project():

          PYWRITER_BACKUP_VERSION:1
          Project Type: <type>

          Summary:
          <summary lines>

          #ENTITY:<Label> id=<id> created=<timestamp>
          Question: Answer
          ...

        Each entry is terminated by a blank line.  Unknown sections are
        ignored.  Entries are appended to the corresponding list in
        self.data.
        """
        with open(txt_path, "r", encoding="utf-8") as f:
            lines = [line.rstrip("\n") for line in f]
        # Reset data
        self.data = {
            "project_type": "Fiction",
            "summary": "",
            "characters": [],
            "settings": [],
            "history": [],
            "topics": []
        }
        i = 0
        # Check version header
        if i < len(lines) and lines[i].startswith("PYWRITER_BACKUP_VERSION:"):
            # Could parse version if needed
            i += 1
        # Project type
        if i < len(lines) and lines[i].startswith("Project Type:"):
            self.data["project_type"] = lines[i].split(":", 1)[1].strip() or "Fiction"
            i += 1
        # Skip blank lines
        while i < len(lines) and not lines[i].strip():
            i += 1
        # Summary header
        if i < len(lines) and lines[i].startswith("Summary:"):
            i += 1
            summary_lines = []
            while i < len(lines) and not lines[i].startswith("#ENTITY:"):
                summary_lines.append(lines[i])
                i += 1
            self.data["summary"] = "\n".join(summary_lines).strip()
        # Now parse entities
        current_label: Optional[str] = None
        current_entry: Optional[Dict[str, Any]] = None
        in_notes = False
        in_links = False
        while i < len(lines):
            line = lines[i]
            if line.startswith("#ENTITY:"):
                # Finish previous entry
                if current_label and current_entry:
                    self._append_entity(current_label, current_entry)
                # Parse new entry header
                parts = line[len("#ENTITY:"):].split()
                label = parts[0]
                ent_id = ""
                created = ""
                for part in parts[1:]:
                    if part.startswith("id="):
                        ent_id = part.split("=", 1)[1]
                    elif part.startswith("created="):
                        created = part.split("=", 1)[1]
                current_label = label
                current_entry = {"id": ent_id, "created": created, "answers": {}, "notes": []}
                in_notes = False
                in_links = False
            elif current_entry is not None and line:
                # Within an entry
                if line.startswith("Notes:"):
                    in_notes = True
                    in_links = False
                elif line.startswith("Links:"):
                    in_links = True
                    in_notes = False
                elif line.startswith("ProgressIndex:"):
                    try:
                        current_entry["progress_index"] = int(line.split(":", 1)[1].strip())
                    except Exception:
                        current_entry["progress_index"] = 0
                elif line.startswith("Complete:"):
                    val = line.split(":", 1)[1].strip().lower()
                    current_entry["complete"] = val == "true"
                elif in_notes:
                    # Note line, format: [timestamp] content
                    if line.startswith("[") and "]" in line:
                        ts, content = line.split("]", 1)
                        ts = ts.strip("[] ")
                        content = content.strip()
                        current_entry.setdefault("notes", []).append({"timestamp": ts, "content": content})
                    else:
                        # No timestamp, treat whole line as content
                        current_entry.setdefault("notes", []).append({"timestamp": "", "content": line.strip()})
                elif in_links:
                    # Links section: each line is an entity id
                    link_id = line.strip()
                    if link_id:
                        current_entry.setdefault("links", []).append(link_id)
                else:
                    # Parse Q/A line
                    if ":" in line:
                        q, a = line.split(":", 1)
                        current_entry["answers"][q.strip()] = a.strip()
            else:
                # Blank line ends current entry
                if current_label and current_entry:
                    self._append_entity(current_label, current_entry)
                    current_label = None
                    current_entry = None
                    in_notes = False
            i += 1
        # Append last entry
        if current_label and current_entry:
            self._append_entity(current_label, current_entry)

    def _append_entity(self, label: str, entry: Dict[str, Any]) -> None:
        """Append a parsed entity to the correct section in self.data."""
        # Normalise label to section key
        mapping = {
            "Character": "characters",
            "Setting": "settings",
            "History": "history",
            "Timeline": "history",
            "Topic": "topics",
            "Topics": "topics"
        }
        section = mapping.get(label)
        if section:
            # Ensure answers dict exists
            # Ensure answers dict exists
            if "answers" not in entry:
                entry["answers"] = {}
            # Fallback id
            if not entry.get("id"):
                entry["id"] = f"{section[:-1]}-{uuid.uuid4().hex[:8]}"
            # Fallback created
            if not entry.get("created"):
                entry["created"] = datetime.datetime.utcnow().isoformat()
            # Normalise optional fields: notes, progress_index, complete, links
            if "notes" not in entry or not isinstance(entry.get("notes"), list):
                entry["notes"] = []
            if "progress_index" not in entry:
                entry["progress_index"] = 0
            if "complete" not in entry:
                entry["complete"] = False
            if "links" not in entry or not isinstance(entry.get("links"), list):
                entry["links"] = []
            self.data[section].append(entry)

    def _normalise_structure(self, loaded: Dict[str, Any]) -> Dict[str, Any]:
        """Ensure loaded JSON conforms to the new data model.

        Converts old style lists of answer dicts into structured entries with
        id and created fields.  Also removes unsupported sections like
        screenplay.
        """
        data = {
            "project_type": loaded.get("project_type", "Fiction"),
            "summary": loaded.get("summary", ""),
            "characters": [],
            "settings": [],
            "history": [],
            "topics": []
        }
        for key in ["characters", "settings", "history", "topics"]:
            entries = loaded.get(key, [])
            for entry in entries:
                if isinstance(entry, dict) and "answers" in entry:
                    # Already structured
                    new_entry = {
                        "id": entry.get("id", f"{key[:-1]}-{uuid.uuid4().hex[:8]}"),
                        "created": entry.get("created", datetime.datetime.utcnow().isoformat()),
                        "answers": entry.get("answers", {}),
                        "notes": entry.get("notes", []),
                        "progress_index": entry.get("progress_index", 0),
                        "complete": entry.get("complete", False),
                        # Ensure links field exists; cast to list if missing
                        "links": entry.get("links", []) if isinstance(entry.get("links", []), list) else []
                    }
                else:
                    # Old style: entry is a dict of question->answer
                    new_entry = {
                        "id": f"{key[:-1]}-{uuid.uuid4().hex[:8]}",
                        "created": datetime.datetime.utcnow().isoformat(),
                        "answers": entry if isinstance(entry, dict) else {},
                        "notes": [],
                        "progress_index": 0,
                        "complete": False,
                        "links": []
                    }
                data[key].append(new_entry)
        return data

    # --- External actions ---
    def _external_action(self, action: str) -> None:
        """
        Perform external actions for donate, feedback and bug report.  Opens
        the corresponding web page using the default browser.  For bug
        reports, the diagnostics text is automatically copied to the clipboard
        before the browser is opened so the user can paste it into their
        report.  If no specific action is recognised, a placeholder message
        is shown.
        """
        urls = {
            "donate": "https://paypal.me/sharxbyte",
            "feedback": "https://discord.com/channels/1004764481307545731/1461203257845350604",
            "bug": "https://discord.com/channels/1004764481307545731/1227670757195255808"
        }
        url = urls.get(action)
        if action == "bug":
            # Copy diagnostics to clipboard so user can include it in bug report
            lines = []
            lines.append(f"Application version: 0.8.0")
            lines.append(f"Python version: {self.capabilities.get('python_version')}")
            lines.append(f"Operating system: {self.capabilities.get('os')}")
            lines.append(f"Frozen executable: {self.capabilities.get('frozen')}")
            for mod, ver in self.capabilities.get("module_versions", {}).items():
                status = "present" if ver else "missing"
                ver_str = ver or "N/A"
                lines.append(f"{mod}: {status} (version: {ver_str})")
            lines.append(f"TTS: {self.capabilities.get('tts_available')}  |  STT: {self.capabilities.get('stt_available')}  |  Pillow: {self.capabilities.get('pillow_available')}")
            diag = "\n".join(lines)
            try:
                self.clipboard_clear()
                self.clipboard_append(diag)
            except Exception:
                pass
        if url:
            try:
                webbrowser.open(url)
            except Exception:
                messagebox.showinfo(action.capitalize(), f"Open this link in your browser:\n{url}")
        else:
            messagebox.showinfo(action.capitalize(), "This feature is not available.")

    # ---------------------------------------------------------------------
    # Dependency audit and diagnostics
    #
    def _perform_dependency_audit(self) -> Dict[str, Any]:
        """
        Check for the presence of optional third‑party modules and record
        platform information.  Hard requirements (Tkinter, Python version) are
        implicitly satisfied if this code is executing.  If future hard
        requirements are added, this function should exit gracefully.

        Returns a dictionary with keys:

            tts_available: True if pyttsx3 is importable and initialises
            stt_available: True if speech_recognition and a microphone class
                are importable
            pillow_available: True if Pillow's Image classes are importable
            frozen: True if running in a bundled executable (via PyInstaller)
            python_version: str for Python version
            os: Operating system name
            module_versions: dict mapping module names to version strings

        If a hard requirement is missing, a user‑friendly error message will
        be shown and the application will exit.
        """
        report: Dict[str, Any] = {}
        # Basic environment info
        report["python_version"] = platform.python_version()
        report["os"] = platform.system() + " " + platform.release()
        report["frozen"] = bool(getattr(sys, "frozen", False))

        module_versions: Dict[str, Optional[str]] = {}

        # Helper to detect module and version
        def check_module(name: str) -> bool:
            if importlib.util.find_spec(name) is not None:
                try:
                    module_versions[name] = importlib.metadata.version(name)
                except Exception:
                    module_versions[name] = "unknown"
                return True
            module_versions[name] = None
            return False

        # Optional dependencies
        tts_ok = check_module("pyttsx3")
        stt_ok = check_module("SpeechRecognition") or check_module("speech_recognition")
        pillow_ok = check_module("Pillow") or check_module("PIL")

        report["tts_available"] = tts_ok
        report["stt_available"] = stt_ok
        report["pillow_available"] = pillow_ok
        report["module_versions"] = module_versions

        # Initialise optional engines if they are available.  Use globals
        # defined at module level so InterviewWindow can access them without
        # re‑importing heavy modules.  Use try blocks to avoid raising
        # exceptions here; if initialisation fails, treat module as
        # unavailable and log a warning.
        global tts_engine, recognizer, microphone
        if tts_ok and pyttsx3 is not None:
            try:
                tts_engine = pyttsx3.init()
            except Exception:
                report["tts_available"] = False
                tts_engine = None
        if stt_ok and sr is not None:
            try:
                recognizer = sr.Recognizer()
                microphone = sr.Microphone() if hasattr(sr, "Microphone") else None
            except Exception:
                report["stt_available"] = False
                recognizer = None
                microphone = None

        # Hard requirements can be added here in future.  If a requirement is
        # missing, display error and exit gracefully.  For now, Tkinter and
        # standard library modules are assumed present.
        return report

    def show_diagnostics(self) -> None:
        """Display a diagnostics window with environment and dependency info."""
        lines = []
        lines.append(f"Application version: 0.8.0")
        lines.append(f"Python version: {self.capabilities.get('python_version')}")
        lines.append(f"Operating system: {self.capabilities.get('os')}")
        lines.append(f"Frozen executable: {self.capabilities.get('frozen')}")
        lines.append("\nModule availability:")
        for mod, ver in self.capabilities.get("module_versions", {}).items():
            status = "present" if ver else "missing"
            ver_str = ver or "N/A"
            lines.append(f"  - {mod}: {status} (version: {ver_str})")
        lines.append("\nVoice capabilities:")
        lines.append(f"  - Text‑to‑speech available: {self.capabilities.get('tts_available')}")
        lines.append(f"  - Speech‑to‑text available: {self.capabilities.get('stt_available')}")
        lines.append(f"  - Pillow available: {self.capabilities.get('pillow_available')}")
        diagnostics_text = "\n".join(lines)
        # Copy to clipboard for convenience
        try:
            self.clipboard_clear()
            self.clipboard_append(diagnostics_text)
        except Exception:
            pass
        # Show in a simple dialog
        messagebox.showinfo("Diagnostics", diagnostics_text)


def main() -> None:
    app = PyWriterAdvanced()
    app.mainloop()


if __name__ == "__main__":
    main()
