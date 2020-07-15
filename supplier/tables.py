import django_tables2 as tables

from.models import Supplier

class SupplierListTable(tables.Table):
    action = tables.TemplateColumn(
        '<a href="{{ record.get_supplier_url }}" class="btn btn-info"><i class="fa fa-edit"></i></a>',
         orderable=False
        )

    class Meta:
        model = Supplier
        template_name = 'django_tables2/bootstrap.html'
        fields = ['sname', 'email', 'mobile', 'address']

