from abc import ABC, abstractmethod


class ClassTemplate(ABC):
    @abstractmethod
    def must_be_implemented(self):
        """Docstring."""


class ConcreteClass(ClassTemplate):
    def must_be_implemented(self):
        pass
