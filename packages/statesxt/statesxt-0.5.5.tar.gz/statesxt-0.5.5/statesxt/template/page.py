from .states.ts01 import ExampleInitState
from .locator import ExampleLocator
from .. import Page


class ExamplePage(Page):
    """Example Page action methods"""

    def __init__(self, base):
        super().__init__(base)
        self.initState = ExampleInitState(base, self)
        self.state = self.initState
        self.lr = ExampleLocator(base)

    """
    Methods: Abstract
    """

    # region
    def changeState(self, newState):
        self.state = newState

    def resetState(self):
        self.state = self.initState

    # endregion

    """
    Methods: Interface
    """

    # region ==> is a Python feature to freely collapsing code, ended with endregion
    def exampleTransition(self, exampleParam):
        return self.state.exampleTransition(exampleParam)

    # endregion

    """
    Methods: Specific
    """
    # region
    # endregion
