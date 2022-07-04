# Generated by Django 4.0.3 on 2022-07-03 00:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0016_rename_connections_connection'),
    ]

    operations = [
        migrations.AddField(
            model_name='connection',
            name='follower_id_post',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='followers', to='network.post'),
        ),
        migrations.AddField(
            model_name='connection',
            name='following_id_post',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='followings', to='network.post'),
        ),
    ]