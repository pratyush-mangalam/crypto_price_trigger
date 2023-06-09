# Generated by Django 4.1.8 on 2023-05-02 15:45

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Users",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("email", models.EmailField(max_length=249, unique=True)),
                ("active", models.BooleanField(default=True)),
                ("created_date", models.DateTimeField(auto_now_add=True)),
                ("password", models.CharField(max_length=100)),
            ],
            options={
                "db_table": "users",
            },
        ),
        migrations.DeleteModel(
            name="User",
        ),
    ]
