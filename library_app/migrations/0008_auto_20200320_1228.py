# Generated by Django 3.0.4 on 2020-03-20 11:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('library_app', '0007_book_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='loaned_date',
        ),
        migrations.RemoveField(
            model_name='book',
            name='loaned_out',
        ),
        migrations.CreateModel(
            name='Loan',
            fields=[
                ('book', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='library_app.Book')),
                ('loaned_out', models.BooleanField(default=False)),
                ('loaned_date', models.DateTimeField(auto_now=True)),
                ('loaner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]