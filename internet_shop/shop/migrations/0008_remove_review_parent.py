# Generated by Django 4.1.1 on 2022-09-21 12:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0007_review_rename_commentphoto_reviewphoto_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='parent',
        ),
    ]
