# Generated by Django 4.1.3 on 2022-12-09 11:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0009_alter_project_options_review_owner_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='project',
            options={'ordering': ['-vote_ratio', 'vote_total', 'title']},
        ),
    ]
