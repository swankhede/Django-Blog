# Generated by Django 3.0 on 2020-01-01 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogApp2', '0017_auto_20200101_2036'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='id',
            field=models.AutoField(auto_created=True, default=1, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='title',
            field=models.CharField(max_length=256),
        ),
    ]