import ttkbootstrap as ttk
from ttkbootstrap import constants as c
from picpy.views.globals.tk_image import TkImage
from picpy.views.tools.toolbox import ToolBox
from picpy.views.tools.loaded_images import LoadedImages
from picpy.views.tools.status_bar import StatusBar, ImageMetadata
from tkinter import Misc
from typing import Callable


class MainView(ttk.Frame):
    def __init__(self, master: Misc):
        self.toolbox: ToolBox
        self.loaded_images: LoadedImages
        self.display: TkImage
        self.status_bar: StatusBar
        super().__init__(master)
        self._build_ui()

    def _build_ui(self):
        self._config_grid()
        self.toolbox = ToolBox(self, [])
        self.display = TkImage(self)
        self.loaded_images = LoadedImages(self)
        self.status_bar = StatusBar(self, ImageMetadata())

        self.toolbox.grid(row=1, column=0, rowspan=2, sticky=c.NS)
        self.display.grid(row=1, column=1, sticky=c.NSEW)
        self.loaded_images.grid(row=1, column=2, rowspan=2, sticky=c.NS)
        self.status_bar.grid(row=2, column=1, sticky=c.EW)

    def _config_grid(self):
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=0)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=0)

    def set_on_load_image(self, callback: Callable[[], None]) -> None:
        self.loaded_images.set_on_load_image(callback)


if __name__ == "__main__":
    from picpy.views.globals.window import Window

    window = Window()
    window.rowconfigure(0, weight=1)
    window.columnconfigure(0, weight=1)

    main_view = MainView(window)
    main_view.grid(row=0, column=0, sticky=c.NSEW)
    window.mainloop()
