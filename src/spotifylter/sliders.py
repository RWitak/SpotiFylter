from multiprocessing.connection import Connection
from tkinter import *
from tkinter import ttk
from typing import Optional

from spotifylter import colors
from spotifylter.features import FEATURE_BOUNDS
from spotifylter.slider import Slider


class Sliders(Frame):
    sender: Optional[Connection]
    feature_bounds: dict

    def __init__(self, sender: Connection = None, **kw):
        super().__init__(**kw)

        self.sender = sender
        self.feature_bounds = {feature: {'range': limits,
                                         'bound': (DoubleVar(name=feature + "_lower"),
                                                   DoubleVar(name=feature + "_upper"))}
                               for feature, limits in FEATURE_BOUNDS.items()}

        callback = self.bounds_changed

        for feature, values in self.feature_bounds.items():
            values['bound'][0].set(values['range'][0])
            values['bound'][1].set(values['range'][1])
            frame = Frame(self, bg=colors.BLACK, padx=15)
            slider = Slider(frame,
                            (values['bound'][0], values['bound'][1]),
                            lambda: True
                            )
            slider.bar_left.trace_add('write', callback)
            slider.bar_right.trace_add('write', callback)
            slider.pack(fill=BOTH, side=RIGHT)
            ttk.Label(frame,
                      text=feature.replace('_', ' ').title(),
                      font="Helvetica 10 bold",
                      background=colors.BLACK,
                      foreground=colors.WHITE
                      ).pack(side=TOP, anchor="e")
            frame.pack(side=TOP, fill=X)

        self.pack()

    def bounds_changed(self, *args):
        unpacked_fb = {feature: tuple(bound.get() for bound in values['bound'])
                       for feature, values in self.feature_bounds.items()}

        self.sender.send(unpacked_fb)
