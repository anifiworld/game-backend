# Generated by Django 3.2.13 on 2022-06-28 04:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('heroes', '0005_remove_herouser_gem_slot5_expire_datetime'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='herouser',
            name='level',
        ),
    ]
