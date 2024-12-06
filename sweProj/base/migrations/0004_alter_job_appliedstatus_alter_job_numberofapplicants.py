# Generated by Django 5.1.2 on 2024-11-29 04:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0003_job_location_alter_job_company"),
    ]

    operations = [
        migrations.AlterField(
            model_name="job",
            name="appliedStatus",
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AlterField(
            model_name="job",
            name="numberOfApplicants",
            field=models.IntegerField(default=0),
        ),
    ]