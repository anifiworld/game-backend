# Generated by Django 4.0.5 on 2022-09-21 07:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stages', '0003_gameplaystage_remove_gameplay_player_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='gameplaystage',
            name='is_cancelled',
            field=models.BooleanField(default=False),
        ),
    ]