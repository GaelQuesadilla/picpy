from tkinter import Misc
from typing import Any
import ttkbootstrap.constants as c

import ttkbootstrap as ttk


class Sidebar(ttk.Frame):
    def __init__(self, master: Misc, padding: int | tuple[int, ...] = 0,  width: int = 200, *args, **kwargs) -> None:
        borderwidth = 10
        super().__init__(master, padding=padding,
                         borderwidth=borderwidth, width=width, *args, **kwargs)


if __name__ == "__main__":
    from picpy.views.globals.window import Window
    app = Window()

    sidebar = Sidebar(app)
    sidebar.config(bootstyle="danger")
    sidebar.pack(side=c.LEFT, fill=c.Y)

    app.mainloop()
