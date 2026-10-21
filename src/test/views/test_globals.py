import pytest
from picpy.views.globals.labeled_frame import LabeledFrame
from picpy.views.globals.tk_image import TkImage
from picpy.views.globals.var_frame import VarFrame


class TestWindow:
    def test_window_render(self, window):
        window.update()
        assert window.winfo_exists()
        assert window.winfo_ismapped()


class TestLabeledFrame:

    @pytest.fixture
    def labeled_frame(self, window):
        labeled_frame = LabeledFrame(window, "Hello world")
        labeled_frame.pack()
        window.update()
        yield labeled_frame
        labeled_frame.destroy()

    def test_labeled_frame_render(self, labeled_frame):
        assert labeled_frame.winfo_exists()
        assert labeled_frame.winfo_ismapped()


class TestVarFrame:

    @pytest.fixture
    def var_frame(self, window):
        var_frame = VarFrame(window, "var name", "var value")
        var_frame.pack()
        window.update()
        yield var_frame
        var_frame.destroy()

    def test_var_frame_render(self, var_frame):
        assert var_frame.winfo_exists()
        assert var_frame.winfo_ismapped()


class TestTkImage:

    @pytest.fixture
    def tk_image(self, window, lena_model):
        tk_image = TkImage(window, lena_model)
        tk_image.pack()
        window.update()
        yield tk_image
        tk_image.destroy()

    def test_tk_image_render(self, tk_image):
        assert tk_image.winfo_exists()
        assert tk_image.winfo_ismapped()
