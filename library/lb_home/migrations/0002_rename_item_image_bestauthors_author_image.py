# Generated by Django 5.1.1 on 2024-11-19 14:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lb_home', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bestauthors',
            old_name='item_image',
            new_name='author_image',
        ),
    ]
