# Generated by Django 2.0.2 on 2018-06-19 02:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tdata', '0011_auto_20180615_1046'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reel',
            name='bar_line_count',
        ),
    ]