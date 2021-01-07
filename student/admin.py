from django.contrib import admin

# Register your models here.
from .models import SchoolModel, StudentModel, StudentDetailsModel, GradeClassModel


# @admin.register(SchoolModel)
class SchoolAdmin(admin.ModelAdmin):
    pass


@admin.register(GradeClassModel)
class GradeClassAdmin(admin.ModelAdmin):
    list_display = ('get_name', 'cnt_student', 'mod_time',)
    list_filter = ('s_grade',)
    ordering = ('s_grade', 's_class')

    def cnt_student(self, id):
        return StudentModel.objects.filter(in_class=id, is_delete=False, status='0').count()


@admin.register(StudentModel)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'name', 'in_class', 'create_time', 'status', 'is_delete')
    list_display_links = ('status', 'uuid',)
    list_filter = ['in_class', ]

    ordering = ('in_class', 'uuid')


class StudentDetailsAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'gender', 'telephone', 'card_num', 'address',)
    list_display_links = ('uuid',)


admin.site.register(StudentDetailsModel, StudentDetailsAdmin)
