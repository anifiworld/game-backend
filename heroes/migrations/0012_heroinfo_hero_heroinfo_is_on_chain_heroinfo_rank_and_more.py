# Generated by Django 4.0.5 on 2022-07-26 08:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("heroes", "0011_alter_heroinfo_options"),
    ]

    operations = [
        migrations.AddField(
            model_name="heroinfo",
            name="hero",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="heroes_type",
                to="heroes.hero",
            ),
        ),
        migrations.AddField(
            model_name="heroinfo",
            name="is_on_chain",
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name="heroinfo",
            name="rank",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="heroes_rank",
                to="heroes.herorank",
            ),
        ),
        migrations.AddField(
            model_name="heroinfo",
            name="rarity",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="heroes_rarity",
                to="heroes.herorarity",
            ),
        ),
        migrations.AlterField(
            model_name="heroinfo",
            name="nft_id",
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name="herorank",
            name="value",
            field=models.IntegerField(unique=True),
        ),
    ]
