# Generated by Django 4.2 on 2023-12-30 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("oauth", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="ouser",
            name="nickname",
            field=models.CharField(default="访客", max_length=10),
        ),
    ]
