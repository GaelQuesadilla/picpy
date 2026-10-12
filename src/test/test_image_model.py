import pytest
import numpy as np
from PIL import Image
from picpy.models.ImageModel import ImageModel
from pathlib import Path
from PIL import UnidentifiedImageError


image_path = Path("src/test/images")
lena_path = image_path / "lena16.png"
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


class TestModel:

    def test_is_empty(self, model):
        assert not model.has_image
        assert model._original_image is None
        assert len(model._history) == 0

    def test_is_not_empty(self, lena_model):
        assert lena_model.has_image
        assert not lena_model._original_image is None
        assert len(lena_model._history) == 1

    def test_error_loads(self, model):

        with pytest.raises(FileNotFoundError) as error:
            model.load_image(image_path / "not_found")

        assert error.type is FileNotFoundError

        with pytest.raises(UnidentifiedImageError) as error:
            model.load_image(absolutely_not_image_path)

        assert error.type is UnidentifiedImageError

        with pytest.raises(UnidentifiedImageError) as error:
            model.load_image(not_image_path)

        assert error.type is UnidentifiedImageError

    def test_load_lena(self, model):
        model.load_image(lena_path)
        assert model.has_image
        assert not model._original_image is None
        assert not model.current_array is None

    def test_normalize_lena(self, lena_model):
        assert not (lena_model.current_array > 1.0).any()

    def test_fidelity(self, lena_model, original_image):
        model_image = ImageModel._to_uint8(lena_model.current_array)
        assert not (model_image - original_image > 0).any()
