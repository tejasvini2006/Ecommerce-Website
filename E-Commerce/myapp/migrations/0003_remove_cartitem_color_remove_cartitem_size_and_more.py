# Generated by Django 5.1.6 on 2025-03-29 07:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_shopkeeper_userprofile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitem',
            name='color',
        ),
        migrations.RemoveField(
            model_name='cartitem',
            name='size',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='color',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='size',
        ),
        migrations.RemoveField(
            model_name='product',
            name='color',
        ),
        migrations.RemoveField(
            model_name='product',
            name='size',
        ),
    ]
