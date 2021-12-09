from tkinter import *
from tkinter import ttk

from features import features
from slider import Slider


class Sliders(ttk.Frame):
    feature_bounds: dict

    def __init__(self, **kw):
        super().__init__(**kw)
        #
        self.feature_bounds = {feature: {'range': limits, 'bound': (DoubleVar(), DoubleVar())}
                               for feature, limits in features.items()}

        for feature, values in self.feature_bounds.items():
            values['bound'][0].set(values['range'][0])
            values['bound'][1].set(values['range'][1])
            ttk.Label(self,
                      text=feature.capitalize(),
                      font="Arial 10 bold"
                      ).pack(side=TOP)
            slider = Slider(self, (values['bound'][0], values['bound'][1]))
            slider.bar_left.trace_add('write', slider.set_vals)
            slider.bar_right.trace_add('write', slider.set_vals)

        self.pack()


    def set_feature_bounds(self, feature_bounds):
        self.feature_bounds = feature_bounds
