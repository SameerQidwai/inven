from django.db.models import Sum
from django.views.generic import ListView, UpdateView, CreateView
from django_tables2 import RequestConfig
from django.urls import reverse
from django.http import JsonResponse

from order.models import Order, OrderItem
from order.tables import OrderTable, OrderItemTable
from order.forms import OrderEditForm

from product.models import Product
from product.tables import ProductTable

from .tables import ReturnTable
from .models import Purchasereturn

from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string

# from .models import Deliver

# from .forms import OrderDeliveryForm 


# from pdb import set_trace
# from django.contrib.admin.views.decorators import staff_member_required
# Create your views here.


# #@method_decorator(staff_member_required, name='dispatch')
class HomepageView(ListView):   #HomePage
    template_name = 'index.html' #html file where to show
    model = Order       #model to call
    queryset = Order.objects.all()[:10] #call all the Order 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        orders = Order.objects.all() #save all Order in the variable to call
        total_sales = orders.aggregate(Sum('total_price'))['total_price__sum'] if orders.exists() else 0  #show total Order price
        paid_value = orders.filter(is_paid=True).aggregate(Sum('total_price'))['total_price__sum']\
            if orders.filter(is_paid=True).exists() else 0 #show the paid Order Price
        remaining = total_sales - paid_value #show unpaid Order price
        diviner = total_sales if total_sales > 0 else 1 
        paid_percent, remain_percent = round((paid_value/diviner)*100, 1), round((remaining/diviner)*100, 1) #paid and unpaid %price
        total_sales = f'{total_sales}'
        paid_value = f'{paid_value}'
        remaining = f'{remaining}'
        orders = OrderTable(orders)     #call ALL Orders to show As Table
        RequestConfig(self.request).configure(orders)   
        context.update(locals())
        return context

class purchasereturnView(UpdateView):  #Update existed Order
    model = Order
    template_name = 'purchaseR.html'
    form_class = OrderEditForm

    def get_success_url(self):
        return reverse('update_order', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        instance = self.object
        # qs_p = Product.objects.filter()[:12]   #Product data in a object
        # products = ProductTable(qs_p)   #show All products as Table
        order_items = ReturnTable(instance.order_items.all())  #show order product  
        # RequestConfig(self.request).configure(products)
        RequestConfig(self.request).configure(order_items)
        context.update(locals())
        return context

# class Delivery(UpdateView):  #new Odrder form

#     template_name = 'yet.html'
#     form_class = OrderDeliveryForm
#     model = Deliver

#     def get_success_url(self):
#         return reverse('update_order', kwargs={'pk': self.object.id})

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context.update(locals())
#         return context


def ajax_return_order_item(request, pk, action):    #add product and delete product
    order_item = get_object_or_404(OrderItem, id=pk)
    product = order_item.product
    instance = order_item.order
    
    qs = Purchasereturn.objects.all()
    qs.id = order_item.id
    qs.order = order_item.order
    qs.product = order_item.product
    qs.price = order_item.price

    if action == 'remove':
        if order_item.qty > 1:
            order_item.qty -= 1
            product.qty += 1
            qs.product += 1
    product.save()
    order_item.save()
    if action == 'delete':
        order_item.delete()
    data = dict()
    instance.refresh_from_db()
    order_items = ReturnTable(instance.order_items.all())  
    RequestConfig(request).configure(order_items)
    data['result'] = render_to_string(template_name='include/order_container.html',
                                      request=request,
                                      context={
                                          'instance': instance,
                                          'order_items': order_items
                                      })
    return JsonResponse(data)

