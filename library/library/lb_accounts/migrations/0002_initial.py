# Generated by Django 5.1.1 on 2024-10-22 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('lb_accounts', '0001_initial'),
        ('lb_collections', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='libraryprofile',
            name='saved_items',
            field=models.ManyToManyField(blank=True, related_name='library_profile_saved_items', to='lb_collections.item'),
        ),
    ]
