# Generated by Django 5.1.2 on 2024-10-30 14:53

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0002_watchlist_addedon"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="watchlist",
            name="itemName",
        ),
        migrations.RemoveField(
            model_name="watchlist",
            name="itemPoster",
        ),
        migrations.RemoveField(
            model_name="watchlist",
            name="itemRating",
        ),
        migrations.RemoveField(
            model_name="watchlist",
            name="itemType",
        ),
    ]
