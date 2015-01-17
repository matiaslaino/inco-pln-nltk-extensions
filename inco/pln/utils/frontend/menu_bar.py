from Tkinter import Menu, Toplevel, StringVar
import tkFileDialog
from ttk import *

__author__ = 'Matias'


class MenuBar:
    def open_configuration(self):
        filewin = Toplevel(self.parent)
        filewin.wm_title('Configuration')

        i = 0

        label = Label(filewin, text="Configure path to binaries")
        label.grid(row=i, column=0)
        i += 1

        label = Label(filewin, text="FreeLing")
        label.grid(row=i, column=0)
        entry_freeling = Entry(filewin, width=100, textvariable=self.var_freeling_path)
        entry_freeling.grid(row=i, column=1)
        control = Button(filewin, text="Browse...", command=self.browse_freeling)
        control.grid(row=1, column=2)
        i += 1

        label = Label(filewin, text="TreeTagger")
        label.grid(row=i, column=0)
        entry_treetagger = Entry(filewin, width=100, textvariable=self.var_treetagger_path)
        entry_treetagger.grid(row=i, column=1)
        control = Button(filewin, text="Browse...", command=self.browse_treetagger)
        control.grid(row=i, column=2)
        i += 1

        label = Label(filewin, text="MaltParser")
        label.grid(row=i, column=0)
        entry_maltparser = Entry(filewin, width=100, textvariable=self.var_maltparser_path)
        entry_maltparser.grid(row=i, column=1)
        control = Button(filewin, text="Browse...", command=self.browse_maltparser)
        control.grid(row=i, column=2)
        i += 1

        label = Label(filewin, text="Spanish model")
        label.grid(row=i, column=0)
        entry_maltparser_model = Entry(filewin, width=100, textvariable=self.var_maltparser_model_path)
        entry_maltparser_model.grid(row=i, column=1)
        control = Button(filewin, text="Browse...", command=self.browse_maltparser_model)
        control.grid(row=i, column=2)
        i += 1

        control = Button(filewin, text="Apply")
        control.grid(row=i, columnspan=2)


    def browse_freeling(self):
        filename = tkFileDialog.askopenfilename(filetypes=(("Windows executable files", "*.exe"),
                                                           ("All files", "*.*")))
        self.var_freeling_path.set(filename)


    def browse_maltparser(self):
        filename = tkFileDialog.askopenfilename(filetypes=(("JAR files", "*.jar"),
                                                           ("All files", "*.*")))
        self.var_maltparser_path.set(filename)


    def browse_maltparser_model(self):
        filename = tkFileDialog.askopenfilename(filetypes=(("MaltParser model files", "*.mco"),
                                                           ("All files", "*.*")))
        self.var_maltparser_model_path.set(filename)


    def browse_treetagger(self):
        filename = tkFileDialog.askopenfilename(filetypes=(("Batch files", "*.bat"),
                                                           ("All files", "*.*")))
        self.var_treetagger_path.set(filename)

    def __init__(self, parent):
        self.parent = parent

        menubar = Menu(self.parent)
        menubar.add_command(label="Configuration", command=self.open_configuration)

        self.var_freeling_path = StringVar()
        self.var_maltparser_path = StringVar()
        self.var_maltparser_model_path = StringVar()
        self.var_treetagger_path = StringVar()

        parent.config(menu=menubar)
