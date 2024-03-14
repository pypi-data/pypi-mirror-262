from pydantic import BaseModel
from rooms_shared_services.src.storage.models import BaseDynamodbModel

from rooms_shared_services.src.models.texts.languages import Language


class TextTranslations(BaseDynamodbModel):
    source: Language = Language.en
    en: str | None = None
    ru: str | None = None
    pl: str | None = None
    he: str | None = None
    it: str | None = None
    de: str | None = None
    fr: str | None = None
    uk: str | None = None
