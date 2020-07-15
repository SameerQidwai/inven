from django.urls import path

from inventory import views
from inventory.views import HomepageView, purchasereturnView, ajax_return_order_item#, Delivery


urlpatterns = [
    # path('',views.product,name='home'),
    path('', HomepageView.as_view(), name='homepage'),
    # path('yet/<int:pk>/', Delivery.as_view(), name='yet'),
    path('yet/<int:pk>/', purchasereturnView.as_view(), name='return'),

    path('ajax/return-product/<int:pk>/<slug:action>', ajax_return_order_item, name='ajax_return'),

]