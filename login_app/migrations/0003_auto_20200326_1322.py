# Generated by Django 3.0.4 on 2020-03-26 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login_app', '0002_user_access_level'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_access_level',
            name='access_level',
            field=models.CharField(choices=[('C', 'Customer'), ('S', 'Staff')], max_length=1),
        ),
    ]
