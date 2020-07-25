#! python3
# Flashcards italiano-tedesco

""" TODO:
    - Divisione per categorie di vocaboli
    - Visualizza errori.
"""

import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilenames
import os
import random
# import sys

WIDTH = 1000  # THERE it is, the abomination: global variables. Yes.
RATIO = 16 / 9
SMALL_FONT = ("Verdana", 12)
MEDIUM_FONT = ("Verdana", 25)
BIG_FONT = ("Verdana", 40)
BUTTON_FONT = ("Verdana", 12)
INITIAL_TEXT = ("Flashcards 0.2\n\n" +
                "Funzionamento: l'applicazione propone un vocabolo.\nPremere barra spaziatrice per mostrare le informazioni rilevanti (traduzione, genere, plurale,...).\n" +
                "Il colore nei sostantivi indica il genere. Specificare se la risposta corrisponde per procedere.\n\n\n")


class FlashCardsApp(tk.Tk):

    def __init__(self, *args, **kwargs):  # args: additional arguments as variables. kwargs: additional arguments ad dictionaries.
        tk.Tk.__init__(self, *args, **kwargs)
        self.geometry("{}x{}".format(WIDTH, int(WIDTH / RATIO)))
        self.resizable(False, False)
        self.title("FlashCards")
        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # Creating styles
        s = ttk.Style()
        s.configure("MyButton.TButton", font=BUTTON_FONT)

        # Setting some variables
        self.right = 0
        self.wrong = 0
        self.words = []

        # Creating all application's frames
        self.frames = {}  # A dictionary of frames, which will constitute pages of the program
        frame = StartPage(self.container, self)
        self.frames[StartPage] = frame  # Add the page to the dict of pages
        frame.grid(row=0, column=0, sticky="nsew")
        self.end_frame = EndPage(self.container, self)
        self.frames[EndPage] = self.end_frame
        self.end_frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
        frame.focus_set()
        self.end_frame.update_points(self.right, self.wrong)

    # Load all words from files into w
    def load_words(self, filenames, shuffle):
        idx = 0
        self.words = []
        # directory = os.listdir()
        for f in filenames:
            # print("Opening", f)
            if os.path.isfile(f) and f.endswith(".txt"):
                file = open(f, "r")
                for line in file:
                    if line.isupper():
                        category = line.strip("\n").lower()
                        continue
                    if category == "nomen":
                        self.words.append(line.strip("\n").split(", "))
                    else:
                        aux = line.strip("\n").split(", ")
                        self.words.append(['0', aux[0], '0', aux[1]])
                    # print(line)
                    self.words[-1].append(category)
                    idx += 1
        # print(self.words)
        if len(self.words) == 0:
            print("No words found. Is the directory right?")
        if shuffle:
            random.shuffle(self.words)
        frame = MainPage(self.container, self)
        self.frames[MainPage] = frame
        frame.grid(row=0, column=0, sticky="nsew")


class StartPage(tk.Frame):
    controller = None

    def file_selection(self):
        filenames = askopenfilenames(initialdir=os.getcwd(), title="Select Files to Open", filetypes=(("Text File", "*.txt"), ("All files", "*.*")))
        self.controller.load_words(filenames, self.shuffle.get())
        print(self.shuffle.get())
        self.controller.show_frame(MainPage)

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        panel = ttk.Frame(self, relief=tk.GROOVE)
        panel.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W + tk.E + tk.N + tk.S)

        label = ttk.Label(panel, text=INITIAL_TEXT, font=SMALL_FONT, justify=tk.CENTER)
        label.pack(padx=10, pady=30)

        # btn = ttk.Button(panel, text="Inizia", style="MyButton.TButton", command=lambda: controller.show_frame(MainPage))
        # btn.pack()
        sel_btn = ttk.Button(panel, text="Inizia", style="MyButton.TButton", command=self.file_selection)
        sel_btn.pack()
        self.shuffle = tk.IntVar()
        tk.Checkbutton(panel, text="Shuffle", variable=self.shuffle).pack()


class MainPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.rowconfigure(0, weight=2)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        self.grid_columnconfigure(3, minsize=WIDTH / 4)
        wordFrame = ttk.Frame(self, relief=tk.GROOVE)
        btnFrame = ttk.Frame(self, relief=tk.GROOVE)
        statFrame = ttk.Frame(self, relief=tk.GROOVE)
        btnFrame.grid(row=0, column=3, padx=5, pady=5, sticky=tk.W + tk.E + tk.N + tk.S)
        wordFrame.grid(row=0, column=0, rowspan=2, columnspan=3, padx=5, pady=5, sticky=tk.W + tk.E + tk.N + tk.S)
        statFrame.grid(row=1, column=3, padx=5, pady=5, sticky=tk.W + tk.E + tk.N + tk.S)

        self.word_index = 0
        label = ttk.Label(wordFrame, text=controller.words[self.word_index][1], font=BIG_FONT, justify=tk.CENTER)
        label.grid(row=0, column=0)
        wordFrame.rowconfigure(0, weight=1)
        wordFrame.columnconfigure(0, weight=1)

        # Functions for buttons and listening
        def button_process(text):
            if str(right_btn["state"]) == "disabled":
                return
            if text == "right" or text == "c":
                controller.right += 1
            elif text == "wrong" or text == "e":
                controller.wrong += 1
            else:
                return
            self.word_index += 1
            try:
                score_label.configure(text="{:.2f}%\n[{}/{}]".format(100 * controller.right / (controller.right + controller.wrong), controller.right, controller.right + controller.wrong))
                label.configure(text=controller.words[self.word_index][1], foreground="#000000")
                right_btn.configure(state=tk.DISABLED)
                wrong_btn.configure(state=tk.DISABLED)
                self.focus_set()
            except IndexError:
                controller.show_frame(EndPage)

        articles = {
            "m": "der",
            "f": "die",
            "n": "das",
            "pl": "die",
            "0": ""
        }

        colors = {
            "m": "#0000cc",
            "f": "#cc0066",
            "n": "#006600",
            "pl": "#cc7a00",
            "0": "#000000"
        }

        def space_bar(event):
            if str(right_btn["state"]) == "disabled":
                # TODO: Flip the card
                txt = ""
                col = "#000000"
                if "0" not in controller.words[self.word_index][0]:
                    txt = articles[controller.words[self.word_index][0]] + " "
                txt += controller.words[self.word_index][1]
                if "0" not in controller.words[self.word_index][2]:
                    txt += ", " + controller.words[self.word_index][2]
                txt += "\n" + controller.words[self.word_index][3]

                if controller.words[self.word_index][0] in colors:
                    col = colors[controller.words[self.word_index][0]]

                label.configure(text=txt, foreground=col)
                right_btn.configure(state=tk.NORMAL)
                wrong_btn.configure(state=tk.NORMAL)

        def key(event):
            if event.char == " ":
                space_bar(event)
            elif event.char == "c" or event.char == "e":
                button_process(event.char)

        self.bind("<Key>", key)
        right_btn = ttk.Button(btnFrame, text="Corretto", underline=0, style="MyButton.TButton", state=tk.DISABLED, command=lambda: button_process("right"))
        right_btn.grid(row=0, column=0)
        wrong_btn = ttk.Button(btnFrame, text="Errato", underline=0, style="MyButton.TButton", state=tk.DISABLED, command=lambda: button_process("wrong"))
        wrong_btn.grid(row=1, column=0)
        end_btn = ttk.Button(btnFrame, text="Termina", style="MyButton.TButton", command=lambda: controller.show_frame(EndPage))
        end_btn.grid(row=2, column=0)
        for row in range(btnFrame.grid_size()[1]):
            btnFrame.rowconfigure(row, weight=1)
        btnFrame.columnconfigure(0, weight=1)
        score_label = ttk.Label(statFrame, text="0%\n[0/0]", font=MEDIUM_FONT, justify=tk.CENTER)
        score_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)


class EndPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.points_label = ttk.Label(self, text="Score = ???", font=BIG_FONT, justify=tk.CENTER)
        self.points_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    def update_points(self, r, w):
        txt = "No registered points"
        if r + w > 0:
            txt = "Score = {:.2f}%\t({}/{})".format(r / (r + w) * 100, r, r + w)
        self.points_label.configure(text=txt)


# print(sys.argv[0])
# os.chdir(os.path.dirname(sys.argv[0]))
app = FlashCardsApp()
app.mainloop()
