from django.db import models
from django.utils import timezone

from student.models import StudentModel, GradeClassModel


class BaseModel(models.Model):
    create_time = models.DateTimeField(verbose_name="创建时间", default=timezone.now)
    mod_time = models.DateTimeField(verbose_name="修改时间", auto_now=True)
    is_delete = models.BooleanField(default=False)

    class Meta:
        abstract = True


class ExamModel(BaseModel):
    date = models.DateField(verbose_name='考试时间')
    name = models.CharField(max_length=256, verbose_name='考试名称')
    remark = models.CharField(max_length=512, verbose_name='考试备注')
    file_path = models.CharField(verbose_name="文件路径", max_length=256, default='-1')

    class Meta:
        ordering = ['date']
        verbose_name = "考试信息表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{}({})'.format(self.date, self.name)


class ScoresModel(BaseModel):
    candidate_number = models.CharField(max_length=64, verbose_name='考号')
    student = models.ForeignKey(StudentModel, on_delete=models.DO_NOTHING)
    grade = models.ForeignKey(GradeClassModel, on_delete=models.DO_NOTHING)
    exam = models.ForeignKey(ExamModel, on_delete=models.DO_NOTHING)

    ranking = models.IntegerField(verbose_name="名次", default=-1)
    total_score = models.SmallIntegerField(verbose_name="总分", help_text='总分', default=-1)

    chinese = models.SmallIntegerField(verbose_name='语文', help_text='语文', default=-1)
    math = models.SmallIntegerField(verbose_name='数学', help_text='数学', default=-1)
    english = models.SmallIntegerField(verbose_name='英语', help_text='英语', default=-1)

    physics = models.SmallIntegerField(verbose_name='物理', help_text='物理', default=-1)
    chemistry = models.SmallIntegerField(verbose_name='化学', help_text='化学', default=-1)
    biology = models.SmallIntegerField(verbose_name='生物', help_text='生物', default=-1)

    politics = models.SmallIntegerField(verbose_name='政治', help_text='政治', default=-1)
    history = models.SmallIntegerField(verbose_name='历史', help_text='历史', default=-1)
    geography = models.SmallIntegerField(verbose_name='地理', help_text='地理', default=-1)

    computer = models.SmallIntegerField(verbose_name='计算机', help_text='计算机', default=-1)
    music = models.SmallIntegerField(verbose_name='音乐', help_text='音乐', default=-1)
    art = models.SmallIntegerField(verbose_name='美术', help_text='美术', default=-1)
    pe = models.SmallIntegerField(verbose_name='体育', help_text='体育', default=-1)

    class Meta:
        ordering = ['exam']
        verbose_name = "成绩信息表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{}({})'.format(self.exam, self.student)
