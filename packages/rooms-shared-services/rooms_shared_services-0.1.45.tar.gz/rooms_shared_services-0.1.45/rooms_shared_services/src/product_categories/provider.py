import yaml
import os

script_dir = os.path.dirname(__file__)

CATEGORIES_PATH = "{}/categories.yml".format(script_dir)


class CategoryProvider(object):
    def __init__(self):
        """Set attributes."""
        self.cat_list = []
        self.validated_cat_list = []
        self.cat_names = []
        self.not_allowed = [" "]
        self.root = ["Categories", "By Rooms", "By Function", "By Origin"]

    def __call__(self):
        self.provide_category_list()
        self.validate_cat_pairs()
        return self.validated_cat_list

    def get_product_categories(self):
        with open(CATEGORIES_PATH, "r") as stream:
            return yaml.load(stream=stream, Loader=yaml.Loader)

    def provide_category_list(self):
        raw_cats = self.get_product_categories()
        self.collect_cat_pairs(raw_cats)

    def collect_cat_pairs(self, raw_cats: dict):
        for parent, cat in raw_cats.items():
            match cat:
                case str():
                    self.cat_list.append((cat, parent))
                case dict():
                    for cat_key, _ in cat.items():
                        self.cat_list.append((cat_key, parent))  # noqa: WPS220
                    self.collect_cat_pairs(raw_cats=cat)
                case list():
                    for cat_name in cat:
                        self.cat_list.append((cat_name, parent))  # noqa: WPS220
                        
    def validate_root(self, cat_elem: str):
        if cat_elem in self.root:
            return None
        return cat_elem

    def validate_cat_pairs(self):  # noqa: WPS231
        for cat_item in self.cat_list:
            cat_child, cat_parent = cat_item
            for name in (cat_child, cat_parent):
                for snippet in self.not_allowed:
                    if snippet in name:
                        raise ValueError("Not allowed snippet {} in {}".format(snippet, name))  # noqa: WPS220
            if cat_child == "other":
                cat_child = "other {}".format(cat_parent)
            if cat_child in self.cat_names:
                raise ValueError("Duplicated category name: {}".format(cat_child))
            self.cat_names.append(cat_child)
            cat_child, cat_parent = [cat_elem.replace('_', ' ').title() for cat_elem in (cat_child, cat_parent)]
            cat_child, cat_parent = [self.validate_root(cat_elem) for cat_elem in (cat_child, cat_parent)]
            if (cat_child, cat_parent) != (None, None):
                self.validated_cat_list.append((cat_child, cat_parent))
