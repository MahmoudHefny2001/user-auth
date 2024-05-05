# Generated by Django 4.2.5 on 2024-03-17 15:49

from django.db import migrations, models
import django_extensions.db.fields
import users.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ContactForm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('phone_number', models.CharField(max_length=12, validators=[users.validators.valid_phone_number])),
                ('message', models.TextField()),
            ],
            options={
                'verbose_name': 'Contact Form',
                'verbose_name_plural': 'Contact Forms',
                'db_table': 'contact_form',
                'ordering': ['-created'],
            },
        ),
    ]
