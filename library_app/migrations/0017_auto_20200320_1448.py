# Generated by Django 3.0.4 on 2020-03-20 13:48

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('library_app', '0016_auto_20200320_1428'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='User_Loans',
            new_name='User_Loan',
        ),
    ]
