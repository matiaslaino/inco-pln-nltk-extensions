__author__ = 'Matias'

try:
    import Tkinter  # Python 2
    import ttk
    from Tkconstants import END, INSERT, W, E, S, N, HORIZONTAL
except ImportError:
    import tkinter as Tkinter  # Python 3
    import tkinter.ttk as ttk
    from tkinter.constants import END, INSERT, W, E, S, N, HORIZONTAL

class ProgressDialog:
    # Create Progress Bar
    def __init__(self, parent):
        self.window3 = Tkinter.Toplevel(parent)

        # self.window3.overrideredirect(1)
        self.window3.attributes("-toolwindow", 1)
        self.window3.protocol("WM_DELETE_WINDOW", self.__doNothing)
        self.window3.grab_set()
        self.textoBar = Tkinter.Label(self.window3, text="Doing stuff, please wait")
        self.textoBar.grid(row=0, column=0, pady=(5, 5))
        self.progressbar = ttk.Progressbar(self.window3, orient=HORIZONTAL, mode='indeterminate', length=250)
        self.progressbar.grid(row=1, column=0, pady=(5, 5))
        self.center(self.window3)
        self.progressbar.start()


    # Close Progress Bar
    def close(self):
        self.progressbar.stop()
        self.window3.destroy()

    def __doNothing(self):
        pass

    def center(self, toplevel):
        toplevel.update_idletasks()
        w = toplevel.winfo_screenwidth()
        h = toplevel.winfo_screenheight()
        size = tuple(int(_) for _ in toplevel.geometry().split('+')[0].split('x'))
        x = w/2 - size[0]/2
        y = h/2 - size[1]/2
        toplevel.geometry("%dx%d+%d+%d" % (size + (x, y)))
