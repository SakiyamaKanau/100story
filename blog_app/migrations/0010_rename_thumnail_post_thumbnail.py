# Generated by Django 3.2.4 on 2021-07-14 08:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog_app', '0009_post_thumnail'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='thumnail',
            new_name='thumbnail',
        ),
    ]
