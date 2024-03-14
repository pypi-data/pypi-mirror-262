from rooms_shared_services.src.models.products.categories import ProductCategory
from rooms_shared_services.src.storage.dynamodb import DynamodbStorageClient
from rooms_shared_services.src.translation.client import TranslationClient
from rooms_shared_services.src.models.texts.languages import Language
from typing import Literal


TranslationVariant = Literal["NAME", "DESCRIPTION"]


class SourceProcessor(object):
    def __init__(self, storage_client: DynamodbStorageClient, translation_client: TranslationClient) -> None:
        self.dynamodb_storage_client = storage_client
        self.translation_client = translation_client

    def run_all_translation(self, languages: list[Language]):
        for batch in self.list_source_by_pages():
            self.run_batch_translation(batch, languages)
            self.update_source(batch)
            
    def update_source(self, batch: list[ProductCategory]):
        ...
            
    def run_batch_translation(self, variant: TranslationVariant, batch: list[ProductCategory], languages: list[Language] = list(Language)):
        for category_item in batch:
            translations = self.translation_client.bulk_translate(
                source_language=Language.en,
                target_languages=languages,
                txt=category_item.name
            )
            match variant:
                case "NAME":
                    category_item.name_translations = translations
                case "DESCRIPTION":
                    category_item.description_translations = translations
                case _:
                    raise ValueError("Invalid translation variant.")
        
    def clean_table(self):
        all_keys = []
        for batch in self.list_source_by_pages():
            all_keys.extend([{"name": cat_item.name} for cat_item in batch])
        if all_keys:
            self.dynamodb_storage_client.bulk_delete(keys=all_keys)

    def create_source(self, category_data: list[ProductCategory]):
        self.clean_table()
        table_items = [category_item.dynamodb_dump(exclude_unset=True) for category_item in category_data]
        self.dynamodb_storage_client.bulk_create(table_items=table_items)
        
    def retrieve_source(self, name: str):
        key = {"name": name}
        category_item = self.dynamodb_storage_client.retrieve(key=key)
        return ProductCategory.validate_dynamodb_item(category_item)
        
    def list_source_by_pages(self):
        for page in self.dynamodb_storage_client.get_by_pages():
            yield [ProductCategory.validate_dynamodb_item(category_item) for category_item in page]
