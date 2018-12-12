# Robert Wyżgolik, 297475
from typing import List, Union, Dict, TypeVar
from functools import reduce
import abc
import re
import unittest


class ServerError(Exception):
    pass


class Product:

    def __init__(self, name: str, price: float):
        self.name = name
        self.price = price

    def __str__(self):
        return '{} {}'.format(self.name, self.price)

    def __repr__(self):
        return self.__str__()


p1 = Product("XYZ12", 3.99)
p2 = Product("xz134", 4.12)
p3 = Product("xYz1", 3.17)
p4 = Product("X1z35", 4.99)
p5 = Product("sk1789", 5.58)
p6 = Product("kk13", 6.89)
p7 = Product("lolo15", 7.78)
p8 = Product("ZST15", 9.14)
p9 = Product("ZU145", 8.88)
p10 = Product("sD24", 14.25)
p11 = Product("yT248", 1.13)
p12 = Product("sty850", 4.85)
p13 = Product("UPs458", 99.99)


lst_2_2much = [p2, p6, p10, p9]
lst_2_ok = [p2, p6, p10]
lst_3_2much = [p1, p4, p12, p13, p3, p8]
lst_3_ok = [p1, p2, p8, p10, p5]


class Server(metaclass=abc.ABCMeta):

    max_numb = 3

    def __init__(self):
        pass

    @abc.abstractmethod
    def search_for_products(self, n: int = 1) -> List[Product]:
        raise NotImplementedError


class LstServer(Server):
    def __init__(self, lst_of_products: List[Product] = None):
        super().__init__()
        if lst_of_products is None:
            self.lst_of_products = []
        else:
            self.lst_of_products = lst_of_products

    def search_for_products(self, n: int = 1) -> List[Product]:
        pattern = re.compile('^[a-zA-Z]{{{n}}}\\d{{2,3}}'.format(n=n))
        products_found = [p for p in self.lst_of_products if re.match(pattern, p.name) is not None]
        if len(products_found) > Server.max_numb:
            raise ServerError
        return sorted(products_found, key=lambda p: p.price)


class DictServer(Server):
    def __init__(self, lst_of_products: Dict=None):
        super().__init__()
        if lst_of_products is None:
            self.lst_of_products = {}
        else:
            self.lst_of_products = {elem.name: elem for elem in lst_of_products}

    def search_for_products(self, n: int = 1) -> List[Product]:
        pattern = re.compile('^[a-zA-Z]{{{n}}}\\d{{2,3}}'.format(n=n))
        products_found = [val for key, val in self.lst_of_products.items() if re.match(pattern, key) is not None]
        if len(products_found) > Server.max_numb:
            raise ServerError
        return sorted(products_found, key=lambda p: p.price)


HelperType = TypeVar('HelperType', bound=Server)


class Client:
    def __init__(self, id_: int, server: HelperType):
        self.id = id_
        self.server = server

    def compute_overall_price(self, n: int = 3) -> Union[float, int]:
        try:
            lst_of_appropriate_products = self.server.search_for_products(n)
        except ServerError:
            return 0
        price = reduce(lambda x, y: x.price+y.price, lst_of_appropriate_products)
        return price


class TestServer(unittest.TestCase):

    def test_exception(self):
        products_to_test = [
            Product("XYZ15", 3.99),
            Product("xsd789", 4.55),
            Product("omg87", 9.990),
            Product("opI78", 2.25)
        ]
        products = [
            Product("xy12", 2.25),
            Product("xZ78", 6.68),
            Product("zT147", 5.57),
            Product("OM98", 4.49)
        ]
        serv_0 = LstServer(products_to_test)
        serv_1 = DictServer(products_to_test)
        serv_2 = LstServer(products)
        serv_3 = DictServer(products)

        with self.assertRaises(ServerError):
            serv_0.search_for_products(3)
            serv_1.search_for_products(3)
            serv_2.search_for_products(2)
            serv_3.search_for_products(2)

    def test_sort(self):
        products = [
            Product("xyz45", 3.33),
            Product("XsD789", 2.29),
            Product("Gts158", 5.59)
        ]
        products_sorted = [
            products[1],
            products[0],
            products[2]
        ]
        serv_0 = LstServer(products)
        serv_1 = DictServer(products)
        self.assertListEqual(serv_0.search_for_products(3), products_sorted)
        self.assertListEqual(serv_1.search_for_products(3), products_sorted)

    def test_return_value_when_exception_raised(self):
        products_3 = [
            Product("xzr89", 1.99),
            Product("xtY78", 6.69),
            Product("bUt78", 2.27),
            Product("FUT587", 3.38)
        ]

        products_2 = [
            Product("Ty150", 147.89),
            Product("Ty89", 5.98),
            Product("Hy89", 21.25),
            Product("aG258", 36.69)
        ]

        serv_0 = LstServer(products_3)
        serv_1 = DictServer(products_3)
        client_0 = Client(1, serv_0)
        client_1 = Client(2, serv_1)
        serv_2 = LstServer(products_2)
        serv_3 = DictServer(products_2)
        client_2 = Client(3, serv_2)
        client_3 = Client(4, serv_3)
        self.assertEqual(client_0.compute_overall_price(3), 0)
        self.assertEqual(client_1.compute_overall_price(3), 0)
        self.assertEqual(client_2.compute_overall_price(2), 0)
        self.assertEqual(client_3.compute_overall_price(2), 0)

if __name__ == '__main__':
    unittest.main()

# Robert Wyżgolik, 297475