# Generated by Django 3.0.4 on 2020-03-21 16:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('library_app', '0018_auto_20200320_1630'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_loan',
            name='magazine_count',
            field=models.IntegerField(default=0),
        ),
        migrations.CreateModel(
            name='Magazine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=500)),
                ('publish_date', models.DateTimeField()),
                ('added_to_library', models.DateTimeField(auto_now_add=True)),
                ('loaner', models.CharField(default='none', max_length=100)),
                ('loaned_out', models.BooleanField(default=False)),
                ('loaned_date', models.DateTimeField(auto_now=True)),
                ('return_date', models.DateTimeField(null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
