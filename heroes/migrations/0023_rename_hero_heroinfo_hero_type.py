# Generated by Django 4.0.5 on 2022-08-24 12:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('heroes', '0022_heroinfo_gem_slot_alter_gem_attribute_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='heroinfo',
            old_name='hero',
            new_name='hero_type',
        ),
    ]
