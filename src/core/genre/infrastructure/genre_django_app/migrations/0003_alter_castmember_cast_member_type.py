# Generated by Django 4.2.5 on 2023-10-16 21:39

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("cast_member_app", "0002_alter_castmember_cast_member_type"),
    ]

    operations = [
        migrations.AlterField(
            model_name="castmember",
            name="cast_member_type",
            field=models.CharField(choices=[("actor", "Actor"), ("director", "Director")], max_length=255),
        ),
    ]
