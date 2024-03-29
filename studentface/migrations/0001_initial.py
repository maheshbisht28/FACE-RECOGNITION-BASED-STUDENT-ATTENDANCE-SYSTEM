# Generated by Django 2.2.7 on 2020-03-26 07:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('roll_no', models.IntegerField(default='000')),
                ('first_name', models.CharField(max_length=10)),
                ('last_name', models.CharField(max_length=10)),
                ('year', models.CharField(choices=[('1', 1), ('2', 2), ('3', 3), ('4', 4), ('5', 5), ('NA', 'NA')], default='NA', max_length=2)),
                ('email', models.EmailField(max_length=20, unique=True, verbose_name='email')),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='date joined')),
                ('last_login', models.DateTimeField(auto_now=True, verbose_name='last login')),
                ('face_encoding', models.FileField(blank=True, default='not applicable', null=True, upload_to='file/')),
                ('is_admin', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_student', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=10, unique=True)),
                ('name', models.CharField(max_length=10, unique=True)),
                ('total_years', models.CharField(choices=[('1', 1), ('2', 2), ('3', 3), ('4', 4), ('5', 5), ('NA', 'NA')], max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='subject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10)),
                ('s_code', models.CharField(max_length=10)),
                ('year', models.CharField(choices=[('1', 1), ('2', 2), ('3', 3), ('4', 4), ('5', 5), ('NA', 'NA')], max_length=2)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='studentface.course')),
            ],
        ),
        migrations.CreateModel(
            name='createclasstime',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(verbose_name='date')),
                ('time', models.DateTimeField(verbose_name='time')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='studentface.course')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='studentface.subject')),
            ],
        ),
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=False)),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='studentface.subject')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
