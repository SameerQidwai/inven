# Generated by Django 2.2.6 on 2019-11-11 08:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0004_auto_20191111_1315'),
        ('order', '0004_auto_20191109_1519'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='delivery',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='inventory.Deliver'),
            preserve_default=False,
        ),
    ]
