"""
Plotting using matplotlib and Tkinter.

Matplotlib does all the 2D graphics for Sage, but unfortunately none
of its GUI backends are compiled by default.  See the README file for
how to enable the Tk backend.  
"""

# Load Tkinter
import sys, os
import tkinter as Tk
import tkinter.ttk as ttk

# Load MatplotLib
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.backends.backend_tkagg as backend

class MatplotFigure:
    def __init__(self, add_subplot=True, root=None, **kwargs):
        args = kwargs
        figure = matplotlib.pyplot.figure(figsize=(10,6), dpi=100)
        figure.set_facecolor('white')
        axis = figure.add_subplot(111) if add_subplot else None
        self.figure, self.axis = figure, axis
        
        window = Tk.Tk() if root is None else Tk.Toplevel(root)
        figure_frame = ttk.Frame(window)
        canvas = backend.FigureCanvasTkAgg(figure, master=figure_frame)
        canvas._tkcanvas.config(highlightthickness=0, width=1000, height=600)
        toolbar = backend.NavigationToolbar2Tk(canvas, figure_frame)
        toolbar.pack(side=Tk.TOP, fill=Tk.X)
        canvas._tkcanvas.pack(side=Tk.TOP,  fill=Tk.BOTH, expand=1)
        toolbar.update()
        
        figure_frame.grid(column=0, row=0, sticky=(Tk.N, Tk.S, Tk.E, Tk.W))
        window.columnconfigure(0, weight=1)
        window.rowconfigure(0, weight=1)
        self.window, self.canvas, self.toolbar = window, canvas, toolbar
        self.figure_frame = figure_frame

    def draw(self):
        self.canvas.draw()

    def clear(self):
        self.axis.clear()
        self.draw()
        

if __name__ == "__main__":
    from numpy import arange, sin, pi
    MF = MatplotFigure()
    t = arange(0.0,3.0,0.01)
    s = sin(2*pi*t)
    ans = MF.axis.plot(t,s)
    Tk.mainloop()
