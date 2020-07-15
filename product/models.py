from django.db import models
from .managers import ProductManager
from decimal import Decimal
import datetime
from django.urls import reverse

# Create your models here.

class Category(models.Model):
    title = models.CharField(max_length=150, unique=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.title


class Product(models.Model): 
    pname = models.CharField('Item',max_length=255,unique=True)
    price = models.DecimalField(default=0.00, decimal_places=2, max_digits=10)
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)
    qty = models.PositiveIntegerField(default=0)
    total_price = models.DecimalField(default=0.00, decimal_places=2, max_digits=10)

    objects = models.Manager()
    broswer = ProductManager()

    class Meta:
        verbose_name_plural = 'Product'

    def save(self, *args, **kwargs):    #save total price of product
        self.total_price = Decimal(self.qty) * Decimal(self.price)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.pname

    def tag_price(self): #CURRENCY
        return self.price

    def get_url(self):
        return reverse('update_product', kwargs={'pk': self.id})
    
    def tag_total_price(self): #CURRENCY
        return self.total_price
    tag_total_price.short_description = 'Total price'

    @staticmethod   #search by name
    def filter_data(request, queryset):
        search_name = request.GET.get('search_name', None)
        queryset = queryset.filter(pname__icontains=search_name ) if search_name else queryset
        return queryset
