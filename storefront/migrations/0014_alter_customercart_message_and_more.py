# Generated by Django 4.0.3 on 2023-01-19 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storefront', '0013_remove_customercart_date_remove_customercart_pincode_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customercart',
            name='message',
            field=models.CharField(max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name='customercheckout',
            name='date',
            field=models.CharField(max_length=10),
        ),
    ]
