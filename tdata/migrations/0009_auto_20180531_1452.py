# Generated by Django 2.0.2 on 2018-05-31 06:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tdata', '0008_reel_used_in_collation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tripitaka',
            name='bar_line_count',
            field=models.CharField(default=0, max_length=256, verbose_name='每栏文本行数'),
        ),
    ]
