import pytest
from picpy.views.globals.window import Window
import pytest
import numpy as np
from PIL import Image
from picpy.models.ImageModel import ImageModel
from pathlib import Path


image_path = Path("src/test/images")
lena_path = image_path / "lena64.png"
not_image_path = image_path / "not_image.png"
absolutely_not_image_path = image_path / "absolutely_not_image.txt"


@pytest.fixture()
def model():
    return ImageModel()


@pytest.fixture()
def lena_model():
    image = ImageModel()
    image.load_image(lena_path)
    return image


@pytest.fixture()
def original_image():
    return np.asarray(Image.open(lena_path).convert("RGB"))


@pytest.fixture(scope="session")
def window():
    window = Window()
    yield window
    window.destroy()
