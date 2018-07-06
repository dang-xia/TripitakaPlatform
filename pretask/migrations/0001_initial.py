# Generated by Django 2.0.2 on 2018-06-28 02:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import tdata.lib.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('rect', '0007_auto_20180606_1609'),
    ]

    operations = [
        migrations.CreateModel(
            name='ColRect',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('cid', models.CharField(db_index=True, max_length=32, verbose_name='经字号')),
                ('char_no', models.PositiveSmallIntegerField(blank=True, default=0, null=True, verbose_name='字号')),
                ('line_no', models.PositiveSmallIntegerField(blank=True, default=0, null=True, verbose_name='行号')),
                ('op', models.PositiveSmallIntegerField(default=1, verbose_name='操作类型')),
                ('x', models.PositiveSmallIntegerField(default=0, verbose_name='X坐标')),
                ('y', models.PositiveSmallIntegerField(default=0, verbose_name='Y坐标')),
                ('w', models.IntegerField(default=1, verbose_name='宽度')),
                ('h', models.IntegerField(default=1, verbose_name='高度')),
                ('cc', models.FloatField(blank=True, default=1, null=True, verbose_name='切分置信度')),
                ('ch', models.CharField(blank=True, default='', max_length=16, null=True, verbose_name='文字')),
                ('wcc', models.FloatField(blank=True, default=1, null=True, verbose_name='识别置信度')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
            ],
            options={
                'verbose_name': '源-切字列区',
                'verbose_name_plural': '源-切字列区管理',
                'ordering': ('-cc',),
            },
        ),
        migrations.CreateModel(
            name='PrePage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bar_info', tdata.lib.fields.JSONField(default=list, verbose_name='切分信息')),
                ('text', models.TextField(blank=True, default='', verbose_name='文本信息')),
                ('image_url', models.CharField(max_length=128, verbose_name='图片地址')),
                ('page_info', models.CharField(blank=True, max_length=128, verbose_name='页面信息')),
            ],
        ),
        migrations.CreateModel(
            name='PrePageColTask',
            fields=[
                ('number', models.CharField(max_length=64, primary_key=True, serialize=False, verbose_name='任务编号')),
                ('ttype', models.PositiveSmallIntegerField(choices=[(2, '置信度'), (1, '顺序校对'), (3, '聚类'), (4, '差缺补漏'), (5, '删框'), (6, '反馈审查')], db_index=True, default=1, verbose_name='切分方式')),
                ('desc', models.TextField(blank=True, null=True, verbose_name='任务格式化描述')),
                ('status', models.PositiveSmallIntegerField(choices=[(0, '未就绪'), (1, '未领取'), (2, '已过期'), (3, '已放弃'), (4, '加急'), (5, '处理中'), (7, '已完成'), (9, '已作废')], db_index=True, default=1, verbose_name='任务状态')),
                ('priority', models.PositiveSmallIntegerField(choices=[(1, '低'), (3, '中'), (5, '高'), (7, '最高')], db_index=True, default=3, verbose_name='任务优先级')),
                ('update_date', models.DateField(null=True, verbose_name='最近处理时间')),
                ('obtain_date', models.DateField(null=True, verbose_name='领取时间')),
                ('current_x', models.IntegerField(default=0, verbose_name='当前块X坐标')),
                ('current_y', models.IntegerField(default=0, verbose_name='当前块Y坐标')),
                ('column_count', models.IntegerField(blank=True, null=True, verbose_name='最大列数')),
                ('rect_set', tdata.lib.fields.JSONField(default=list, verbose_name='切字列块JSON切分数据集')),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='pagecol_tasks', to=settings.AUTH_USER_MODEL)),
                ('page', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='pretask.PrePage')),
                ('schedule', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='pagecol_tasks', to='rect.Schedule', verbose_name='切分计划')),
            ],
            options={
                'verbose_name': '切分预处理校对',
                'verbose_name_plural': '切分预处理校对',
            },
        ),
        migrations.CreateModel(
            name='PrePageColVerifyTask',
            fields=[
                ('number', models.CharField(max_length=64, primary_key=True, serialize=False, verbose_name='任务编号')),
                ('ttype', models.PositiveSmallIntegerField(choices=[(2, '置信度'), (1, '顺序校对'), (3, '聚类'), (4, '差缺补漏'), (5, '删框'), (6, '反馈审查')], db_index=True, default=1, verbose_name='切分方式')),
                ('desc', models.TextField(blank=True, null=True, verbose_name='任务格式化描述')),
                ('status', models.PositiveSmallIntegerField(choices=[(0, '未就绪'), (1, '未领取'), (2, '已过期'), (3, '已放弃'), (4, '加急'), (5, '处理中'), (7, '已完成'), (9, '已作废')], db_index=True, default=1, verbose_name='任务状态')),
                ('priority', models.PositiveSmallIntegerField(choices=[(1, '低'), (3, '中'), (5, '高'), (7, '最高')], db_index=True, default=3, verbose_name='任务优先级')),
                ('update_date', models.DateField(null=True, verbose_name='最近处理时间')),
                ('obtain_date', models.DateField(null=True, verbose_name='领取时间')),
                ('current_x', models.IntegerField(default=0, verbose_name='当前块X坐标')),
                ('current_y', models.IntegerField(default=0, verbose_name='当前块Y坐标')),
                ('column_count', models.IntegerField(blank=True, null=True, verbose_name='最大列数')),
                ('rect_set', tdata.lib.fields.JSONField(default=list, verbose_name='切字列块JSON切分数据集')),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='pagecolverify_tasks', to=settings.AUTH_USER_MODEL)),
                ('page', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='pretask.PrePage')),
                ('schedule', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='pagecolverify_tasks', to='rect.Schedule', verbose_name='切分计划')),
            ],
            options={
                'verbose_name': '切分预处理校对审定',
                'verbose_name_plural': '切分预处理校对审定',
            },
        ),
        migrations.AddField(
            model_name='colrect',
            name='page',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='pretask.PrePage'),
        ),
    ]