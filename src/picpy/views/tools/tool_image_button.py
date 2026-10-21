from typing import Tuple
from tkinter import Misc
from PIL.ImageTk import PhotoImage, Image
from tkinter_icons import MaterialIcon
from picpy.utils.config import is_dark
from picpy.views.tools.tool_button import ToolButton
from pathlib import Path
from picpy.utils.config import config


class ToolImageButton(ToolButton):
    def __init__(self, master: Misc, icon_path: Path | str, action: str, description: str | None = None, padding: int | Tuple[int, int] = 5, size: Tuple[int, int] = (30, 30), *args, **kwargs):
        image = Image.open(icon_path).resize(size=size)
        icon = PhotoImage(image)

        super().__init__(master, icon, action, description, padding, *args, **kwargs)


if __name__ == "__main__":
    from picpy.views.globals.window import Window

    window = Window()
    icon_path = Path(config["assets"]["path"])/"template_icons"/"1_grid.png"
    tool_button = ToolImageButton(window, icon_path, "debug", "HELLO WORLD")
    tool_button.pack()
    window.mainloop()
