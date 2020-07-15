from django.urls import path

from product import views
from product.views import (ProductTableView, ProductListView, delete_product, ProductUpdateView,delete_product,
                             done_product_edit )

urlpatterns = [
    # path('',views.product,name='home'),
    path('Products/', ProductListView.as_view(), name='product_list'),
    path('Addproduct/', ProductTableView.as_view(), name='add-product'),
    path('update-product/<int:pk>/', ProductUpdateView.as_view(), name='update_product'),
    path('delete-product/<int:pk>/', delete_product, name='delete_product'),
    path('done-product/<int:pk>/', done_product_edit, name='done_product'),


]