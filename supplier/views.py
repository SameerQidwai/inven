from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import CreateView, ListView, UpdateView
from django_tables2 import RequestConfig

from .forms import SupplierAddForm, SupplierEditForm
from .models import Supplier
from .tables import SupplierListTable

# Create your views here.

class SupplierAddView(CreateView):
    template_name = 'form.html'
    form_class = SupplierAddForm
    model = Supplier
    queryset = Supplier.objects.all()[:10]

    def get_success_url(self):
        self.new_object.refresh_from_db()
        # return reverse('newSupplier', kwargs={'pk': self.new_object.id})
        return reverse('newSupplier')

    def form_valid(self, form):
        object = form.save()
        object.refresh_from_db()
        self.new_object = object
        return super().form_valid(form)

class SupplierListView(ListView):
    template_name = 'SupplierList.html'
    model = Supplier
    paginate_by = 50

    def get_queryset(self):
        qs = Supplier.objects.all()
        if self.request.GET:
            qs = Supplier.filter_data(self.request, qs)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        suppliers = SupplierListTable(self.object_list)
        RequestConfig(self.request).configure(suppliers)
        context.update(locals())
        return context

class SupplierUpdateView(UpdateView):
    model = Supplier
    template_name = 'supplierUpdate.html'
    form_class = SupplierEditForm

    def get_success_url(self):
        return reverse('update_supplier', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        instance = self.object
        context.update(locals())
        return context


def delete_supplier(request, pk):
    instance = get_object_or_404(Supplier, id=pk)
    instance.delete()
    messages.warning(request, 'The product is deleted!')
    return redirect(reverse('supplierlist'))


def done_supplier_edit(request, pk):
    instance = get_object_or_404(Supplier, id=pk)
    instance.save()
    return redirect(reverse('supplierlist'))
