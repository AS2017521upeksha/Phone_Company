# Generated by Django 5.1 on 2024-11-03 12:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_alter_order_customer'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Profile',
        ),
    ]