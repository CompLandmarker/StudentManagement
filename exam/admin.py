from django.contrib import admin

# Register your models here.
from .models import ExamModel, ScoresModel


@admin.register(ExamModel)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('date', 'name', 'remark', 'mod_time', 'create_time')
    list_display_links = ('remark', 'name',)
    ordering = ['date']


def get_student_name(obj):
    return '{}'.format(obj.student.name).upper()


# 'student.in_class',
class ScoreAdmin(admin.ModelAdmin):
    list_display = (
        'ranking', 'student_name', 'grade', 'chinese', 'math', 'english', 'politics',
        'biology', 'history', 'geography', 'score_sum',
    )
    ordering = ['exam','ranking']
    list_filter = ['exam', ]
    search_fields = ('student_name', 'chinese', 'math', 'english')

    def student_name(self, obj):
        return obj.student.name


admin.site.register(ScoresModel, ScoreAdmin)
