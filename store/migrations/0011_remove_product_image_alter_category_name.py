# Generated by Django 4.2.17 on 2024-12-12 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0010_alter_order_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='image',
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=10),
        ),
    ]
