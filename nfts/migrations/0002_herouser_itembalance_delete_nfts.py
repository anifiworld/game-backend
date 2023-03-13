# Generated by Django 4.0.5 on 2022-07-20 05:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nfts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='HeroUser',
            fields=[
                ('nft_id', models.CharField(db_column='id', max_length=255, primary_key=True, serialize=False)),
                ('base_str', models.IntegerField(db_column='str')),
                ('base_int', models.IntegerField(db_column='int')),
                ('base_vit', models.IntegerField(db_column='vit')),
                ('base_agi', models.IntegerField(db_column='agi')),
                ('rank', models.IntegerField()),
                ('owner', models.CharField(blank=True, max_length=255, null=True)),
                ('is_deleted', models.BooleanField(db_column='isDeleted')),
                ('created_at', models.DateTimeField(db_column='createdAt')),
                ('updated_at', models.DateTimeField(db_column='updatedAt')),
            ],
            options={
                'db_table': 'indexer_hero_stats',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ItemBalance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=255)),
                ('resource', models.CharField(max_length=255)),
                ('balance', models.CharField(max_length=255)),
                ('expiration_date', models.IntegerField(blank=True, db_column='expirationDate', null=True)),
                ('created_at', models.DateTimeField(db_column='createdAt')),
                ('updated_at', models.DateTimeField(db_column='updatedAt')),
            ],
            options={
                'db_table': 'indexer_item_balances',
                'managed': False,
            },
        ),
        migrations.DeleteModel(
            name='Nfts',
        ),
    ]