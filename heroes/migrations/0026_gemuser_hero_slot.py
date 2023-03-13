# Generated by Django 4.0.5 on 2022-09-13 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('heroes', '0025_remove_gemuser_gem_slot_remove_gemuser_hero_nft_id_and_more'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='gemuser',
            constraint=models.UniqueConstraint(fields=('hero', 'slot'), name='hero_slot'),
        ),
    ]
