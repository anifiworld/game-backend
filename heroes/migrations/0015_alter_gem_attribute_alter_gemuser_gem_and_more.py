# Generated by Django 4.0.5 on 2022-08-17 07:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("heroes", "0014_alter_heroinfo_rank"),
    ]

    operations = [
        migrations.AlterField(
            model_name="gem",
            name="attribute",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="gems",
                to="heroes.gemattribute",
            ),
        ),
        migrations.AlterField(
            model_name="gemuser",
            name="gem",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="users",
                to="heroes.gem",
            ),
        ),
        migrations.AlterField(
            model_name="gemuser",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="gems",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]