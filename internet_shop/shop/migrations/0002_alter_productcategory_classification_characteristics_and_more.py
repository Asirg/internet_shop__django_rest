# Generated by Django 4.1.1 on 2022-09-20 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productcategory',
            name='classification_characteristics',
            field=models.ManyToManyField(blank=True, to='shop.characteristic'),
        ),
        migrations.AlterField(
            model_name='productcategory',
            name='groups_characteristics',
            field=models.ManyToManyField(blank=True, to='shop.groupcharacteristics'),
        ),
    ]