# Generated by Django 4.0.3 on 2023-01-18 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storefront', '0011_alter_customercart_pincode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customercart',
            name='pincode',
            field=models.IntegerField(default='000000', max_length=6),
        ),
    ]
