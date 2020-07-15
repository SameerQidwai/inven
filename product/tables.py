import django_tables2 as tables

from .models import Product

class ProductTable(tables.Table):
    tag_price = tables.Column(orderable=False, verbose_name='Price')
    action = tables.TemplateColumn(
        '<button class="btn btn-info add_button" data-href="{% url "ajax_add" instance.id record.id %}">Add!</a>',
        orderable=False
    )

    class Meta:
        model = Product
        template_name = 'django_tables2/bootstrap.html'
        fields = ['pname', 'category', 'qty', 'tag_price']

class ProductListTable(tables.Table):
    tag_price = tables.Column(orderable=False, verbose_name='Price')
    action = tables.TemplateColumn(
        '<a href="{{ record.get_url }}" class="btn btn-info"><i class="fa fa-edit"></i></a>',
         orderable=False
        )

    class Meta:
        model = Product
        template_name = 'django_tables2/bootstrap.html'
        fields = ['pname', 'category', 'qty', 'tag_price']

