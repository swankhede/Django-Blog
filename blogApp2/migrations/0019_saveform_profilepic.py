# Generated by Django 3.0 on 2020-01-02 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogApp2', '0018_auto_20200101_2038'),
    ]

    operations = [
        migrations.AddField(
            model_name='saveform',
            name='ProfilePic',
            field=models.ImageField(blank=True, upload_to='media'),
        ),
    ]