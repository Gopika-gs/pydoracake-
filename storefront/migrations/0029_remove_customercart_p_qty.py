# Generated by Django 4.0.3 on 2023-02-02 07:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('storefront', '0028_alter_customercart_p_qty'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customercart',
            name='p_qty',
        ),
    ]
