# Generated by Django 4.1.3 on 2022-11-13 21:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("movies", "0004_alter_personfilmwork_role"),
    ]

    operations = [
        migrations.AddIndex(
            model_name="filmwork",
            index=models.Index(fields=["updated_at"], name="film_work_updated_at_idx"),
        ),
        migrations.AddIndex(
            model_name="genre",
            index=models.Index(fields=["updated_at"], name="genre_updated_at_idx"),
        ),
        migrations.AddIndex(
            model_name="person",
            index=models.Index(fields=["updated_at"], name="person_updated_at_idx"),
        ),
    ]
