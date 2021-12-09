from tkinter import *
from RangeSlider.RangeSlider import RangeSliderH


class Slider(RangeSliderH):
    label: Label
    bar_left: DoubleVar
    bar_right: DoubleVar

    def __init__(self,
                 master,
                 variables: tuple[DoubleVar, DoubleVar]):
        self.bar_left, self.bar_right = variables
        super().__init__(master,
                         variables,
                         font_size=12,
                         padX=100,
                         Height=63,
                         valueSide='BOTTOM',
                         bgColor="#f0f0f0",
                         digit_precision='.2f')
        self.pack(side=TOP)

    def set_vals(self, *_):
        print(f"{self.bar_left.get()}, {self.bar_right.get()}")
