from django.contrib import admin

# Register your models here.
from .models import SchoolModel, StudentModel, StudentDetailsModel, GradeClassModel


# @admin.register(SchoolModel)
class SchoolAdmin(admin.ModelAdmin):
    pass


@admin.register(GradeClassModel)
class GradeClassAdmin(admin.ModelAdmin):
    list_display = ('student_grade', 'student_class', 'student_cnt', 'create_time',)
    list_filter = ('student_grade',)
    ordering = ('student_grade', 'student_class')


@admin.register(StudentModel)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_uuid','student_name', 'in_class', 'create_time')
    list_display_links = ('student_uuid',)

    ordering = ('in_class', 'student_uuid')


class StudentDetailsAdmin(admin.ModelAdmin):
    list_display = ('student_uuid', 'gender', 'telephone', 'card_num', 'address',)
    list_display_links = ('student_uuid',)


admin.site.register(StudentDetailsModel, StudentDetailsAdmin)
