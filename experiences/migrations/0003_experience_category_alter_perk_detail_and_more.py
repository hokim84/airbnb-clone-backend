# Generated by Django 4.1.4 on 2023-01-02 10:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("categories", "0001_initial"),
        ("experiences", "0002_remove_perk_a_experience_end_alter_experience_start"),
    ]

    operations = [
        migrations.AddField(
            model_name="experience",
            name="category",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="categories.category",
            ),
        ),
        migrations.AlterField(
            model_name="perk",
            name="detail",
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name="perk",
            name="name",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
