import tkinter as tk
from multiprocessing.connection import Connection
from tkinter import ttk
from typing import Optional

from spotifylter import colors
from spotifylter.features import FEATURE_BOUNDS
from spotifylter.front_end.slider import Slider


class Sliders(tk.Frame):
    sender: Optional[Connection]
    feature_bounds: dict

    def __init__(self, sender: Connection = None, **kw):
        super().__init__(**kw)

        self.sender = sender
        self.feature_bounds = {feature: {'range': limits,
                                         'bound_var': (tk.DoubleVar(name=feature + "_lower"),
                                                       tk.DoubleVar(name=feature + "_upper"))}
                               for feature, limits in FEATURE_BOUNDS.items()}

        self.build_controls()

    def build_controls(self):
        callback = self.bounds_changed

        for feature, values in self.feature_bounds.items():
            left_var, right_var = values['bound_var']
            left_var.set(values['range'][0])
            right_var.set(values['range'][1])

            frame = tk.Frame(self, bg=colors.BLACK, padx=15)

            slider = Slider(master=frame,
                            variables=(left_var, right_var))

            slider.bar_left.trace_add('write', callback)
            slider.bar_right.trace_add('write', callback)

            slider.pack(fill=tk.BOTH, side=tk.RIGHT)
            ttk.Label(frame,
                      text=feature.replace('_', ' ').title(),
                      font="Helvetica_Neue 12 bold",
                      background=colors.BLACK,
                      foreground=colors.WHITE
                      ).pack(side=tk.RIGHT, anchor=tk.NE)

            frame.pack(side=tk.TOP, fill=tk.X)

        self.pack()

    def bounds_changed(self, *_):
        unpacked_fb = {feature: tuple(bound.get() for bound in values['bound_var'])
                       for feature, values in self.feature_bounds.items()}

        self.sender.send(unpacked_fb)
