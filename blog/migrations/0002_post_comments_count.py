# Generated by Django 4.2.6 on 2023-11-02 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='comments_count',
            field=models.IntegerField(default=0),
        ),
    ]
