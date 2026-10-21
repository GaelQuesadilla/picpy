from pathlib import Path
from tkinter import Misc
from typing import Callable, List, Tuple
from dataclasses import dataclass
import ttkbootstrap as ttk
from ttkbootstrap import constants as c
from picpy.utils.config import config
from picpy.views.tools.tool_button import ToolButton
from picpy.views.tools.tool_icon_button import ToolIconButton
from picpy.views.tools.tool_image_button import ToolImageButton
from picpy.utils.logger import logger


@dataclass(frozen=True)
class Tool:
    action: str
    description: str
    icon_name: str | None = None
    icon_path: str | Path | None = None


class ToolBox(ttk.Frame):
    def __init__(
        self,
        master: Misc,
        tools: List[Tool],
        padding: int | Tuple[int, int] = 5,
        columns: int = 5,
        *args,
        **kwargs,
    ):
        super().__init__(master, padding=padding, *args, **kwargs)
        self.tools = tools
        self.columns = columns

        self._listeners: List[Callable[[str], None]] = []

        self._build_ui()

    def _build_ui(self) -> None:
        for index, tool in enumerate(self.tools):
            button = self._create_button(tool)
            button.add_listener(self._notify_listeners)
            row, column = divmod(index, self.columns)
            button.grid(row=row, column=column, padx=2, pady=2)

    def set_tools(self, values: List[Tool]):
        self.tools = values
        self._build_ui

    def _create_button(self, tool: Tool) -> ToolButton:
        if tool.icon_name is not None:
            return ToolIconButton(self, tool.icon_name, tool.action, tool.description)
        if tool.icon_path is not None:
            return ToolImageButton(self, tool.icon_path, tool.action, tool.description)
        raise ValueError(
            f"La herramienta '{tool.action}' necesita icon_name o icon_path")

    def add_listener(self, listener: Callable[[str], None]) -> None:
        self._listeners.append(listener)

    def _notify_listeners(self, action: str) -> None:
        for listener in self._listeners:
            listener(action)


if __name__ == "__main__":
    from picpy.views.globals.window import Window

    window = Window()
    icon_path = Path(config["assets"]["path"]) / \
        "template_icons"
    tools = [
        Tool("debug", "Debug", icon_name="cog"),
        Tool("grid_1", "Cuadrícula 1", icon_path=icon_path/"1_grid.png"),
        Tool("grid_2", "Cuadrícula 2", icon_path=icon_path/"2_grid_H.png"),
        Tool("grid_3", "Cuadrícula 3", icon_path=icon_path/"2_grid_V.png"),
        Tool("grid_4", "Cuadrícula 4", icon_path=icon_path/"3_grid_BB.png"),
        Tool("grid_5", "Cuadrícula 5", icon_path=icon_path/"3_grid_BL.png"),
        Tool("grid_6", "Cuadrícula 6", icon_path=icon_path/"3_grid_BR.png"),
        Tool("grid_7", "Cuadrícula 7", icon_path=icon_path/"3_grid_BT.png"),
        Tool("grid_8", "Cuadrícula 8", icon_path=icon_path/"4_grid.png"),
    ]
    toolbox = ToolBox(window, tools)
    toolbox.add_listener(logger.debug)
    toolbox.pack()
    window.mainloop()
