# Generated by Django 4.0.5 on 2022-08-19 12:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('heroes', '0019_remove_gem_is_off_chain_gem_is_on_chain'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='heroinfo',
            options={'verbose_name_plural': "Hero's info"},
        ),
        migrations.RemoveField(
            model_name='heroinfo',
            name='is_on_chain',
        ),
    ]
