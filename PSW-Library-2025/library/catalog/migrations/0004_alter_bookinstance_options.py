# Generated by Django 5.2 on 2025-05-08 09:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0003_genre_language_bookinstance_book_genre_book_language"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="bookinstance",
            options={
                "ordering": ["due_back", "book"],
                "permissions": (("can_mark_returned", "Set book as returned"),),
            },
        ),
    ]
