# Generated by Django 2.2.7 on 2020-03-31 07:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studentface', '0002_remove_createclasstime_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendance',
            name='classtime',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]