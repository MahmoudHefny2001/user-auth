# Generated by Django 4.2.5 on 2024-05-05 20:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('merchants', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='merchant',
            name='terms_agreement',
            field=models.BooleanField(blank=True, default=True, null=True),
        ),
        migrations.AlterField(
            model_name='merchantprofile',
            name='image',
            field=models.ImageField(blank=True, default=None, null=True, upload_to='merchants/profiles/'),
        ),
    ]
