# Generated by Django 2.2.6 on 2019-11-11 08:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0006_remove_order_delivery'),
        ('inventory', '0004_auto_20191111_1315'),
    ]

    operations = [
        migrations.AddField(
            model_name='deliver',
            name='order',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='order.Order'),
        ),
    ]
