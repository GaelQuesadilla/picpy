from tkinter import Misc
from typing import Any, List, Callable

import ttkbootstrap as ttk
from ttkbootstrap import constants as c
from picpy.models.ImageModel import ImageModel
from typing import List
from picpy.views.globals.tk_image import TkImage
from picpy.utils.logger import logger


class LoadedImages(ttk.ScrolledFrame):
    def __init__(self, master: Misc, *, padding: int = 2, loaded_images: List[ImageModel] = [],  **kwargs) -> None:
        self.loaded_images = loaded_images
        self._tk_images: List[TkImage] = []
        super().__init__(master, padding=padding, auto_hide=False, **kwargs)
        self._build_ui()
        self._listeners: List[Callable[[int], None]] = []

    def add_listener(self, listener: Callable[[int], None]):
        self._listeners.append(listener)

    def _build_ui(self) -> None:
        if not self.loaded_images:
            logger.debug("No hay imágenes cargadas en LoadedImages")
            ttk.Label(self, text="No hay imágenes disponibles").pack()
            return
        width = self.winfo_width()
        logger.debug(f"{width=}")
        for image in self.loaded_images:
            tk_image = TkImage(self, image, )
            tk_image.pack(fill=c.X, pady=2)
            self._tk_images.append(tk_image)
        self.bind("<Configure>", self._resize_images, add="+")

    def _resize_images(self, event) -> None:
        for tk_image in self._tk_images:
            tk_image.image_size = (event.width, None)
            tk_image._display_image()


if __name__ == "__main__":
    from picpy.utils.config import config
    from picpy.views.globals.window import Window

    def load_model() -> ImageModel:
        model = ImageModel()
        model.load_image(config["test"]["test_image"])
        return model

    window = Window()
    loaded_images = LoadedImages(
        window, loaded_images=[load_model() for _ in range(5)])
    loaded_images.pack(fill=c.BOTH, expand=True)
    window.mainloop()
