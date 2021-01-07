# Generated by Django 2.2 on 2020-12-10 23:56

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('student', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExamModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='创建时间')),
                ('mod_time', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('is_delete', models.BooleanField(default=False)),
                ('date', models.DateField(verbose_name='考试时间')),
                ('name', models.CharField(max_length=256, verbose_name='考试名称')),
                ('remark', models.CharField(max_length=512, verbose_name='考试备注')),
                ('file_path', models.FilePathField(allow_folders=True, default='-1', verbose_name='文件路径')),
            ],
            options={
                'verbose_name': '考试信息表',
                'verbose_name_plural': '考试信息表',
                'ordering': ['date'],
            },
        ),
        migrations.CreateModel(
            name='ScoresModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='创建时间')),
                ('mod_time', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('is_delete', models.BooleanField(default=False)),
                ('candidate_number', models.CharField(max_length=64, verbose_name='考号')),
                ('ranking', models.IntegerField(default=-1, verbose_name='名次')),
                ('total_score', models.SmallIntegerField(default=-1, help_text='总分', verbose_name='总分')),
                ('chinese', models.SmallIntegerField(default=-1, help_text='语文', verbose_name='语文')),
                ('math', models.SmallIntegerField(default=-1, help_text='数学', verbose_name='数学')),
                ('english', models.SmallIntegerField(default=-1, help_text='英语', verbose_name='英语')),
                ('physics', models.SmallIntegerField(default=-1, help_text='物理', verbose_name='物理')),
                ('chemistry', models.SmallIntegerField(default=-1, help_text='化学', verbose_name='化学')),
                ('biology', models.SmallIntegerField(default=-1, help_text='生物', verbose_name='生物')),
                ('politics', models.SmallIntegerField(default=-1, help_text='政治', verbose_name='政治')),
                ('history', models.SmallIntegerField(default=-1, help_text='历史', verbose_name='历史')),
                ('geography', models.SmallIntegerField(default=-1, help_text='地理', verbose_name='地理')),
                ('computer', models.SmallIntegerField(default=-1, help_text='计算机', verbose_name='计算机')),
                ('music', models.SmallIntegerField(default=-1, help_text='音乐', verbose_name='音乐')),
                ('art', models.SmallIntegerField(default=-1, help_text='美术', verbose_name='美术')),
                ('pe', models.SmallIntegerField(default=-1, help_text='体育', verbose_name='体育')),
                ('exam', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='exam.ExamModel')),
                ('grade', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='student.GradeClassModel')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='student.StudentModel')),
            ],
            options={
                'verbose_name': '成绩信息表',
                'verbose_name_plural': '成绩信息表',
                'ordering': ['exam'],
            },
        ),
    ]
