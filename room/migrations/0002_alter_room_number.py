# Generated by Django 4.2.6 on 2023-10-25 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('room', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='number',
            field=models.IntegerField(blank=True, verbose_name='Number'),
        ),
    ]