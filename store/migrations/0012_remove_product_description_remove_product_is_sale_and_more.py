# Generated by Django 4.2.17 on 2024-12-12 19:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0011_remove_product_image_alter_category_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='description',
        ),
        migrations.RemoveField(
            model_name='product',
            name='is_sale',
        ),
        migrations.RemoveField(
            model_name='product',
            name='more_info',
        ),
        migrations.RemoveField(
            model_name='product',
            name='sale_price',
        ),
    ]