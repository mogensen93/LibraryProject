# Generated by Django 3.0.4 on 2020-03-20 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library_app', '0011_auto_20200320_1255'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='loaned_date',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='book',
            name='loaned_out',
            field=models.BooleanField(default=False),
        ),
        migrations.DeleteModel(
            name='Loan',
        ),
    ]
