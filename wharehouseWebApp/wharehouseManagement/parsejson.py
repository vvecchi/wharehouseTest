import json
from .models import Article
from .models import Product
from .models import PartsAmount
from django.core.exceptions import ObjectDoesNotExist


def parse_inventory(json_string):
    inventory = json.loads(json_string)['inventory']
    for article in inventory:
        Article(**article).save()


def parse_products(json_string):
    products_dict = json.loads(json_string)['products']
    for product_dict in products_dict:
        try:
            product = Product.objects.get(name=product_dict['name'])
        except ObjectDoesNotExist:
            product = Product(name=product_dict['name'])
        product.save()
        for contained_article in product_dict['contain_articles']:
            article = Article.objects.get(art_id=contained_article['art_id'])
            part_amount = PartsAmount(product=product, article=article,
                                       amount_of=contained_article['amount_of'])
            part_amount.save()
                
