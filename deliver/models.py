from django.db import models
from inventry.models import Order
# Create your models here.

class Deliver(models.Model):
    isdeliver = bool()
    

    def __str__(self):
        return 

    def __unicode__(self):
        return 
