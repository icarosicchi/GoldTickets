# Generated by Django 4.2.7 on 2023-12-02 16:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0008_alter_event_author'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='author',
        ),
        migrations.AddField(
            model_name='event',
            name='author_id',
            field=models.IntegerField(default=1),
        ),
    ]
