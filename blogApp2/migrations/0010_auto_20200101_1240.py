# Generated by Django 3.0 on 2020-01-01 07:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogApp2', '0009_auto_20191229_2050'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blogpost',
            name='id',
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='title',
            field=models.CharField(max_length=256, primary_key=True, serialize=False),
        ),
    ]
