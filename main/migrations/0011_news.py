# Generated by Django 2.1.3 on 2019-01-29 02:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_auto_20181210_0114'),
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('foto', models.ImageField(blank=True, null=True, upload_to='')),
                ('txt', models.TextField()),
                ('date', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'Новости',
            },
        ),
    ]
