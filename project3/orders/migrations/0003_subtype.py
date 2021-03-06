# Generated by Django 2.2.1 on 2019-05-22 02:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_subtopping'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True)),
                ('price_sm', models.DecimalField(decimal_places=2, max_digits=6, null=True)),
                ('price_lg', models.DecimalField(decimal_places=2, max_digits=6, null=True)),
            ],
        ),
    ]
