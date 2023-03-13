# Generated by Django 3.2.13 on 2022-06-15 18:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Gem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('nft_id', models.CharField(default='', max_length=255)),
                ('attribute_value', models.DecimalField(decimal_places=2, default=1, max_digits=8)),
                ('attribute_is_percentage', models.BooleanField(default=False)),
                ('level_needed', models.IntegerField(default=1)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='GemAttribute',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': "Gem's attributes",
            },
        ),
        migrations.CreateModel(
            name='Hero',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('image_url', models.URLField(blank=True, null=True)),
                ('hp_multiplier', models.DecimalField(decimal_places=2, default=1, max_digits=5)),
                ('atk_multiplier', models.DecimalField(decimal_places=2, default=1, max_digits=5)),
                ('matk_multiplier', models.DecimalField(decimal_places=2, default=1, max_digits=5)),
                ('def_multiplier', models.DecimalField(decimal_places=2, default=1, max_digits=5)),
                ('aspd_multiplier', models.DecimalField(decimal_places=2, default=1, max_digits=5)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'Heroes',
            },
        ),
        migrations.CreateModel(
            name='HeroClass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': "Hero's classes",
            },
        ),
        migrations.CreateModel(
            name='HeroRank',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.IntegerField()),
                ('multiplier', models.DecimalField(decimal_places=2, default=1, max_digits=5)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': "Hero's ranks",
            },
        ),
        migrations.CreateModel(
            name='HeroRarity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('multiplier', models.DecimalField(decimal_places=2, default=1, max_digits=5)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': "Hero's rarities",
            },
        ),
        migrations.CreateModel(
            name='HeroUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nft_id', models.CharField(default='', max_length=255)),
                ('team_slot', models.IntegerField(default=0)),
                ('gem_slot5_expire_datetime', models.DateTimeField(default=django.utils.timezone.now)),
                ('level', models.IntegerField(default=1)),
                ('exp', models.IntegerField(default=0)),
                ('strength', models.IntegerField(default=1)),
                ('agility', models.IntegerField(default=1)),
                ('vitality', models.IntegerField(default=1)),
                ('intelligent', models.IntegerField(default=1)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('hero', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users', to='heroes.hero')),
                ('rank', models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='heroes_this_rank', to='heroes.herorank')),
                ('rarity', models.ForeignKey(blank=True, db_constraint=False, default=1, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='heroes_this_rarity', to='heroes.herorarity')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='heroes', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Individual heroes',
            },
        ),
        migrations.AddField(
            model_name='hero',
            name='hero_class',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='heroes', to='heroes.heroclass'),
        ),
        migrations.CreateModel(
            name='GemUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gem_slot', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('gem', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='users', to='heroes.gem')),
                ('hero', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='gem_users', to='heroes.herouser')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='gems', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Individual gems',
            },
        ),
        migrations.AddField(
            model_name='gem',
            name='attribute',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='gems', to='heroes.gemattribute'),
        ),
    ]