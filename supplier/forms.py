from django import forms
from .models import Supplier
# from phonenumber_field.formfields import PhoneNumberField

class BaseForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

class SupplierAddForm(BaseForm, forms.ModelForm):
    sname = forms.CharField(label='Supplier Name')
    email = forms.CharField(label='Email')
    address = forms.Textarea()
    # mobile = PhoneNumberField(label='Contact No')
    mobile = forms.CharField(label='Contact No')

    class Meta:
        model = Supplier
        fields = ['sname','email','address','mobile']

class SupplierEditForm(BaseForm, forms.ModelForm):
    sname = forms.CharField(label='Supplier Name')
    email = forms.CharField(label='Email')
    address = forms.Textarea()
    # mobile = PhoneNumberField(label='Contact No')
    mobile = forms.CharField(label='Contact No')
    
    class Meta:
        model = Supplier
        fields = ['sname','email','address','mobile']
