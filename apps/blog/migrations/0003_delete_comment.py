# Generated by Django 4.2.21 on 2025-06-08 16:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0002_alter_article_options_alter_article_author_and_more"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Comment",
        ),
    ]
