# Generated by Django 2.2.7 on 2020-04-30 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studentface', '0010_auto_20200427_1151'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='img',
            field=models.ImageField(default='file/S.jpg', upload_to='file/'),
        ),
    ]