# Generated by Django 2.2.1 on 2019-06-11 02:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0016_order_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='submitted',
            field=models.BooleanField(default=False),
        ),
    ]