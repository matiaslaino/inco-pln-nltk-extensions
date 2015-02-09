from Tkconstants import RIGHT
from Tkconstants import Y
import Tkinter as tk

__author__ = 'Matias'


class UIUtils:
    @staticmethod
    def set_vertical_scroll(widget):
        """
        :param widget:
        :type widget: tk.Widget
        """

        scroll = tk.Scrollbar(widget, background=UIUtils.background)
        scroll.config(command=widget.yview)
        widget.config(yscrollcommand=scroll.set)

        scroll.pack(side=RIGHT, fill=Y)

    background = '#4D4D4D'
    foreground = '#FFFFFF'