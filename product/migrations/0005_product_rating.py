# Generated by Django 5.1.3 on 2024-12-01 20:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_product_in_stock'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='rating',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
