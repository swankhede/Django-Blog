# Generated by Django 3.0 on 2019-12-27 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogApp2', '0002_saveform_username'),
    ]

    operations = [
        migrations.CreateModel(
            name='blogpost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256)),
                ('content', models.CharField(max_length=1000)),
                ('author', models.CharField(max_length=256)),
                ('dateTime', models.CharField(max_length=256)),
            ],
        ),
    ]
