from ..interface import ExampleInterface


class ExampleInitState(ExampleInterface):
    def __init__(self, base, contextPage) -> None:
        super().__init__(base, contextPage)

    def exampleTransition(self, exampleParam):
        """Required Process"""
        self.bd.fd.insert_to_textbox(self.p.lr.EXAMPLE_LOCATOR1(), exampleParam)
        """Transition"""
        self.p.changeState(ExampleInitState(self.bd, self.p))
