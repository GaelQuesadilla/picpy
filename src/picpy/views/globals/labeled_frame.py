from tkinter import Misc
from picpy.utils.logger import logger
import ttkbootstrap as ttk
import ttkbootstrap.constants as c
from typing import Tuple


class LabeledFrame(ttk.LabelFrame):
    def __init__(self, master: Misc, text="", padding: int | Tuple[int, int] = 5,  *args, **kwargs):

        super().__init__(master, padding=padding, text=text, *args, **kwargs)
        self._build_ui()

    @logger.catch
    def _build_ui(self) -> None:
        pass


if __name__ == "__main__":
    from picpy.views.globals.window import Window

    window = Window()
    labeled_frame = LabeledFrame(window, "Hello world")
    labeled_frame.pack(fill=c.BOTH, expand=True)
    window.mainloop()
