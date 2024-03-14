from abc import ABC, abstractmethod
from src.models.texts.languages import Language


class AbstractTranslationProvider(ABC):
    @abstractmethod
    def translate(self, txt: str, source: Language, target: Language):
        ...
