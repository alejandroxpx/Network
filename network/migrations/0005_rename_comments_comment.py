# Generated by Django 4.0.3 on 2022-05-13 03:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0004_rename_newpost_post'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Comments',
            new_name='Comment',
        ),
    ]