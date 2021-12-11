import threading
from tkinter import *
from tkinter import font

import colors
from sliders import Sliders
from spotifylter.features import FEATURE_BOUNDS
from spotifylter.main import get_client, Skipper


class Root(Tk):
    frm: Frame

    def __init__(self):
        super().__init__()
        self.config(background=colors.BLACK)


def set_up_window(_root: Root):
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

    Sliders(master=_root)

    _root.mainloop()


if __name__ == '__main__':
    # TODO: Multi-threading. A: tk mainloop, B: skipping loop
    feature_bounds = FEATURE_BOUNDS.copy()

    spotipy_client = get_client()
    skipper = Skipper(spotipy_client)
    back_end = threading.Thread(name="Back-End", target=skipper.skip_unwanted)

    root = Root()
    set_up_window(root)
    front_end = threading.Thread(name="Front-End", target=root.mainloop)

    back_end.start()
    front_end.start()
