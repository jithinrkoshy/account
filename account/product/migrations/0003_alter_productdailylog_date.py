# Generated by Django 3.2 on 2021-04-27 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_alter_productdailylog_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productdailylog',
            name='date',
            field=models.DateField(unique=True),
        ),
    ]
