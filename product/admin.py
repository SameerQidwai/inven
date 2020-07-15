from django.contrib import admin

# Register your models here.
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['title']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['pname', 'category','price', 'qty', 'tag_total_price']
    list_select_related = ['category']
    list_filter = ['category']
    search_fields = ['pname']
    list_per_page = 50
    fields = ['pname', 'category', 'qty', 'price', 'tag_total_price']
    autocomplete_fields = ['category']
    readonly_fields = ['tag_total_price']