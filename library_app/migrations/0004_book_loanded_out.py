# Generated by Django 3.0.4 on 2020-03-19 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library_app', '0003_remove_book_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='loanded_out',
            field=models.BooleanField(default=False),
        ),
    ]