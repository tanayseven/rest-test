import datetime
from datetime import timedelta
from json import JSONEncoder
from typing import Dict, List, Union

from http_quest.di import container
from http_quest.utilities import RandomWrapper


name_with_categories = {
    'Mobile Phone': 'Electronics',
    'Laptop': 'Electronics',
    'Charger': 'Electronics',
    'Rice': 'Food',
    'Wheat': 'Food',
    'Pulses': 'Food',
    'Milk': 'Food',
    'Shirt': 'Outfit',
    'Pants': 'Outfit',
    'T-Shirt': 'Outfit',
    'Skirt': 'Outfit',
    'Fight \'em': 'Gaming',
    'Race \'em': 'Gaming',
}


# class DateTime:
#     @inject
#     def __init__(self, datetime: datetime.datetime = datetime.datetime):
#         self._datetime = datetime

#     @property
#     def datetime(self):
#         return self._datetime


# injected_datetime = injector.get(DateTime)


class Product:
    def __init__(self, name: str, category: str, price: int, start_date,
                 end_date):

        self.name = name
        self.category = category
        self.price = price
        self.start_date = start_date
        self.end_date = end_date
        self.datetime_ = container.datetime

    def to_dict(self) -> dict:
        return {
            'name': self.name,
            'price': self.price,
            'start_date': self.start_date.isoformat(),
            'end_date': self.end_date.isoformat(),
        }

    def is_active(self):
        return self.start_date <= self.datetime_.now() <= self.end_date

    @classmethod
    def solution_count(cls, product_list: List['Product']) -> Dict[str, int]:
        return {
            'count': len(product_list)
        }

    @classmethod
    def solution_active_count(cls, product_list: List['Product']) -> Dict[str, int]:
        active_count = len([x for x in product_list if x.is_active()])
        return {
            'count': active_count
        }

    @classmethod
    def solution_active_date_count_categories(cls, product_list: List['Product']) -> Dict[str, int]:
        result = {x.category: 0 for x in product_list}
        for key in result.keys():
            result[key] += 1
        return result

    @classmethod
    def solution_total_value_for_active_date(cls, product_list: List['Product']) -> Dict[str, int]:
        return {'total_value': sum([x.price for x in product_list if x.is_active()])}

    @staticmethod
    def fn_for_solution(problem_number: int) -> Union['function', None]:
        try:
            return [
                Product.solution_count,
                Product.solution_active_count,
                Product.solution_active_date_count_categories,
                Product.solution_total_value_for_active_date,
            ][problem_number]
        except IndexError:
            return None


class ProductFactory:
    def __init__(self):
        self._random = container.random
        self._datetime = container.datetime

    def new_product(self, id_: int) -> Product:
        name = list(name_with_categories.keys())[id_]
        return Product(
            name,
            name_with_categories[name],
            self._random.randrange(100, 10000),
            self._datetime.now() - timedelta(days=self._random.randrange(2, 9)),
            self._datetime.now() + timedelta(days=self._random.randrange(2, 9)),
        )




class ProductCollection:
    @staticmethod
    def generate_products(count: int) -> List[Product]:
        product_factory: ProductFactory = ProductFactory()
        return [
            product_factory.new_product(x) for x in range(count)
        ]

    @staticmethod
    def to_dict(products: List['Product']) -> List[dict]:
        return [
            product.to_dict() for product in products
        ]
