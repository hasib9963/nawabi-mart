# Generated by Django 4.2.7 on 2024-09-18 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0013_remove_cartitem_price_orderitem_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
