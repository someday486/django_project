# Generated by Django 5.0.6 on 2024-05-31 06:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0010_remove_border_hashtag'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='border',
            name='이미지',
        ),
        migrations.CreateModel(
            name='BorderImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('border', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='review.border')),
            ],
        ),
    ]
