from src.storage.models import BaseDynamodbModel
from src.models.texts.translations import TextTranslations
from pydantic import HttpUrl

class ProductCategory(BaseDynamodbModel):
    name: str
    id: int
    parent: int | None = None
    description: str | None = None
    image: HttpUrl | None = None
    name_translations: TextTranslations | None = None
    description_translations: TextTranslations | None = None
