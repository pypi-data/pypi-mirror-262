from abc import ABC, abstractmethod
from dotenv import load_dotenv
import warnings

from base.base_driver import BaseDriver
from base.wait import MyBy

# looding all env variables and ignoring a certain warning
load_dotenv()
warnings.filterwarnings("ignore", message="Worksheet.update.*method signature will change.*")


class StateInterface(ABC):
    """
    An abstract class for all the state interface classes
    """

    def __init__(self, base: BaseDriver) -> None:
        self.__bd = base

    @property
    def bd(self):
        return self.__bd


class Page(ABC):
    """A parent class of all specific page classes."""

    def __init__(self, base: BaseDriver) -> None:
        self.__bd = base
        self.jpnFormats = ["jpn", "japan", "japanese", "jp"]
        self.engFormats = ["eng", "english", "en"]
        self.emptyFormats = ["", "-", "<blank>", "<empty>", "blank", "empty"]
        self.anyFormats = ["anything", "dc", "Any", "any"]
        self.spaceFormats = ["<space>"]

    @property
    def bd(self):
        return self.__bd

    @abstractmethod
    def changeState(self):
        pass

    @abstractmethod
    def resetState(self):
        pass


class Locator:
    """A parent class of all page locator classes."""

    def __init__(self, base: BaseDriver) -> None:
        self.__bd = base
        self.by = MyBy()

    @property
    def bd(self):
        return self.__bd
