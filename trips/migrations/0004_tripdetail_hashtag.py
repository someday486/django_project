# Generated by Django 5.0.6 on 2024-05-30 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trips', '0003_tripdetail_context'),
    ]

    operations = [
        migrations.AddField(
            model_name='tripdetail',
            name='hashtag',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]
