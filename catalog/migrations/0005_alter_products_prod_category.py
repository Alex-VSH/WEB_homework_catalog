# Generated by Django 4.2.6 on 2023-12-03 17:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0004_productversion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='prod_category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.category', verbose_name='категория'),
        ),
    ]
