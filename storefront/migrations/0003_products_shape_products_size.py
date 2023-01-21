# Generated by Django 4.0.3 on 2023-01-17 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storefront', '0002_customercheckout_customerpayedproducts_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='shape',
            field=models.CharField(choices=[('Round', 'Round'), ('Square', 'Square')], default='Round', max_length=6),
        ),
        migrations.AddField(
            model_name='products',
            name='size',
            field=models.IntegerField(default='6'),
        ),
    ]
