from tkinter import *
from tkinter import ttk
from tkinter.ttk import Frame



class Root(Tk):
    frm: Frame

    def __init__(self):
        super().__init__()
        self.frm = ttk.Frame(self, padding=50)
        self.frm.pack()

        # ttk.Label(self.frm, text="Filter your current playlist!").grid(column=0, row=0)
        # ttk.Button(self.frm, text="Quit", command=self.destroy).grid(column=0, row=1)



if __name__ == '__main__':
    root = Root()

    from sliders import Sliders
    Sliders(master=root)

    root.mainloop()
