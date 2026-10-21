import pytest
from picpy.views.sidebar.sidebar import Sidebar


class TestSidebar:

    @pytest.fixture
    def sidebar(self, window):
        sidebar = Sidebar(window)
        sidebar.pack()
        window.update()
        yield sidebar
        sidebar.destroy()

    def test_sidebar_render(self, sidebar):
        assert sidebar.winfo_exists()
        assert sidebar.winfo_ismapped()
