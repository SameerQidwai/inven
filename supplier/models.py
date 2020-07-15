from django.db import models
from django.urls import reverse
# from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
class Supplier(models.Model):
    # id= models.PositiveIntegerField(primary_key=True)
    sname= models.CharField(max_length=255)
    address= models.TextField(max_length=255,unique=True)
    email= models.CharField(max_length=255,unique=True)
    # mobile= PhoneNumberField(unique=True)
    mobile = models.CharField(max_length=12,unique=True)

    def __str__(self):
        return self.sname

    def get_supplier_url(self):
        return reverse('update_supplier', kwargs={'pk': self.id})

    @staticmethod
    def filter_data(request, queryset):
        search_name = request.GET.get('search_name', None)
        queryset = queryset.filter(sname__icontains=search_name ) if search_name else queryset
        return queryset