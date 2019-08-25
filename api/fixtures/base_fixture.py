from abc import ABC, abstractmethod, abstractproperty
from typing import Set


class BaseFixture(ABC):

    @abstractproperty
    def dependencies(self) -> Set[str]:
        pass

    @abstractproperty
    def key(self) -> str:
        pass

    @abstractmethod
    def load(self):
        pass
