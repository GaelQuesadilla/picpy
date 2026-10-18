from tkinter import Misc
from typing import Any, Callable
from picpy.utils.logger import logger
from picpy.models.ImageModel import ImageModel
import ttkbootstrap as ttk
import ttkbootstrap.constants as c
from picpy.utils.config import config


class TkImage(ttk.Canvas):
    def __init__(self, master: Misc, model: ImageModel | None = None, on_click: Callable[[Any], None] | None = None, *args, **kwargs):

        self.model = model or ImageModel()
        self.model.add_listener(self._update_image)
        self.on_click = on_click

        self.photo = self.model.get_current_as_tk()

        super().__init__(master, *args, **kwargs)
        self._build_ui()

    @logger.catch
    def _build_ui(self) -> None:
        self._update_image()
        self.bind("<Button-1>", self.on_click)

    def _display_image(self) -> None:
        if self.photo is None:
            logger.warning("No hay ninguna imagen disponible")
            return

        self.create_image(0, 0, image=self.photo, anchor=c.NW)

    def _update_image(self) -> None:
        self.photo = self.model.get_current_as_tk()
        self._display_image()


if __name__ == "__main__":
    from picpy.views.globals.window import Window
    from picpy.operations.pixel_operations import contrast

    window = Window()

    model = ImageModel()
    model.load_image(config["test"]["test_image"])

    def on_click(event: Any) -> None:
        if model.current_array is not None:
            model.apply_operation(
                lambda array: contrast(array, gamma=1.1, beta=0.1))

    tk_image = TkImage(window, model, on_click)
    tk_image.pack(fill=c.BOTH, expand=True)

    window.mainloop()
