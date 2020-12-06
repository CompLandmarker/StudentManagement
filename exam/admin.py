from django.contrib import admin

# Register your models here.
from .models import ExamModel, ScoresModel


@admin.register(ExamModel)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('exam_date', 'exam_name', 'create_time', 'remark')
    list_display_links = ('remark', 'exam_name',)
    ordering = ['-exam_date']


def get_student_name(obj):
    return '{}'.format(obj.student.name).upper()


# 'student.in_class',
class ScoreAdmin(admin.ModelAdmin):
    list_display = (
        'admin_num', 'exam', 'score_num', 'student_name', 'get_class', 'chinese', 'math', 'english', 'politics',
        'biology',
        'history', 'geography', 'sum_score', 'create_time',
    )
    ordering = ['-exam', '-sum_score', ]
    list_filter = ('exam',)
    search_fields = ('student_name', 'chinese', 'math', 'english')

    def student_name(self, obj):
        return obj.student.student_name

    def get_class(self, obj):
        return obj.student.in_class

    def admin_num(self, obj):
        # i = obj.index()
        return 1


admin.site.register(ScoresModel, ScoreAdmin)
