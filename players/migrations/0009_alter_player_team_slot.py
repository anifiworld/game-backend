# Generated by Django 4.0.5 on 2022-08-15 12:14

from django.db import migrations, models
import players.models


class Migration(migrations.Migration):

    dependencies = [
        ("players", "0008_player_team_slot"),
    ]

    operations = [
        migrations.AlterField(
            model_name="player",
            name="team_slot",
            field=models.JSONField(default=players.models.default_team_slot_dict),
        ),
    ]
