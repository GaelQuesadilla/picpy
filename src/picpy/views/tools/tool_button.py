import ttkbootstrap as ttk
from ttkbootstrap import constants as c
from typing import Tuple, List, Callable, Any
from tkinter import Misc
from tkinter_icons import MaterialIcon
from picpy.utils.config import is_dark
from picpy.utils.logger import logger


class ToolButton(ttk.Button):
    def __init__(self, master: Misc, icon_name: str, action: str, description: str | None = None,  padding: int | Tuple[int, int] = 5,  * args, **kwargs):
        super().__init__(master, padding=padding, compound=c.CENTER,
                         command=self._notify_listeners,  *args, **kwargs)

        self.icon_name = icon_name
        self.description = description
        self.action = action

        self._listeners: List[Callable[[str], None]] = []
        self.add_listener(self._log_click)

        self._build_ui()

    @property
    def icon_name(self) -> str:
        return self._icon_name

    @icon_name.setter
    def icon_name(self, value: str):

        self._icon_name = value
        self.icon = MaterialIcon(
            self.icon_name, size=20, color=self._icon_color)
        self.configure(image=self.icon.image)

    @property
    def _icon_color(self):
        return "#f0f0f0" if is_dark() else "#101010"

    def _build_ui(self):
        if self.description:
            ttk.ToolTip(self, text=self.description)

    def add_listener(self, listener: Callable[[str], None]):
        self._listeners.append(listener)

    def _notify_listeners(self):
        for listener in self._listeners:
            listener(self.action)

    def _log_click(self, action) -> None:
        logger.debug(
            f"Click sobre {self.icon_name}: {self.description}. Acción: {action}")


if __name__ == "__main__":
    from picpy.views.globals.window import Window

    window = Window()
    tool_button = ToolButton(window, "cog", "debug", "HELLO WORLD")
    tool_button.pack()
    window.mainloop()
