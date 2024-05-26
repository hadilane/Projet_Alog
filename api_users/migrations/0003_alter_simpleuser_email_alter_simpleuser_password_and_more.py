# Generated by Django 5.0.3 on 2024-05-24 22:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api_users", "0002_alter_simpleuser_username"),
    ]

    operations = [
        migrations.AlterField(
            model_name="simpleuser",
            name="email",
            field=models.EmailField(max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name="simpleuser",
            name="password",
            field=models.CharField(max_length=128),
        ),
        migrations.AlterField(
            model_name="simpleuser",
            name="username",
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
