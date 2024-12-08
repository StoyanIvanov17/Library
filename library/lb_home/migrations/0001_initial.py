# Generated by Django 5.1.1 on 2024-11-19 14:43

import library.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BestAuthors',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('item_image', models.ImageField(upload_to='author_images/', validators=[library.core.validators.MaxFileSizeValidator(10485760)], verbose_name='Item Image')),
            ],
        ),
    ]
