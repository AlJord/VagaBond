# Generated by Django 4.0.4 on 2022-04-29 00:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_alter_image_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='latitude',
            field=models.FloatField(blank=True, null=True, verbose_name='latitude'),
        ),
        migrations.AlterField(
            model_name='log',
            name='longitude',
            field=models.FloatField(blank=True, null=True, verbose_name='longitude'),
        ),
    ]