from pathlib import Path

import pytest
from picpy.models.image_metadata import ImageMetadata
from picpy.views.tools.status_bar import StatusBar
from picpy.views.tools.toolbox import ToolBox
from picpy.views.tools.tool_button import ToolButton
from PIL import ImageTk, Image
from picpy.utils.config import config


class TestStatusBar:

    @pytest.fixture
    def status_bar(self, window):
        metadata = ImageMetadata(
            name="image.png", size=(100, 100), path=Path.cwd())
        status_bar = StatusBar(window, metadata)
        status_bar.pack()
        window.update()
        yield status_bar
        status_bar.destroy()

    def test_status_bar_render(self, status_bar):
        assert status_bar.winfo_exists()
        assert status_bar.winfo_ismapped()


class TestToolButton:

    @pytest.fixture
    def tool_button(self, window):
        icon = Image.open(config["test"]["test_image"]).resize((30, 30))
        icon_tk = ImageTk.PhotoImage(icon)
        tool_button = ToolButton(window, icon_tk,  "cog", "HELLO WORLD")
        tool_button.pack()
        window.update()
        yield tool_button
        tool_button.destroy()

    def test_tool_button_render(self, tool_button):
        assert tool_button.winfo_exists()
        assert tool_button.winfo_ismapped()


class TestToolBox:

    @pytest.fixture
    def toolbox(self, window):
        toolbox = ToolBox(window, width=50, height=50)
        toolbox.pack()
        window.update()
        yield toolbox
        toolbox.destroy()

    def test_toolbox_render(self, toolbox):
        assert toolbox.winfo_exists()
        assert toolbox.winfo_ismapped()
