# Generated by Django 3.2.4 on 2021-07-15 10:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog_app', '0010_rename_thumnail_post_thumbnail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='content',
            field=models.TextField(max_length=1000, verbose_name='内容'),
        ),
    ]
