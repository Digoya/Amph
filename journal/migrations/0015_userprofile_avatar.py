# Generated by Django 2.0.5 on 2018-06-01 15:14

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('journal', '0014_auto_20180601_1700'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='avatar',
            field=models.ImageField(default='D:\\Amphstatic/journal/images/default.png', upload_to=''),
        ),
    ]
