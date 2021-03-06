# Generated by Django 3.1.4 on 2022-05-01 09:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookLists',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('books_complete', models.ManyToManyField(related_name='books_complete', to='books.Book')),
                ('books_dropped', models.ManyToManyField(related_name='books_dropped', to='books.Book')),
                ('books_progress', models.ManyToManyField(related_name='books_on_progress', to='books.Book')),
                ('books_waiting', models.ManyToManyField(related_name='books_waiting_list', to='books.Book')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
