import json
from typing import Any

from django.core.management import BaseCommand

from catalog.models import Category, Product


class Command(BaseCommand):

    @staticmethod
    def json_read_categories(json_data_file: Any) -> str:
        """Функция чтения фикстуры с категориями"""
        with open(json_data_file, "r", encoding="utf-8") as fp:
            return json.load(fp)

    @staticmethod
    def json_read_products(json_data_file: Any) -> str:
        """Функция чтения фикстуры с продуктами"""
        with open(json_data_file, "r", encoding="utf-8") as fp:
            return json.load(fp)

    def handle(self, *args, **options):

        Category.objects.all().delete()
        Product.objects.all().delete()

        # Создайте списки для хранения объектов
        product_for_create = []
        category_for_create = []

        # Обходим все значения категорий из фиктсуры для получения информации об одном объекте
        for category in Command.json_read_categories('catalog/fixtures/category.json'):
            category_for_create.append(
                Category(name=category['fields']['name'], description=category['fields']['description'])
            )

        # Создаем объекты в базе с помощью метода bulk_create()
        Category.objects.bulk_create(category_for_create)

        # Обходим все значения продуктов из фиктсуры для получения информации об одном объекте
        for product in Command.json_read_products('catalog/fixtures/products.json'):
            product_for_create.append(
                Product(name=product['fields']['name'],
                        category=Category.objects.get(id=product['fields']['category']),
                        price_per_product=product['fields']['price_per_product'])
            )

        # Создаем объекты в базе с помощью метода bulk_create()
        Product.objects.bulk_create(product_for_create)
