# Generated by Django 4.1.5 on 2023-01-04 14:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("stats", "0004_run_nb_run"),
    ]

    operations = [
        migrations.RenameField(
            model_name="run",
            old_name="nb_run",
            new_name="num_run",
        ),
        migrations.AlterField(
            model_name="run",
            name="score",
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="run",
            name="time",
            field=models.FloatField(default=999),
        ),
    ]
