# Generated by Django 4.1.3 on 2022-12-09 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='is_read',
            field=models.BooleanField(default=False, null=True),
        ),
    ]