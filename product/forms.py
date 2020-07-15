from django import forms

from .models import Product, Category



class BaseForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class ProductCreateForm(BaseForm, forms.ModelForm):
    category = forms.ModelChoiceField(label="Category",queryset=Category.objects.all())
    pname = forms.CharField(label='Item Name', widget=forms.TextInput(attrs={'placeholder': 'Product Name'}))
    price = forms.DecimalField(label='price')
    qty = forms.IntegerField(label='Quantity') 
    class Meta:
        model = Product
        fields = ['category','pname','price','qty']


class ProductEditForm(BaseForm, forms.ModelForm):
    pname = forms.CharField(label='Item Name')
    price = forms.DecimalField(label='price')
    qty = forms.IntegerField(label='Quantity') 
    class Meta:
        model = Product
        fields = ['pname', 'price', 'qty']



