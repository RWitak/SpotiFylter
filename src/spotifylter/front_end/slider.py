import tkinter as tk
from typing import Callable, Any

from RangeSlider.RangeSlider import RangeSliderH

from spotifylter import colors


class Slider(RangeSliderH):
    callback: Callable[..., Any]
    bar_left: tk.DoubleVar
    bar_right: tk.DoubleVar

    def __init__(self,
                 master,
                 variables: tuple[tk.DoubleVar, tk.DoubleVar]):

        self.bar_left, self.bar_right = variables

        super().__init__(master,
                         variables,
                         line_width=3,
                         bar_radius=8,
                         font_family="Helvetica Neue",
                         font_size=12,
                         padX=30,
                         Height=63,
                         valueSide='BOTTOM',
                         bgColor=colors.BLACK,
                         bar_color_outer=colors.GREEN,
                         bar_color_inner=colors.WHITE,
                         line_color=colors.WHITE,
                         line_s_color=colors.GREEN,
                         digit_precision='.2f')
        self.canv.config(highlightcolor=colors.WHITE)

    def print_values(self, *_):
        print(f"{self.bar_left.get()}, {self.bar_right.get()}")

    # noinspection PyPep8Naming
    # noinspection PyUnboundLocalVariable
    def _RangeSliderH__addBar(self, pos, tempIdx=None):
        """OVERRIDES PARENT METHOD TO ADD TEXT COLOR.
        @ pos: position of the bar, ranged from (0,1)"""
        if pos < 0 or pos > 1:
            raise Exception("Pos error - Pos: " + str(pos))
        if self.draw == 'auto':
            R = RangeSliderH.BAR_RADIUS
            r = RangeSliderH.BAR_RADIUS_INNER
            L = self.canv_W - 2 * self.slider_x
            y = self.slider_y
            x = self.slider_x + pos * L
            id_outer = self.canv.create_oval(x - R, y - R, x + R, y + R, fill=RangeSliderH.BAR_COLOR_OUTTER, width=2,
                                             outline="")
            id_inner = self.canv.create_oval(x - r, y - r, x + r, y + r, fill=RangeSliderH.BAR_COLOR_INNER, outline="")
            if self.show_value:
                if self.valueSide == 'TOP':
                    y_value = y - RangeSliderH.BAR_RADIUS - RangeSliderH.FONT_SIZE / 2
                    value = pos * (self.max_val - self.min_val) + self.min_val
                    id_value = self.canv.create_text(x, y_value, anchor=tk.S,
                                                     text=format(value, RangeSliderH.DIGIT_PRECISION) + self.suffix,
                                                     font=(RangeSliderH.FONT_FAMILY, RangeSliderH.FONT_SIZE),
                                                     fill=colors.WHITE)
                elif self.valueSide == 'BOTTOM':
                    y_value = y + RangeSliderH.BAR_RADIUS + RangeSliderH.FONT_SIZE / 2
                    value = pos * (self.max_val - self.min_val) + self.min_val
                    id_value = self.canv.create_text(x, y_value, anchor=tk.N,
                                                     text=format(value, RangeSliderH.DIGIT_PRECISION) + self.suffix,
                                                     font=(RangeSliderH.FONT_FAMILY, RangeSliderH.FONT_SIZE),
                                                     fill=colors.WHITE)
                else:
                    raise Exception("valueSide can either be TOP or BOTTOM")
                return [id_outer, id_inner, id_value]
            else:
                return [id_outer, id_inner]
        elif self.draw == 'image':
            L = self.canv_W - 2 * self.slider_x
            y = self.slider_y
            x = self.slider_x + pos * L
            if tempIdx == 0:
                imageH = self.canv.create_image(x, y, anchor=RangeSliderH.IMAGE_ANCHOR_L, image=self.ImageL)
            elif tempIdx == 1:
                imageH = self.canv.create_image(x, y, anchor=RangeSliderH.IMAGE_ANCHOR_R, image=self.ImageR)
            if self.show_value:
                if self.valueSide == 'TOP':
                    y_value = y - self.ImageL.height() / 2 - RangeSliderH.FONT_SIZE / 2
                    value = pos * (self.max_val - self.min_val) + self.min_val
                    id_value = self.canv.create_text(x, y_value, anchor=tk.S,
                                                     text=format(value, RangeSliderH.DIGIT_PRECISION) + self.suffix,
                                                     font=(RangeSliderH.FONT_FAMILY, RangeSliderH.FONT_SIZE),
                                                     fill=colors.WHITE)
                elif self.valueSide == 'BOTTOM':
                    y_value = y + self.ImageL.height() / 2 + RangeSliderH.FONT_SIZE / 2
                    value = pos * (self.max_val - self.min_val) + self.min_val
                    id_value = self.canv.create_text(x, y_value, anchor=tk.N,
                                                     text=format(value, RangeSliderH.DIGIT_PRECISION) + self.suffix,
                                                     font=(RangeSliderH.FONT_FAMILY, RangeSliderH.FONT_SIZE),
                                                     fill=colors.WHITE)
                else:
                    raise Exception("valueSide can either be TOP or BOTTOM")
                return [imageH, id_value]
            else:
                return [imageH]

    # noinspection PyPep8Naming
    # noinspection PyUnboundLocalVariable,PyShadowingBuiltins
    def _RangeSliderH__checkSelection(self, x, y):
        """
        OVERRIDES PARENT METHOD TO BRANCH BEHAVIOUR FOR OVERLAPPING BARS.
        To check if the position is inside the bounding rectangle of a Bar
        Return [True, bar_index] or [False, None]
        """
        selected_indices = []

        for idx in range(len(self.bars)):
            id = self.bars[idx]["Ids"][0]
            bbox = self.canv.bbox(id)
            if bbox[0] < x < bbox[2] and bbox[1] < y < bbox[3]:
                selected_indices.append(idx)

        if len(selected_indices) == 1:
            return [True, selected_indices[0]]
        if len(selected_indices) == 2:
            return [True, self.__pick_bar(selected_indices, x)]
        else:
            return [False, None]

    def __pick_bar(self, selected_indices, x):
        pos = self._RangeSliderH__calcPos(x)
        left_d = pos - self.min_val
        right_d = self.max_val - pos
        if left_d > right_d:
            return min(selected_indices)
        else:
            return max(selected_indices)
