# Generated by Django 2.2.1 on 2019-06-09 18:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0011_auto_20190609_1850'),
    ]

    operations = [
        migrations.CreateModel(
            name='Platter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=6)),
                ('size', models.CharField(choices=[('sm', 'small'), ('lg', 'large')], default='sm', max_length=2)),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.PastaType')),
            ],
        ),
    ]