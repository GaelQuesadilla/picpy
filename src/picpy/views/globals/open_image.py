from tkinter import filedialog, messagebox

from PIL import UnidentifiedImageError

from picpy.models.ImageModel import ImageModel
from picpy.utils.logger import logger

IMAGE_FILETYPES = [("Imágenes", "*.png *.jpg *.jpeg *.bmp")]


def load_images_from_dialog() -> list[ImageModel]:
    """Abre el diálogo de archivos y devuelve un ImageModel por cada imagen válida."""
    paths = filedialog.askopenfilenames(filetypes=IMAGE_FILETYPES)
    models: list[ImageModel] = []

    for path in paths:
        model = ImageModel()
        try:
            model.load_image(path)
        except FileNotFoundError:
            messagebox.showerror(
                "Error", f"No se encontró el archivo:\n{path}")
        except UnidentifiedImageError:
            messagebox.showerror("Error", f"No es una imagen válida:\n{path}")
        else:
            models.append(model)
            logger.debug(f"Imagen cargada: {path}")

    return models
