import ttkbootstrap as ttk
from ttkbootstrap import constants as c


class ToolBox(ttk.Frame):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


if __name__ == "__main__":
    from picpy.views.globals.window import Window

    window = Window()
    toolbox = ToolBox(window)
    toolbox.pack()
    window.mainloop()
