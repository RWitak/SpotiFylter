import tkinter as tk
from multiprocessing.connection import Connection
from tkinter import font as tk_font

from spotifylter import colors
from spotifylter.front_end.sliders import Sliders
from spotifylter.front_end.tk_root import Root


def set_up_window(_root: Root, pipe_sender: Connection = None):
    _root.title("Spotify Filter")
    _root.config(padx=25, pady=10)
    _font = tk_font.Font(name="Helvetica Neue", size=24, weight="bold")
    tk.Label(
        _root,
        text="Filter current playback",
        font=_font,
        pady=20,
        fg=colors.WHITE,
        bg=colors.BLACK
    ).pack()

    Sliders(master=_root, sender=pipe_sender, pady=15, bg=colors.BLACK)

    _root.mainloop()


def start_gui(pipe_sender: Connection):
    root = Root()
    set_up_window(root, pipe_sender=pipe_sender)
    root.mainloop()
