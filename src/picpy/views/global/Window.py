from tkinter import Misc
from typing import Any, Callable, Tuple
from picpy.utils.config import project, config, assets
from picpy.utils.logger import logger
from math import sqrt
import ttkbootstrap as ttk


class Window(ttk.Window):
    def __init__(self) -> None:
        phi = (1 + sqrt(5))/2

        theme = config["GUI"]["theme"]
        light_theme = theme + "-light"
        dark_theme = theme + "-dark"
        title = project["project"]["name"]
        iconphoto = str(assets / "logo.png")
        size = (int(700 * phi), 700)
        minsize = (int(500 * phi), 500)
        resizable = (True, True)
        def on_close(): logger.info("Cerrando ventana principal")

        super().__init__(title, light_theme=light_theme, dark_theme=dark_theme, iconphoto=iconphoto, size=size,
                         minsize=minsize,  resizable=resizable, on_close=on_close)

        self.theme_mode = config["GUI"]["mode"]

    def mainloop(self, n: int = 0) -> None:
        return super().mainloop(n)


if __name__ == "__main__":
    window = Window()
    window.mainloop()
