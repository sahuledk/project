# Generated by Django 4.1.3 on 2022-12-07 03:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_profile_location_skills'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='username',
            field=models.CharField(blank=True, max_length=200, null=True, unique=True),
        ),
    ]
