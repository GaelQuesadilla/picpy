import ttkbootstrap as ttk
from ttkbootstrap import constants as c
from typing import Tuple, List, Callable
from tkinter import Misc
from tkinter_icons import MaterialIcon
from picpy.utils.config import config
from picpy.utils.logger import logger
from PIL import ImageTk, Image


class ToolButton(ttk.Button):
    def __init__(self, master: Misc, icon: ImageTk.PhotoImage | MaterialIcon, action: str, description: str | None = None,  padding: int | Tuple[int, int] = 5,  * args, **kwargs):
        super().__init__(master, padding=padding, compound=c.CENTER,
                         command=self._notify_listeners,  *args, **kwargs)

        self.icon = icon
        self.description = description
        self.action = action

        self._listeners: List[Callable[[str], None]] = []
        self.add_listener(self._log_click)

        self._build_ui()

    def _build_ui(self):
        self.configure(image=self.icon)  # pyright: ignore[reportArgumentType]
        if self.description:
            ttk.ToolTip(self, text=self.description)

    def add_listener(self, listener: Callable[[str], None]):
        self._listeners.append(listener)

    def _notify_listeners(self):
        for listener in self._listeners:
            listener(self.action)

    def _log_click(self, action) -> None:
        logger.debug(
            f"Click sobre {self.description}. Acción: {action}")


if __name__ == "__main__":
    from picpy.views.globals.window import Window

    window = Window()
    icon = Image.open(config["test"]["test_image"]).resize((30, 30))
    icon_tk = ImageTk.PhotoImage(icon)
    tool_button = ToolButton(window, icon_tk, "debug", "HELLO WORLD")
    tool_button.pack()
    window.mainloop()
