import re
from django.core.validators import MinValueValidator
from django.db import models
from django.db import transaction

class Article(models.Model):
    """Articles have an Id, a name and stock information and are used to build products"""
    art_id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=200)
    stock = models.IntegerField(validators=[MinValueValidator(0)])

    def __str__(self) -> str:
        return self.name + ": " + str(self.stock) + " id: " + str(self.art_id)

    def __eq__(self, other) -> bool: # overrding '==' so testing code gets simpler
        if not isinstance(other, self.__class__):
            return False
        equals = self.art_id == other.art_id
        equals = equals and (self.name == other.name)
        equals = equals and (self.stock == other.stock)
        return equals

class Product(models.Model):
    """Products have a name and are made of articles"""
    name = models.CharField(max_length=200)
    contain_articles = models.ManyToManyField('Article', through='PartsAmount',
                                              related_name="parts")

    @property
    def quantity(self) -> int:
        """Number of available products, based on the stock of its constituent articles"""
        parts = PartsAmount.objects.filter(product=self)
        return min(map(lambda part: part.article.stock//part.amount_of, parts))

    @transaction.atomic
    def remove(self):
        """Remove a product by going through its articles and removing the amount needed from each"""
        if self.quantity <= 0:
            raise Exception("Trying to remove sold out product")
        for parts_amount in PartsAmount.objects.filter(product=self):
            article = parts_amount.article
            article.stock -= parts_amount.amount_of
            article.save()


    def __str__(self) -> str:
        return self.name


class PartsAmount(models.Model):
    """PartsAmount define the relationship between a Product an its constituent articles"""
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    article = models.ForeignKey('Article', on_delete=models.CASCADE)
    amount_of = models.IntegerField() #Number of articles of this kind needed for the product

    def __str__(self) -> str:
        return self.article.name + ": " + str(self.amount_of)
