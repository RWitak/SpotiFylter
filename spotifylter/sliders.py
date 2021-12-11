from tkinter import *
from tkinter import ttk

import colors
from features import FEATURES
from slider import Slider


class Sliders(Frame):
    feature_bounds: dict

    def __init__(self, **kw):
        super().__init__(**kw)

        self.feature_bounds = {feature: {'range': limits,
                                         'bound': (DoubleVar(name=feature + "_lower"),
                                                   DoubleVar(name=feature + "_upper"))}
                               for feature, limits in FEATURES.items()}

        for feature, values in self.feature_bounds.items():
            values['bound'][0].set(values['range'][0])
            values['bound'][1].set(values['range'][1])
            frame = Frame(self, bg=colors.BLACK, padx=15)
            slider = Slider(frame,
                            (values['bound'][0], values['bound'][1]),
                            )
            slider.bar_left.trace_add('write', slider.set_values)
            slider.bar_right.trace_add('write', slider.set_values)
            slider.pack(fill=BOTH, side=RIGHT)
            ttk.Label(frame,
                      text=feature.replace('_', ' ').title(),
                      font="Helvetica 10 bold",
                      background=colors.BLACK,
                      foreground=colors.WHITE
                      ).pack(side=TOP, anchor="e")
            frame.pack(side=TOP, fill=X)

        self.pack()

    def set_feature_bounds(self, feature_bounds):
        self.feature_bounds = feature_bounds
