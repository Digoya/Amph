# Generated by Django 2.0.5 on 2018-06-05 15:44

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('journal', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Journal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('journal_name', models.CharField(default='No Name', max_length=100)),
                ('avatar', models.ImageField(blank=True, upload_to='avatars')),
                ('author',
                 models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='journal.UserProfile')),
                ('tags', models.ManyToManyField(blank=True, to='journal.Tag')),
            ],
        ),
        migrations.AlterField(
            model_name='emailverification',
            name='expiration_date',
            field=models.DateTimeField(default=datetime.datetime(2018, 6, 7, 18, 44, 43, 846942)),
        ),
        migrations.AddField(
            model_name='article',
            name='journal',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='journal.Journal'),
        ),
    ]
