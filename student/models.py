from django.db import models


class BaseModel(models.Model):
    create_time = models.DateTimeField(auto_created=True, auto_now_add=True)
    is_delete = models.BooleanField(default=False)

    class Meta:
        abstract = True


class SchoolModel(BaseModel):
    name = models.CharField(max_length=256, verbose_name='学校名称')

    class Meta:
        verbose_name = "学校信息表"
        verbose_name_plural = "学校信息表"

    def __str__(self):
        return self.name


class GradeClassModel(BaseModel):
    student_grade = models.CharField(max_length=128, verbose_name='年级')
    student_class = models.CharField(max_length=128, verbose_name='班级')
    student_cnt = models.SmallIntegerField(verbose_name='班级人数', default=-1)

    class Meta:
        ordering = ['student_grade', 'student_class']
        verbose_name = "班级信息表"
        verbose_name_plural = "班级信息表"

    def __str__(self):
        return '{}{}'.format(self.student_grade, self.student_class)


class StudentModel(BaseModel):
    IN_CLASS_STATUS = (
        ('0', '在班'),
        ('1', '已转班'),
        ('2', '已转学'),
    )

    student_uuid = models.CharField(primary_key=True, max_length=128, help_text='系统级别的唯一身份', verbose_name='系统级别的唯一身份')
    student_name = models.CharField(max_length=64)
    in_class = models.ForeignKey(GradeClassModel, on_delete=models.DO_NOTHING)
    status = models.CharField(max_length=16, choices=IN_CLASS_STATUS, default='0')

    class Meta:
        ordering = ['student_uuid']
        verbose_name = "学生信息表"
        verbose_name_plural = "学生信息表"

    def __str__(self):
        return '{} - {}'.format(self.student_name, self.in_class)
        #     luxiaoxiao - 七年级9班


class StudentDetailsModel(BaseModel):
    GENDER_CHOICES = (
        ('0', '女'),
        ('1', '男'),
    )

    student_uuid = models.OneToOneField(StudentModel, on_delete=models.DO_NOTHING)
    gender = models.CharField(max_length=16, choices=GENDER_CHOICES, default=0)
    address = models.CharField(max_length=256, verbose_name='家庭地址')
    card_num = models.CharField(max_length=24, verbose_name='身份证号码')
    telephone = models.CharField(max_length=18, verbose_name='电话号码')

    class Meta:
        ordering = ['student_uuid']
        verbose_name = "学生详情表"
        verbose_name_plural = "学生详情表"

    def __str__(self):
        return '{}({})'.format(self.student_uuid.student_name, self.student_uuid)
