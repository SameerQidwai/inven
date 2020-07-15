from django import forms

# from .models import Deliver
# from order.models import Order

# class BaseForm(forms.Form): #Create form by Models

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         for field_name, field in self.fields.items():
#             field.widget.attrs['class'] = 'form-control'


# class OrderDeliveryForm(BaseForm, forms.ModelForm): #Edit existed form
#     d_date= forms.DateTimeField(required=False,widget=forms.DateInput(attrs={'type': 'date'}))
#     class Meta:
#         model = Deliver
#         fields = ['is_deliver', 'd_date', 'reciverName']