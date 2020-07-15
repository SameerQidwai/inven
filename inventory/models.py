from django.db import models
# from datetime import datetime

# from django.utils import timezone
from product.models import Product
from order.models import Order
from decimal import Decimal

# from order.models import Order
# from django.urls import reverse
# # # Create your models here

# class Deliver(models.Model):
#     order = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True, null=True)
#     is_deliver = models.BooleanField(default=False)
#     d_date = models.DateTimeField(verbose_name='Delivered Date')
#     reciverName = models.CharField(max_length=225)

#     # def __str__(self):
#     #     return self.is_deliver

#     # def __unicode__(self):
#     #     return 
#     # def deliverd():
#     #     if is_deliver:
#     # def get_delivery_url(self):
#     #     return reverse('yet', kwargs={'pk': self.id})

#     # def create_profile(sender, **kwargs):
#     # user = kwargs["instance"]
#     # if kwargs["created"]:
#     #     up = UserProfile(user=user, stuff=1, thing=2)
#     #     up.save()

#     # post_save.connect(create_profile, sender=User)

class Purchasereturn(models.Model): #Items of the order
    product = models.ForeignKey(Product, on_delete=models.PROTECT) 
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items_return')
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
