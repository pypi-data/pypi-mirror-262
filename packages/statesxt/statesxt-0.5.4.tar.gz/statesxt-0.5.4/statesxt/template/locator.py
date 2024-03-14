from .. import Locator


class ExampleLocator(Locator):
    """Example page locator class"""

    def __init__(self, base) -> None:
        super().__init__(base)
        self.setup()

    def setup(self):
        # flags
        self.EXAMPLE_LOCATOR1 = lambda loc="exampleloc1": self.bd.wd.clickable(self.by.xpath, loc)
        self.EXAMPLE_LOCATOR2 = lambda loc="exampleloc2": self.bd.wd.visible(self.by.xpath, loc)
