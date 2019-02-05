# Generated by Django 2.1.3 on 2018-11-21 02:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20181121_1236'),
    ]

    operations = [
        migrations.AlterField(
            model_name='object',
            name='date_n',
            field=models.DateField(blank=True),
        ),
        migrations.AlterField(
            model_name='object',
            name='dolgota',
            field=models.DecimalField(blank=True, decimal_places=10, default=0, max_digits=13),
        ),
        migrations.AlterField(
            model_name='object',
            name='mainimage',
            field=models.ImageField(blank=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='object',
            name='opisanie',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='object',
            name='shirota',
            field=models.DecimalField(blank=True, decimal_places=10, default=0, max_digits=13),
        ),
    ]
