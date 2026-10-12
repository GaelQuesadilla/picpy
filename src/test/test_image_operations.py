import pytest
import numpy as np
from PIL import Image
from picpy.models.ImageModel import ImageModel
from pathlib import Path
from picpy.operations.pixel_operations import power, brightness, contrast, inverse, logarithmic, exponential

image_path = Path("src/test/images")
lena_path = image_path / "lena64.png"


@pytest.fixture()
def lena_model():
    image = ImageModel()
    image.load_image(lena_path)
    return image


class TestPrecision:

    def test_brightness(self, lena_model):
        for beta_int in range(-256, 256, 8):
            beta = beta_int/255
            lena_model.apply_operation(brightness, beta)
            lena_model.apply_operation(brightness, -beta)
            errors = np.abs(lena_model.current_array -
                            lena_model._original_image)

            assert (errors < 1/255).all()

    def test_contrast(self, lena_model):
        """
        B = A * gamma + beta
        B - beta = A * gamma
        B * 1/gamma - beta/gamma = A
        """
        for gamma_int in range(-10, 10):
            if gamma_int == 0:
                continue

            for beta_int in range(0, 256, 16):
                beta = beta_int/255
                gamma = gamma_int/10
                lena_model.apply_operation(contrast, gamma, beta)
                lena_model.apply_operation(contrast, 1/gamma, -beta/gamma)
                errors = np.abs(lena_model.current_array -
                                lena_model._original_image)
                print(f"test_contrast {gamma=}{beta=}:\n{errors}")

                assert (errors < 1).all()

    def test_inverse(self, lena_model):

        for _ in range(0, 10):
            lena_model.apply_operation(inverse)
            lena_model.apply_operation(inverse)
            errors = np.abs(lena_model.current_array -
                            lena_model._original_image)

            assert (errors < 1/255).all()

    def test_logarithmic_and_exponential(self, lena_model):
        """
        B = c * log(1 + A)
        B / c = log(1 + A)
        EXP(B/C) = 1 + A
        EXP(B/C) - 1 = A
        """

        for c_int in range(1, 10):
            c = c_int / 10
            lena_model.apply_operation(logarithmic, c)
            lena_model.apply_operation(exponential, c)
            errors = np.abs(lena_model.current_array -
                            lena_model._original_image)

            assert (errors < 1/255).all()

    def test_power(self, lena_model):
        """
         B = c * A ^ exp
         B/c = A ^ exp
         A = (B/c) ^ (1/exp) 
         A = (B ^ (1 / exp)) * (c ^ (-1 / exp)) 
        """
        for exp_int in range(0, 10):
            if exp_int == 0:
                continue
            for c_int in range(1, 10):
                exp = exp_int/10
                c = c_int / 10
                lena_model.apply_operation(power, exp, c)
                lena_model.apply_operation(power, 1/exp, c**(-1/exp))
                errors = np.abs(lena_model.current_array -
                                lena_model._original_image)

                assert (errors < 1/255).all()
