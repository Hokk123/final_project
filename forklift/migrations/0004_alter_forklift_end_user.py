# Generated by Django 4.1.3 on 2023-07-04 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forklift', '0003_alter_forklift_delivery_address_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='forklift',
            name='end_user',
            field=models.CharField(max_length=64),
        ),
    ]
