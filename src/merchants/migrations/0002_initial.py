# Generated by Django 4.2.5 on 2024-04-17 06:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('merchants', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MerchantBridge',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('users.user',),
        ),
        migrations.CreateModel(
            name='Merchant',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('address', models.TextField(blank=True, null=True)),
                ('payment_information', models.TextField(blank=True, null=True)),
                ('terms_agreement', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'merchants',
            },
            bases=('merchants.merchantbridge',),
        ),
        migrations.AddField(
            model_name='merchantprofile',
            name='merchant',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to='merchants.merchant'),
        ),
    ]
