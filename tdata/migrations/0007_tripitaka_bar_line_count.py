# Generated by Django 2.0.2 on 2018-05-22 03:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tdata', '0006_configuration_task_timeout'),
    ]

    operations = [
        migrations.AddField(
            model_name='tripitaka',
            name='bar_line_count',
            field=models.CharField(default='0', max_length=256, verbose_name='每栏文本行数'),
        ),
    ]
