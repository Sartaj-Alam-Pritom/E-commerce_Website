# Generated by Django 5.1.3 on 2024-12-01 20:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0005_product_rating'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='rating',
        ),
    ]