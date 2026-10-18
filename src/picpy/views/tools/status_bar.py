import ttkbootstrap as ttk
import ttkbootstrap.constants as c
from tkinter import Misc
from picpy.models.image_metadata import ImageMetadata
from picpy.views.globals.var_frame import VarFrame
from typing import Tuple


class StatusBar(ttk.Frame):
    def __init__(self, master: Misc, image_metadata: ImageMetadata, padding: int | Tuple[int, int] = 5, *args, **kwargs) -> None:
        self.image_metadata = image_metadata
        super().__init__(master, padding=padding, *args, **kwargs)

        self._build_ui()

    def _build_ui(self):
        metadata = self.image_metadata
        var_frames = [
            VarFrame(self, var_name="Nombre", var_value=metadata.name),
            VarFrame(self, var_name="Tamaño",
                     var_value=" X ".join(map(lambda v: f"{v}px", metadata.size))),
            VarFrame(self, var_name="Directorio", var_value=metadata.path)
        ]
        chars = [max(len(frame.var_name), len(str(frame.var_value)))
                 for frame in var_frames]

        for i, frame in enumerate(var_frames):
            self.columnconfigure(i, weight=chars[i])
            frame.grid(row=0, column=i, padx=0, pady=0, sticky=c.EW)


if __name__ == "__main__":
    from picpy.views.globals.window import Window
    from pathlib import Path
    app = Window()

    metadata = ImageMetadata(
        name="image.png", size=(100, 100), path=Path.cwd())
    status_bar = StatusBar(app, metadata)
    status_bar.pack(side=c.BOTTOM, fill=c.X)

    app.mainloop()
