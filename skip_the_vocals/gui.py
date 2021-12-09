from tkinter import *
from tkinter import font

import colors
from sliders import Sliders


class Root(Tk):
    frm: Frame

    def __init__(self):
        super().__init__()
        self.config(background=colors.BLACK)


def set_up_window():
    root = Root()
    root.title("Spotify Filter")
    FONT=font.Font(name="Helvetica Neue", size=24, weight="bold")
    Label(root, text="Filter current playback", font=FONT, pady=20, fg=colors.WHITE, bg=colors.BLACK).pack()
    sliders = Sliders(master=root)

    root.mainloop()


if __name__ == '__main__':
    set_up_window()
