# Generated by Django 4.2.5 on 2024-03-17 15:49

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Processing', 'Processing'), ('Shipped', 'Shipped'), ('Delivered', 'Delivered'), ('Canceled', 'Canceled')], default='Pending', max_length=50)),
                ('total_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('shipping_address', models.TextField(blank=True, null=True)),
                ('payment_method', models.CharField(choices=[('Credit Card', 'Credit Card'), ('Debit Card', 'Debit Card'), ('PayPal', 'PayPal'), ('Cash on Delivery', 'Cash on Delivery'), ('Mobile Money', 'Mobile Money'), ('Bank Transfer', 'Bank Transfer'), ('Other', 'Other')], default='Cash on Delivery', max_length=100)),
                ('extra_notes', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Order',
                'verbose_name_plural': 'Orders',
                'db_table': 'orders',
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('quantity', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(1000)])),
                ('sub_total_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='orders.order')),
            ],
            options={
                'verbose_name': 'Order Item',
                'verbose_name_plural': 'Order Items',
                'db_table': 'order_items',
                'ordering': ['-created'],
            },
        ),
    ]