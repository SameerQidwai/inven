from django.contrib import admin

from .models import Supplier 
# Register your models here.
@admin.register(Supplier)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['sname', 'address','email', 'mobile']
    search_fields = ['sname']
    list_per_page = 50
    fields = ['sname', 'address','email', 'mobile']
