# Generated by Django 5.0.6 on 2024-05-28 06:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0005_alter_border_작성자'),
        ('trips', '0002_delete_user'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Review',
        ),
        migrations.RemoveField(
            model_name='border',
            name='댓글수',
        ),
        migrations.AddField(
            model_name='border',
            name='trip',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='trips.trip'),
        ),
    ]
