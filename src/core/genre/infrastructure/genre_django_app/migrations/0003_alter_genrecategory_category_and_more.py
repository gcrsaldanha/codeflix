# Generated by Django 4.2.5 on 2023-11-22 00:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("django_app", "0003_delete_genrecategory"),
        ("genre_django_app", "0002_genrecategory"),
    ]

    operations = [
        migrations.AlterField(
            model_name="genrecategory",
            name="category",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, related_name="related_genres", to="django_app.category"
            ),
        ),
        migrations.AlterField(
            model_name="genrecategory",
            name="genre",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="related_categories",
                to="genre_django_app.genre",
            ),
        ),
    ]
