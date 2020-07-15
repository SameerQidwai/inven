import django_tables2 as tables

from order.models import OrderItem #, Order


# class OrderTable(tables.Table): #show all Order in a Table
#     tag_total_price = tables.Column(orderable=False, verbose_name='Value')
#     action = tables.TemplateColumn(
#         '<a href="{{ record.get_edit_url }}" class="btn btn-info"><i class="fa fa-edit"></i></a>', orderable=False
#         )

#     class Meta:
#         model = Order
#         template_name = 'django_tables2/bootstrap.html'
#         fields = ['date', 'title', 'tag_total_price']

class ReturnTable(tables.Table): #show Product in Order Cart
    tag_total_price = tables.Column(orderable=False, verbose_name='Price')
    action = tables.TemplateColumn('''
            <button data-href="{% url "ajax_return" record.id "remove" %}" class="btn btn-warning edit_button"><i class="fa fa-arrow-down"></i></button>
            <button data-href="{% url "ajax_return" record.id "delete" %}" class="btn btn-danger edit_button"><i class="fa fa-trash"></i></button>
    ''', orderable=False)

    class Meta:
        model = OrderItem
        template_name = 'django_tables2/bootstrap.html'
        fields = ['product', 'qty', 'tag_total_price']

# class GoodTable(tables.Table):  #show Product in Good Received Note document
#     product = tables.Column(verbose_name= 'Product') 
#     qty = tables.Column(verbose_name= 'Order Quantity') 
#     price = tables.Column(verbose_name= 'Price', orderable=False)
#     total_price = tables.Column(verbose_name= 'Total Price', orderable=False)
#     dqty = tables.Column(default=' ', verbose_name= 'Delivered Quantity', orderable=False)
#     comment = tables.Column(default=' ', orderable=False)
        
#     class Meta:
#         model = OrderItem
#         template_name = 'django_tables2/bootstrap.html'
#         fields = ['product', 'dqty', 'qty', 'price', 'total_price', 'comment']