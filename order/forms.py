from django import forms

from .models import Order
from supplier.models import Supplier


class BaseForm(forms.Form): #Create form by Models

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class OrderCreateForm(BaseForm, forms.ModelForm):   #New order Form
    title = forms.CharField()
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    supplier = forms.ModelChoiceField(label="Supplier Name",queryset=Supplier.objects.all())


    class Meta:
        model = Order
        fields = ['title','date', 'supplier']


class OrderEditForm(BaseForm, forms.ModelForm): #Edit existed form

    class Meta:
        model = Order
        fields = ['date', 'title', 'total_price', 'is_paid','delivery']