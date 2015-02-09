__author__ = 'Matias'

from Tkinter import *
root = Tk()
# Button(root, text="A").pack(side=LEFT, expand=YES, fill=Y)
# Button(root, text="B").pack(side=TOP, expand=YES, fill=BOTH)
# Button(root, text="C").pack(side=RIGHT, expand=YES, fill=NONE, anchor=NE)
# Button(root, text="D").pack(side=LEFT, expand=NO, fill=Y)
# Button(root, text="E").pack(side=TOP, expand=NO, fill=BOTH)
# Button(root, text="F").pack(side=RIGHT, expand=NO, fill=NONE)
# Button(root, text="G").pack(side=BOTTOM, expand=YES, fill=Y)
# Button(root, text="H").pack(side=TOP, expand=NO, fill=BOTH)
# Button(root, text="I").pack(side=RIGHT, expand=NO)
# Button(root, text="J").pack(anchor=SE)
#
# Button(root, text="A").pack(side=LEFT, expand=YES, fill=Y)
# Button(root, text="B").pack(side=TOP, expand=YES, fill=Y)

input_text_area = Text(root)
input_text_area.grid(row=1, column=0, columnspan=4, sticky=W+E)
input_text_area.configure(background='#4D4D4D')

Tk.grid_columnconfigure(root, 0, weight=1)

root.mainloop()