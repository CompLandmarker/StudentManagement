from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from student.models import StudentModel, GradeClassModel
from exam.models import ScoresModel, ExamModel
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
    obj_grade = GradeClassModel.objects.get(pk=pk)
    data_list = StudentModel.objects.filter(in_class=obj_grade, status='0').order_by('name')
    return render(request, "organization/class-details.html", {'data_list': data_list})


def wqs(request):
    score = ExamModel.objects.all()[:5]
    student = StudentModel.objects.all()[:5]
    data = sorted(chain(score, student), key=attrgetter("mod_time"))

    return HttpResponse(data)
