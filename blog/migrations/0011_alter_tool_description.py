# Generated by Django 4.2 on 2024-02-03 23:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0010_alter_tool_toolset"),
    ]

    operations = [
        migrations.AlterField(
            model_name="tool",
            name="description",
            field=models.TextField(max_length=250, verbose_name="描述"),
        ),
    ]