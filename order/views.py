import datetime

from django.contrib import messages
from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.generic import CreateView, ListView, UpdateView
from django_tables2 import RequestConfig
from easy_pdf import rendering


from product.models import Category, Product
from product.tables import ProductTable

from .forms import OrderCreateForm, OrderEditForm
from .models import Order, OrderItem
from .tables import GoodTable, OrderItemTable, OrderTable, PurchaseInvoice

# from multiple_forms import MultipleFormsView
# import pdb
# from django.utils.decorators import method_decorator
# from django.contrib.admin.views.decorators import staff_member_required
# Create your views here.


# #@method_decorator(staff_member_required, name='dispatch')

def auto_create_order_view(request):    #Create new Order don't know if need
    new_order = Order.objects.create(
        title='Order 66',
        date=datetime.datetime.now()
    )
    new_order.title = f'Order - {new_order.id}'
    new_order.save()
    return redirect(new_order.get_edit_url())


#@method_decorator(staff_member_required, name='dispatch')
class OrderListView(ListView):  #Show All available Order
    template_name = 'list.html'
    model = Order
    paginate_by = 50

    def get_queryset(self): #search name
        qs = Order.objects.all()
        if self.request.GET:
            qs = Order.filter_data(self.request, qs)
        return qs

    def get_context_data(self, **kwargs): #show order
        context = super().get_context_data(**kwargs)
        orders = OrderTable(self.object_list)
        RequestConfig(self.request).configure(orders)
        context.update(locals())
        return context



#@method_decorator(staff_member_required, name='dispatch')
class CreateOrderView(CreateView):  #new Odrder form
    template_name = 'form.html'
    form_class = OrderCreateForm
    model = Order

    def get_success_url(self):  
        self.new_object.refresh_from_db()
        return reverse('update_order', kwargs={'pk': self.new_object.id})

    def form_valid(self, form):
        object = form.save()
        object.refresh_from_db()
        self.new_object = object
        return super().form_valid(form)


#@method_decorator(staff_member_required, name='dispatch')
class OrderUpdateView(UpdateView):  #Update existed Order
    model = Order
    template_name = 'order_update.html'
    form_class = OrderEditForm

    def get_success_url(self):
        return reverse('update_order', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        instance = self.object
        qs_p = Product.objects.filter()[:12]   #Product data in a object
        products = ProductTable(qs_p)   #show All products as Table
        order_items = OrderItemTable(instance.order_items.all())  #show order product  
        RequestConfig(self.request).configure(products)
        RequestConfig(self.request).configure(order_items)
        context.update(locals())
        return context

class GoodTableView(ListView):  #Good Received Note 
    template_name = 'note.html'
    model = OrderItem
    paginate_by = 50


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id = self.kwargs['pk']  #take primary key
        instance = Order.objects.filter(id=id).first() #call Order with primary key
        grnote = GoodTable(instance.order_items.all())
        RequestConfig(self.request).configure(grnote)
        context.update(locals())
        return context


class Invoice(ListView):  #Good Received Note 
    template_name = 'invoice.html'
    model = OrderItem
    paginate_by = 50


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id = self.kwargs['pk']  #take primary key
        instance = Order.objects.filter(id=id).first() #call Order with primary key
        invoice = PurchaseInvoice(instance.order_items.all())
        RequestConfig(self.request).configure(invoice)
        context.update(locals())
        return context



def delete_order(request, pk):  #Delete Order from the primary key
    instance = get_object_or_404(Order, id=pk)
    instance.delete()
    messages.warning(request, 'The order is deleted!')
    return redirect(reverse('homepage'))



def done_order_view(request, pk):   #ave order
    instance = get_object_or_404(Order, id=pk)
    # instance.is_paid = True
    # instance.save()
    return redirect(reverse('homepage'))



def ajax_add_product(request, pk, dk): #add product in OrderItem cart
    instance = get_object_or_404(Order, id=pk)
    product = get_object_or_404(Product, id=dk)
    order_item, created = OrderItem.objects.get_or_create(order=instance, product=product)
    if created:
        order_item.qty = 1
        order_item.price = product.price
        # order_item.discount_price = product.discount_value
    else:
        order_item.qty += 1
    order_item.save()
    product.qty -= 1
    product.save()
    instance.refresh_from_db()
    order_items = OrderItemTable(instance.order_items.all())
    RequestConfig(request).configure(order_items)
    data = dict()
    data['result'] = render_to_string(template_name='include/order_container.html',
                                      request=request,
                                      context={'instance': instance,
                                               'order_items': order_items
                                               }
                                    )
    return JsonResponse(data)



def ajax_modify_order_item(request, pk, action):    #add product and delete product
    order_item = get_object_or_404(OrderItem, id=pk)
    product = order_item.product
    instance = order_item.order
    if action == 'remove':
        if order_item.qty > 1:
            order_item.qty -= 1
            product.qty += 1
        # if order_item.qty < 1: order_item.qty = 1
    if action == 'add':
        order_item.qty += 1
        product.qty -= 1
    product.save()
    order_item.save()
    if action == 'delete':
        order_item.delete()
    data = dict()
    instance.refresh_from_db()
    order_items = OrderItemTable(instance.order_items.all())  
    RequestConfig(request).configure(order_items)
    data['result'] = render_to_string(template_name='include/order_container.html',
                                      request=request,
                                      context={
                                          'instance': instance,
                                          'order_items': order_items
                                      })
    return JsonResponse(data)



def ajax_search_products(request, pk): #search product by name
    instance = get_object_or_404(Order, id=pk)
    q = request.GET.get('q', None)
    products = Product.broswer.filter(pname__startswith=q) if q else Product.broswer()
    products = ProductTable(products)
    RequestConfig(request).configure(products)
    data = dict()
    data['products'] = render_to_string(template_name='include/product_container.html',
                                        request=request,
                                        context={
                                            'products': products,
                                            'instance': instance
                                        })
    return JsonResponse(data)



def order_action_view(request, pk, action): #if paid or not
    instance = get_object_or_404(Order, id=pk)
    # if action == 'is_paid':
    #     instance.is_paid = True
    #     instance.save()
    if action == 'delete':
        instance.delete()
    return redirect(reverse('homepage'))
    
# def order_dliver(request, )


def ajax_calculate_results_view(request):
    orders = Order.filter_data(request, Order.objects.all())
    total_price, total_paid_value, remaining_value, data = 0, 0, 0, dict()
    if orders.exists():
        total_price = orders.aggregate(Sum('final_value'))['final_value__sum']
        total_paid_value = orders.filter(is_paid=True).aggregate(Sum('final_value'))['final_value__sum'] if\
            orders.filter(is_paid=True) else 0
        remaining_value = total_price - total_paid_value
    total_price, total_paid_value, remaining_value = f'{total_price}',\
                                                     f'{total_paid_value}', f'{remaining_value}'
    data['result'] = render_to_string(template_name='include/result_container.html',
                                      request=request,
                                      context=locals())
    return JsonResponse(data)

def ajax_calculate_category_view(request):
    orders = Order.filter_data(request, Order.objects.all())
    order_items = OrderItem.objects.filter(order__in=orders)
    category_analysis = order_items.values_list('product__category__title').annotate(qty=Sum('qty'),
                                                                                      total_incomes=Sum('total_price')
                                                                                      )
    data = dict()
    category = True
    data['result'] = render_to_string(template_name='include/result_container.html',
                                      request=request,
                                      context=locals()
                                      )
    return JsonResponse(data)
