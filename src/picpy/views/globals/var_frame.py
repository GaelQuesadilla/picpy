import ttkbootstrap as ttk
import ttkbootstrap.constants as c
from tkinter import Misc
from typing import Any
from picpy.models.image_metadata import ImageMetadata
from picpy.views.globals.labeled_frame import LabeledFrame


class VarFrame(ttk.Frame):
    def __init__(self, master: Misc, var_name: str, var_value: Any, *args, **kwargs) -> None:
        self.var_name = var_name
        self.var_value = var_value
        super().__init__(master, padding=5, *args, **kwargs)
        self._build_ui()

    def _build_ui(self):
        varname_frame = LabeledFrame(
            self, text=self.var_name, padding=(15, 5))
        varvalue_label = ttk.Label(varname_frame, text=self.var_value)
        varname_frame.pack(padx=2, pady=0, expand=True, fill=c.BOTH)
        varvalue_label.pack(expand=True, fill=c.BOTH)


if __name__ == "__main__":
    from picpy.views.globals.window import Window
    app = Window()

    status_bar = VarFrame(app, "var name", "var value")
    status_bar.pack(side=c.BOTTOM, fill=c.X)

    app.mainloop()
