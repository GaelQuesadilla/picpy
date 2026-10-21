from tkinter import Misc
from typing import Any, Callable, Tuple
from picpy.utils.logger import logger
from picpy.models.ImageModel import ImageModel
from PIL import Image, ImageTk
import ttkbootstrap as ttk
import ttkbootstrap.constants as c
from picpy.utils.config import config


class TkImage(ttk.Canvas):
    def __init__(self, master: Misc, model: ImageModel | None = None, on_click: Callable[[Any], None] | None = None, *args, **kwargs):
        self.image_size = (None, None)
        self.model = model or ImageModel()
        self.model.add_listener(self._update_image)
        self.on_click = on_click

        self.photo = self.model.get_current_as_pil()

        super().__init__(master, *args, **kwargs)
        self._build_ui()

    @logger.catch
    def _build_ui(self) -> None:
        self._update_image()
        self.bind("<Button-1>", self.on_click)

    def _display_image(self) -> None:
        image = self.model.get_current_as_pil()
        if image is None:
            logger.warning("No hay ninguna imagen disponible")
            return
        scale = self._scale_for(image.size)
        if scale != 1:
            image = image.resize(
                (round(image.width * scale), round(image.height * scale)))

        self.photo = ImageTk.PhotoImage(image)
        self.configure(height=image.height)
        self.delete("all")
        self.create_image(0, 0, image=self.photo, anchor=c.NW)

    def _scale_for(self, image_size: Tuple[int, int]) -> float:
        ratios = [
            target / current
            for target, current in zip(self.image_size, image_size)
            if target is not None
        ]
        return min(ratios, default=1.0)

    def _update_image(self) -> None:
        self.photo = self.model.get_current_as_pil()
        self._display_image()

    def set_model(self, model: ImageModel):
        self.model = model
        self.model.add_listener(self._update_image)
        self._update_image()


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
