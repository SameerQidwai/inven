from django.urls import path

from order import views
from order.views import ( OrderUpdateView, CreateOrderView, delete_order,
                            OrderListView, done_order_view, auto_create_order_view,
                            ajax_add_product, ajax_modify_order_item, ajax_search_products, ajax_calculate_results_view,
                             order_action_view, ajax_calculate_category_view,GoodTableView,Invoice
                             )


urlpatterns = [
    path('order-list/', OrderListView.as_view(), name='order_list'),
    path('create/', CreateOrderView.as_view(), name='create-order'),
    path('create-auto/', auto_create_order_view, name='create_auto'),
    path('update/<int:pk>/', OrderUpdateView.as_view(), name='update_order'),
    path('done/<int:pk>/', done_order_view, name='done_order'),
    path('delete/<int:pk>/', delete_order, name='delete_order'),
    path('action/<int:pk>/<slug:action>/', order_action_view, name='order_action'),
    path('delete/<int:pk>/', delete_order, name='delete_order'),
    path('Good-note/<int:pk>/', GoodTableView.as_view(), name='grnote'),
    path('Invoice/<int:pk>/', Invoice.as_view(), name='invoice'),


    #ajax
    path('ajax/search-products/<int:pk>/', ajax_search_products, name='ajax-search'),
    path('ajax/add-product/<int:pk>/<int:dk>/', ajax_add_product, name='ajax_add'),
    path('ajax/modify-product/<int:pk>/<slug:action>', ajax_modify_order_item, name='ajax_modify'),
    path('ajax/calculate-results/', ajax_calculate_results_view, name='ajax_calculate_result'),
    path('ajax/calculate-category-results/', ajax_calculate_category_view, name='ajax_category_result'),


]