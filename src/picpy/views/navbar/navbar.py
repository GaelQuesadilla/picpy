from tkinter import Misc
from typing import Any
import ttkbootstrap.constants as c

import ttkbootstrap as ttk


class Navbar(ttk.Frame):
    def __init__(self, master: Misc, padding: int | tuple[int, ...] = 0,  height: int = 75, *args, **kwargs) -> None:
        borderwidth = 10
        super().__init__(master, padding=padding,
                         borderwidth=borderwidth, height=height, *args, **kwargs)


if __name__ == "__main__":
    from picpy.views.globals.window import Window
    app = Window()

    navbar = Navbar(app)
    navbar.config(bootstyle="danger")
    navbar.pack(side=c.TOP, fill=c.X)

    app.mainloop()
