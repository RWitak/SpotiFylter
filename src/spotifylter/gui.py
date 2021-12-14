from multiprocessing import Process, Pipe
from multiprocessing.connection import Connection
from tkinter import *
from tkinter import font

from spotifylter import colors
from spotifylter.features import FEATURE_BOUNDS
from spotifylter.main import get_client, Skipper
from spotifylter.sliders import Sliders


class Root(Tk):
    frm: Frame

    def __init__(self):
        super().__init__()
        self.config(background=colors.BLACK)


def set_up_window(_root: Root, pipe_sender: Connection = None):
    _root.title("Spotify Filter")
    _font = font.Font(name="Helvetica Neue", size=24, weight="bold")
    Label(
        _root,
        text="Filter current playback",
        font=_font,
        pady=20,
        fg=colors.WHITE,
        bg=colors.BLACK
    ).pack()

    Sliders(master=_root, sender=pipe_sender)

    _root.mainloop()


def start_gui(pipe_sender: Connection):
    root = Root()
    set_up_window(root, pipe_sender=pipe_sender)
    root.mainloop()


if __name__ == '__main__':
    feature_bounds = FEATURE_BOUNDS.copy()

    receiver, sender = Pipe(duplex=False)

    spotipy_client = get_client()
    skipper = Skipper(spotipy_client, receiver=receiver)
    back_end = Process(name="Back-End", target=skipper.loop)

    front_end = Process(name="Front-End", target=start_gui, args=(sender,))

    back_end.start()
    front_end.start()
