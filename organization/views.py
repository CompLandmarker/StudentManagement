from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from student.models import StudentModel, GradeClassModel
from exam.models import ScoresModel, ExamModel
import json

# Create your views here.
def list(request):
    data_list = GradeClassModel.objects.order_by()
    # print(data_list)
    # return render(request, "organization/class-list.html", {'data_list': data_list})
    return HttpResponse("ok")

def index(request):
    # return render(request, "index.html")
    return HttpResponse("ok")

def class_details(request, pk):
    # latest_exam = ExamModel.objects.order_by('exam_date').last()
    # get_grade = GradeClassModel.objects.filter(id=pk, ).first()
    # data_list = ScoresModel.objects.filter(
    #     exam=latest_exam, stdent__in_class=get_grade
    # ).oredr_by('-sum_score')
    # for i in data_list:
    #     tmp_sum = get_sum_score(i)
    #     ScoresModel.objects.filter(id=i.id).update(sum_score=tmp_sum)
    # data_list = ScoresModel.objects.filter(exam_id=pk).order_by(
    #     '-sum_score', '-chinese', '-math', '-english')
    # update_sort_index(data_list)
    # data_list = ScoresModel.objects.filter(exam_id=pk).order_by(
    #     '-sum_score', '-chinese', '-math', '-english')
    # print(data_list[0].score_num)
    # return render(request, "organization/class-details.html", {'data_list': data_list})
    return HttpResponse("ok")

def wqs(request):
    score = ExamModel.objects.all().values()
    # print(score)
    # aa = {'score': list(score)}
    aa={}
    print(type(score))
    aa['2']=list(score)
    aa['1']=3323232
    # list(score)
    # print(type(aa))
    # return JsonResponse(json.dumps(aa),safe=False, json_dumps_params={'ensure_ascii': False},)
    return HttpResponse(aa['2'])