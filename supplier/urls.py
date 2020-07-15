from django.urls import path

from supplier import views
from supplier.views import (SupplierAddView, SupplierListView, SupplierUpdateView, delete_supplier, done_supplier_edit)

urlpatterns = [
    # path('',views.product,name='home'),
        path('Supplier/', SupplierListView.as_view(), name='supplierlist'),
        path('newsupplier/', SupplierAddView.as_view(), name='newSupplier'),
        path('update-supplier/<int:pk>/', SupplierUpdateView.as_view(), name='update_supplier'),
        path('delete-supplier/<int:pk>/', delete_supplier, name='delete_supplier'),
        path('saved-supplier/<int:pk>/', done_supplier_edit, name='save-supplier'),


]