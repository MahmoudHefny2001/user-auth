# Generated by Django 4.2.5 on 2024-05-15 21:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0002_initial'),
        ('carts', '0005_remove_cart_item_quantity_remove_cart_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='customer',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='carts', to='customers.customer'),
        ),
    ]
