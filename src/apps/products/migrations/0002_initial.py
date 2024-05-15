# Generated by Django 4.2.5 on 2024-05-13 23:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('merchants', '0002_initial'),
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='merchant',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='products', to='merchants.merchant'),
        ),
        migrations.AlterUniqueTogether(
            name='productcolor',
            unique_together={('product', 'color')},
        ),
    ]
