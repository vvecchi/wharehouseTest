from django.test import TestCase
from .models import Article
from .models import Product
from .models import PartsAmount
from .parsejson import parse_inventory
from .parsejson import parse_products
from . import views
from django.test import Client


INVENTORY_FILENAME = 'wharehouseManagement/testData/inventory.json'
PRODUCTS_FILENAME = 'wharehouseManagement/testData/products.json'


def read_data(filename, parse_method):
    json_string = open(filename, 'r').read()
    parse_method(json_string)


def read_inventory(): read_data(INVENTORY_FILENAME, parse_inventory)


def read_products(): read_data(PRODUCTS_FILENAME, parse_products)


def load_data():
    read_inventory()
    read_products()

class LoadedDataTests(TestCase):
    def setUp(self) -> None:
        load_data()



class ReadFileTests(TestCase):
    def test_inventory_reader(self):
        read_inventory()
        leg = Article(art_id=1, name='leg', stock=12)
        self.assertEqual(leg, Article.objects.get(art_id=1))

    def test_product_reader(self):
        read_inventory()
        read_products()
        dining_chair = Product.objects.get(name='Dining Chair')
        self.assertTrue(len(dining_chair.contain_articles.all()) == 3)

    def testReloadData(self):
        read_inventory()
        db_leg = Article.objects.get(art_id=1)
        db_leg.stock = 1
        db_leg.save()
        leg = Article(art_id=1, name='leg', stock=12)
        self.assertNotEqual(leg, Article.objects.get(art_id=1))
        read_inventory()
        self.assertEqual(leg, Article.objects.get(art_id=1))

class ProductTests(LoadedDataTests):
       
    def test_availbility(self):
        dining_chair = Product.objects.get(name='Dining Chair')
        self.assertEquals(dining_chair.quantity, 2)

    def test_remove_product(self):
        dining_chair = Product.objects.get(name='Dining Chair')
        old_quantity = dining_chair.quantity
        leg = dining_chair.contain_articles.get(name='leg')
        old_stock = leg.stock
        amount_of = PartsAmount.objects.get(product=dining_chair, article=leg).amount_of

        dining_chair.remove()
        self.assertEquals(dining_chair.quantity, old_quantity - 1)
        self.assertEquals(dining_chair.contain_articles.get(name='leg').stock, old_stock - amount_of)

    
    def test_remove_soldout_product(self):
        dining_chair = Product.objects.get(name='Dining Chair')
        while(Product.objects.get(name='Dining Chair').quantity > 0):
            dining_chair.remove()
        with self.assertRaises(Exception) as context:
            dining_chair.remove()


class ViewTest(LoadedDataTests):

    def test_logged_view_allows_selling(self):
        pass