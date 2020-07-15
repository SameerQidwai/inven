from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.db.models import Sum
from datetime import datetime
from django.dispatch import receiver
from django.shortcuts import get_object_or_404
from django.db.models.signals import post_delete
from decimal import Decimal
from .managers import  OrderManager
import product.models as product
from supplier.models import Supplier
# from inventory.models import Deliver
import pdb

# Create your models here.


class Order(models.Model): 
    title= models.CharField(max_length=255)
    timestamp= models.DateTimeField(auto_now_add=True) 
    date = models.DateField(default=datetime.now)
    is_paid= models.BooleanField(default=False)  
    total_price = models.DecimalField(default=0.00, decimal_places=2, max_digits=20)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    delivery = models.BooleanField(default=False)

    objects = models.Manager()
    browser = OrderManager()
    
    class Meta:
        ordering = ['-date']

    def save(self, *args, **kwargs): #save total price of the products
        order_items = self.order_items.all()
        self.total_price = order_items.aggregate(Sum('total_price'))['total_price__sum'] if order_items.exists() else 0.00
        super().save(*args, **kwargs)
    
    def __str__(self):  #Add new product 
        return self.title if self.title else 'New Order'

    def get_edit_url(self): #goto update_order function
        return reverse('update_order', kwargs={'pk': self.id})

    def get_delete_url(self): #goto delete_order 
        return reverse('delete_order', kwargs={'pk': self.id})

    def tag_total_price(self):  #save it woth Currency 
        return f'{self.total_price}'
    tag_total_price.short_description = 'price'

    @staticmethod   #filter funtion to search
    def filter_data(request, queryset):
        search_name = request.GET.get('search_name', None)
        date_start = request.GET.get('date_start', None)
        date_end = request.GET.get('date_end', None)
        queryset = queryset.filter(title__contains=search_name) if search_name else queryset # searc by date from, till
        if date_end and date_start and date_end >= date_start:
            date_start = datetime.datetime.strptime(date_start, '%m/%d/%Y').strftime('%Y-%m-%d')
            date_end = datetime.datetime.strptime(date_end, '%m/%d/%Y').strftime('%Y-%m-%d')
            print(date_start, date_end)
            queryset = queryset.filter(date__range=[date_start, date_end])
        return queryset

class OrderItem(models.Model): #Items of the order
    product = models.ForeignKey(product.Product, on_delete=models.PROTECT) 
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    qty = models.PositiveIntegerField(default=1)
    price = models.DecimalField(default=0.00, decimal_places=2, max_digits=20)
    total_price = models.DecimalField(default=0.00, decimal_places=2, max_digits=20)

    def __str__(self):
        return {self.product.pname}

    def save(self, *args, **kwargs):  #set total price of the porduct
        self.total_price = Decimal(self.qty) * Decimal(self.price)
        self.price = Decimal(self.product.price) #save price of product from Product Model
        super().save(*args, **kwargs)
        self.order.save()

    def tag_total_price(self):  #save with Currency
        return f'{self.total_price}'
    tag_total_price.short_description = 'price'


    def tag_price(self):
        return f'{self.price}'


@receiver(post_delete, sender=OrderItem) #delete product from Product Model after Order
def delete_order_item(sender, instance, **kwargs):
    product = instance.product
    product.qty += instance.qty
    product.save()
    instance.order.save()


