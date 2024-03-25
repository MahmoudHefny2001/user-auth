# Generated by Django 4.2.5 on 2024-03-23 23:13

from django.db import migrations, models
import django_extensions.db.fields
import reviews.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ProductReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('rating', models.IntegerField(validators=[reviews.validators.validate_rating])),
                ('review', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Product Review',
                'verbose_name_plural': 'Product Reviews',
                'db_table': 'product_reviews',
                'ordering': ['-created'],
            },
        ),
    ]