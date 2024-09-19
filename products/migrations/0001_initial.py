# Generated by Django 5.1.1 on 2024-09-16 02:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('categories', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('price', models.CharField(max_length=8)),
                ('description', models.TextField()),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('image', models.ImageField(upload_to='products/media/uploads/')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='categories.category')),
            ],
        ),
    ]
