from django.shortcuts import render, redirect
from django_tables2 import RequestConfig
# from .tables import ProductTable
from django.urls import reverse
from django.views.generic import UpdateView, CreateView,ListView
from .forms import ProductCreateForm, ProductEditForm
from .models import Product
from django.contrib import messages
from .tables import ProductListTable
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string
import pdb
# Create your views here.


class ProductListView(ListView): #Show All product via Table 
    template_name = 'productList.html'
    model = Product
    paginate_by = 50

    def get_queryset(self): #search function
        qs = Product.objects.all()
        if self.request.GET:
            qs = Product.filter_data(self.request, qs)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = ProductListTable(self.object_list) #All Product Table
        RequestConfig(self.request).configure(products)
        context.update(locals())
        return context


class ProductTableView(CreateView):  #Add new Product
    template_name = 'form.html'
    form_class = ProductCreateForm #from this form in the forms
    model = Product
    queryset = Product.objects.all()[:10]

    def get_success_url(self):
        self.new_object.refresh_from_db()
        # return reverse('add-product', kwargs={'pk': self.new_object.id})
        return reverse('add-product')

    def form_valid(self, form):
        object = form.save()
        object.refresh_from_db()
        self.new_object = object
        return super().form_valid(form)


class ProductUpdateView(UpdateView):
    model = Product
    template_name = 'product_update.html'
    form_class = ProductEditForm

    def get_success_url(self):
        return reverse('update_product', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        instance = self.object
        context.update(locals())
        return context

def delete_product(request, pk):
    instance = get_object_or_404(Product, id=pk)
    instance.delete()
    messages.warning(request, 'The product is deleted!')
    return redirect(reverse('product_list'))


def done_product_edit(request, pk):
    instance = get_object_or_404(Product, id=pk)
    instance.save()
    return redirect(reverse('product_list'))



