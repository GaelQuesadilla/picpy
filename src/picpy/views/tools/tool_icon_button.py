from typing import Tuple
from tkinter import Misc
from tkinter_icons import MaterialIcon
from picpy.utils.config import is_dark
from picpy.views.tools.tool_button import ToolButton


class ToolIconButton(ToolButton):

    def __init__(self, master: Misc, icon_name: str, action: str, description: str | None = None, padding: int | Tuple[int, int] = 5, *args, **kwargs):

        self.icon_name = icon_name
        icon = self.icon
        super().__init__(master, icon, action, description, padding, *args, **kwargs)

    @property
    def icon_name(self) -> str:
        return self._icon_name

    @icon_name.setter
    def icon_name(self, value: str):
        self._icon_name = value
        self.icon = MaterialIcon(
            self.icon_name, size=35, color=self._icon_color)

    @property
    def _icon_color(self):
        return "#f0f0f0" if is_dark() else "#101010"


if __name__ == "__main__":
    from picpy.views.globals.window import Window

    window = Window()
    tool_button = ToolIconButton(window, "cog", "debug", "HELLO WORLD")
    tool_button.pack()
    window.mainloop()
