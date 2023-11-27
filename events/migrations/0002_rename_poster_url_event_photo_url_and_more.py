# Generated by Django 4.2.7 on 2023-11-26 18:25

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='poster_url',
            new_name='photo_url',
        ),
        migrations.RemoveField(
            model_name='event',
            name='release_year',
        ),
        migrations.AddField(
            model_name='event',
            name='creation_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='event',
            name='description',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='event',
            name='event_date',
            field=models.DateField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='location',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='event',
            name='price',
            field=models.DecimalField(decimal_places=2, default=None, max_digits=10),
        ),
        migrations.AlterField(
            model_name='event',
            name='name',
            field=models.CharField(default='', max_length=255),
        ),
    ]
