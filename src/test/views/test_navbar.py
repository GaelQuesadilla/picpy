import pytest
from picpy.views.navbar.navbar import Navbar


class TestNavbar:

    @pytest.fixture
    def navbar(self, window):
        navbar = Navbar(window)
        navbar.pack()
        window.update()
        yield navbar
        navbar.destroy()

    def test_navbar_render(self, navbar):
        assert navbar.winfo_exists()
        assert navbar.winfo_ismapped()
