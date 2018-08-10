# Generated by Django 2.0.1 on 2018-08-10 01:22

from django.db import migrations, models
import django.db.models.deletion
import tdata.lib.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tsdata', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CutTask',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.SmallIntegerField(verbose_name='类型')),
                ('status', models.SmallIntegerField(verbose_name='状态')),
                ('priority', models.SmallIntegerField(verbose_name='优先级')),
                ('origin_cut', tdata.lib.fields.JSONField(default=dict, verbose_name='原始切分')),
                ('cut_result', tdata.lib.fields.JSONField(default=dict, verbose_name='切分结果')),
                ('creator', models.CharField(blank=True, max_length=255, verbose_name='创建人')),
                ('created_at', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('executor', models.CharField(blank=True, max_length=255, verbose_name='执行人')),
                ('picked_at', models.DateTimeField(auto_now=True, verbose_name='执行时间')),
                ('finished_at', models.DateTimeField(auto_now=True, verbose_name='完成时间')),
                ('page', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='tsdata.Page', verbose_name='实体藏经页')),
            ],
            options={
                'verbose_name': '切分任务',
                'verbose_name_plural': '切分任务',
            },
        ),
        migrations.CreateModel(
            name='Pagestatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('col_cut_initial', models.SmallIntegerField(verbose_name='切列校对')),
                ('col_cut_confirm', models.SmallIntegerField(verbose_name='切列审定')),
                ('char_cut_initial', models.SmallIntegerField(verbose_name='切字校对')),
                ('char_cut_confirm', models.SmallIntegerField(verbose_name='切字审定')),
                ('remark', models.TextField(blank=True, default='', verbose_name='备注')),
                ('page', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='tsdata.Page', verbose_name='实体藏经页')),
            ],
            options={
                'verbose_name': '切分进度',
                'verbose_name_plural': '切分进度',
            },
        ),
    ]
