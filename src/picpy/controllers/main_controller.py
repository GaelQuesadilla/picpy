
from picpy.views.globals.open_image import load_images_from_dialog
from picpy.models.ImageModel import ImageModel
from picpy.views.main_view import MainView
from ttkbootstrap import constants as c
from pathlib import Path


class MainController:
    def __init__(self, main_view: MainView):
        self.view = main_view
        self.models: list[ImageModel] = []
        self.selected_index: int | None = None
        self._bind_events()
        self._refresh_view()

    @property
    def current_model(self) -> ImageModel | None:
        if self.selected_index is None:
            return None
        return self.models[self.selected_index]

    def open_images(self) -> None:
        new_models = load_images_from_dialog()
        if not new_models:
            return
        self.models.extend(new_models)
        self.selected_index = len(self.models) - 1
        self._refresh_view()

    def on_image_selected(self, index: int) -> None:
        if not 0 <= index < len(self.models):
            return
        self.selected_index = index
        self._refresh_display()

    def _refresh_view(self) -> None:
        self.view.loaded_images.set_images(self.models)
        self._refresh_display()

    def _bind_events(self) -> None:
        self.view.set_on_load_image(self.open_images)
        self.view.loaded_images.add_listener(self.on_image_selected)

    def _refresh_display(self) -> None:
        model = self.current_model
        if model is None:
            return

        self.view.status_bar.image_metadata.size = model.get_current_as_pil().size  # type: ignore
        self.view.status_bar.image_metadata.name = str(Path(model.path).name)
        self.view.status_bar.image_metadata.path = Path(model.path)
        self.view.status_bar._build_ui()
        self.view.display.set_model(model)


if __name__ == "__main__":
    from picpy.views.globals.window import Window

    window = Window()
    window.rowconfigure(0, weight=1)
    window.columnconfigure(0, weight=1)

    main_view = MainView(window)
    main_view.grid(row=0, column=0, sticky=c.NSEW)
    controller = MainController(main_view)
    window.mainloop()
