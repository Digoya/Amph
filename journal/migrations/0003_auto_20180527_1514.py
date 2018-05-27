# Generated by Django 2.0.5 on 2018-05-27 12:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0002_user_password'),
    ]

    operations = [
        migrations.CreateModel(
            name='Journal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120)),
                ('short_desc', models.CharField(blank=True, max_length=240, null=True)),
                ('main_text', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag_name', models.CharField(max_length=20)),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='email',
            field=models.EmailField(blank=True, help_text='Enter your Email', max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='short_describe',
            field=models.CharField(blank=True, help_text='Enter short Description', max_length=240, null=True),
        ),
        migrations.AddField(
            model_name='journal',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='journal.User'),
        ),
        migrations.AddField(
            model_name='journal',
            name='tags',
            field=models.ManyToManyField(blank=True, null=True, to='journal.Tags'),
        ),
    ]
