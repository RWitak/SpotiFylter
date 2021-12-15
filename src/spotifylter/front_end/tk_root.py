import tkinter as tk

from spotifylter import colors


class Root(tk.Tk):
    frm: tk.Frame

    def __init__(self):
        super().__init__()
        self.config(background=colors.BLACK)
