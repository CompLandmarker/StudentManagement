from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from student.models import StudentModel, GradeClassModel
from exam.models import ScoresModel, ExamModel
from django.forms.models import model_to_dict
import json

from itertools import chain
from operator import attrgetter


# Create your views here.
def list(request):
    data_list = GradeClassModel.objects.order_by()
    return render(request, "organization/class-list.html", {'data_list': data_list})


def index(request):
    return render(request, "index.html")


def class_details(request, pk):
    obj_grade = GradeClassModel.objects.get(id=pk)
    student_list = StudentModel.objects.filter(in_class=obj_grade, status='0').order_by('name')

    exam_object = ExamModel.objects.order_by('date')

    data_list = []

    for i in student_list:
        tmp = {}
        tmp['name'] = i.name
        # print(tmp)
        last_ranking = 0
        score = []
        for num, exam in enumerate(exam_object):
            try:
                student_info = ScoresModel.objects.filter(student=i, exam=exam).first()
                ranking = student_info.ranking
                total_score = student_info.total_score
            except AttributeError:
                print("{}同学最近考试成绩不存在".format(i.name))
                ranking = 0
                total_score = 0
            if num == 0:
                score.append((ranking, 0, total_score))
            else:
                score.append((ranking, -(ranking - last_ranking), total_score))
            last_ranking = ranking
        tmp['score'] = score
        data_list.append(tmp)
        print(tmp)

    # [{name:xxx,score:[(名次,进退步,分数),((名次,进退步,分数),...)]}, ..]
    # print(data_list)
    return render(request, "organization/class-details.html",
                  {'data_list': data_list, 'name': obj_grade, 'exam_list': exam_object})


def wqs(request):
    score = ExamModel.objects.all()[:5]
    student = StudentModel.objects.all()[:5]
    data = sorted(chain(score, student), key=attrgetter("mod_time"))

    return HttpResponse(data)
