# Generated by Django 4.2.5 on 2024-05-13 23:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('reviews', '0001_initial'),
        ('customers', '0002_initial'),
        ('products', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='productreview',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='customers.customer'),
        ),
        migrations.AddField(
            model_name='productreview',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='products.product'),
        ),
        migrations.AlterUniqueTogether(
            name='productreview',
            unique_together={('product', 'customer')},
        ),
    ]
