from tkinter import Misc
from typing import Callable, List

import ttkbootstrap as ttk
from ttkbootstrap import constants as c
from picpy.models.ImageModel import ImageModel
from picpy.views.globals.tk_image import TkImage
from picpy.utils.logger import logger


class LoadedImages(ttk.Frame):
    def __init__(self, master: Misc, padding: int = 2, loaded_images: List[ImageModel] | None = None, **kwargs):
        super().__init__(master, padding=padding, **kwargs)
        self.loaded_images: List[ImageModel] = loaded_images or []
        self._tk_images: List[TkImage] = []
        self._listeners: List[Callable[[int], None]] = []
        self.load_button: ttk.Button
        self.scrolled: ttk.ScrolledFrame
        self._build_ui()
        self.refresh()

    def add_listener(self, listener: Callable[[int], None]) -> None:
        self._listeners.append(listener)

    def _notify_listeners(self, index: int):
        for listener in self._listeners:
            listener(index)

    def set_on_load_image(self, callback: Callable[[], None]) -> None:
        self.load_button.configure(command=callback)

    def set_images(self, images: List[ImageModel]) -> None:
        self.loaded_images = images
        self.refresh()

    def refresh(self) -> None:
        for child in self.scrolled.winfo_children():
            child.destroy()
        self._tk_images.clear()

        if not self.loaded_images:
            logger.debug("No hay imágenes cargadas en LoadedImages")
            ttk.Label(self.scrolled, text="No hay imágenes disponibles").pack()
            return

        for index, image in enumerate(self.loaded_images):
            tk_image = TkImage(
                self.scrolled,
                image,
                on_click=lambda _event, i=index: self._notify_listeners(i),
            )
            tk_image.pack(fill=c.X, pady=2)
            self._tk_images.append(tk_image)

    def _build_ui(self) -> None:
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)

        self.load_button = ttk.Button(
            self, text="Cargar imagen", bootstyle=c.PRIMARY
        )
        self.load_button.grid(
            row=0, column=0, sticky=c.EW, padx=2, pady=(0, 4))

        self.scrolled = ttk.ScrolledFrame(self, auto_hide=False)
        self.scrolled.grid(row=1, column=0, sticky=c.NSEW)
        self.scrolled.bind("<Configure>", self._resize_images, add="+")

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
        window, loaded_images=[load_model() for _ in range(5)]
    )
    loaded_images.set_on_load_image(lambda: print("cargar imagen"))
    loaded_images.pack(fill=c.BOTH, expand=True)
    window.mainloop()
