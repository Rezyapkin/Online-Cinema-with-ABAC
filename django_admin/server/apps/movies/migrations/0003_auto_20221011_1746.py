# Generated by Django 3.2.16 on 2022-10-11 17:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("movies", "0002_auto_20221011_1332"),
    ]

    operations = [
        migrations.RenameField(
            model_name="filmwork",
            old_name="created",
            new_name="created_at",
        ),
        migrations.RenameField(
            model_name="filmwork",
            old_name="modified",
            new_name="updated_at",
        ),
        migrations.RenameField(
            model_name="genre",
            old_name="created",
            new_name="created_at",
        ),
        migrations.RenameField(
            model_name="genre",
            old_name="modified",
            new_name="updated_at",
        ),
        migrations.RenameField(
            model_name="genrefilmwork",
            old_name="created",
            new_name="created_at",
        ),
        migrations.RenameField(
            model_name="person",
            old_name="created",
            new_name="created_at",
        ),
        migrations.RenameField(
            model_name="person",
            old_name="modified",
            new_name="updated_at",
        ),
        migrations.RenameField(
            model_name="personfilmwork",
            old_name="created",
            new_name="created_at",
        ),
    ]