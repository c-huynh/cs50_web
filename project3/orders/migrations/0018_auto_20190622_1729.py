# Generated by Django 2.2.1 on 2019-06-22 17:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0017_order_submitted'),
    ]

    operations = [
        migrations.AlterField(
            model_name='platter',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.PlatterType'),
        ),
    ]