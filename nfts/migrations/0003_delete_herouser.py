# Generated by Django 4.0.5 on 2022-09-19 15:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nfts', '0002_herouser_itembalance_delete_nfts'),
    ]

    operations = [
        migrations.DeleteModel(
            name='HeroUser',
        ),
    ]
