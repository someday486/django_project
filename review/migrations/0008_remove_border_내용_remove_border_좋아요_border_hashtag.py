# Generated by Django 5.0.6 on 2024-05-30 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0007_remove_border_trip_remove_border_작성자_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='border',
            name='내용',
        ),
        migrations.RemoveField(
            model_name='border',
            name='좋아요',
        ),
        migrations.AddField(
            model_name='border',
            name='hashtag',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]
