# Generated by Django 4.1.5 on 2023-01-02 19:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("stats", "0002_alter_run_time"),
    ]

    operations = [
        migrations.AlterField(
            model_name="aesteticscores",
            name="first_rank",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="first_rank",
                to="stats.team",
            ),
        ),
        migrations.AlterField(
            model_name="aesteticscores",
            name="second_rank",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="second_rank",
                to="stats.team",
            ),
        ),
        migrations.AlterField(
            model_name="aesteticscores",
            name="third_rank",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="third_rank",
                to="stats.team",
            ),
        ),
    ]
