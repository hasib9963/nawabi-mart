# Generated by Django 4.2.7 on 2024-09-17 21:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0005_remove_order_is_paid_order_email_order_name_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='total',
            new_name='total_price',
        ),
    ]
