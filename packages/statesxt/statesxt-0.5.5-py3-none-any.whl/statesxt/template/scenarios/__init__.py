import pytest
import softest

from ..page import ExamplePage


@pytest.mark.order(1)
@pytest.mark.usefixtures("setup")
class TestExample(softest.TestCase):
    """Test cases for example page"""

    @pytest.fixture(autouse=True)
    def class_setup(self):
        self.p = ExamplePage(self.base)
