from rooms_shared_services.src.translation.providers.abstract import AbstractTranslationProvider
from rooms_shared_services.src.models.texts.translations import Language
from rooms_shared_services.src.models.texts.translations import TextTranslations


class TranslationClient(object):
    def __init__(self, provider: AbstractTranslationProvider) -> None:
        self.provider = provider
        
    def bulk_translate(self, source_language: Language, target_languages: list[Language], txt: str) -> TextTranslations:
        translations = [self.provider.translate(
            txt=txt,
            source=source_language,
            target=target_language
        ) for target_language in target_languages]
        text_translations = TextTranslations(source=source_language)
        for target_language, translation in zip(target_languages, translations):
            setattr(text_translations, target_language.name, translation)
        return text_translations
        
        
