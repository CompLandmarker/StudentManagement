from django.shortcuts import render
from django.http import HttpResponse

from exam.models import ExamModel, ScoresModel


# Create your views here.
def index(request):
    return HttpResponse("exam-index")


def exam_list(request):
    data_list = ExamModel.objects.order_by('exam_date')
    print(data_list)
    return render(request, 'exam/exam-list.html', {'data_list': data_list})


def exam_score(request):
    data_list = ScoresModel.objects.filter(exam_id=5)
    # text = {}
    # for i, data in enumerate(data_list):
    print(type(data_list[0]))
    vv = sorted(data_list)
    print(vv)
    return HttpResponse(vv)


def get_sum_score(score_instance):
    tmp = 0
    scores_list = []
    scores_list.append(score_instance.chinese)
    scores_list.append(score_instance.math)
    scores_list.append(score_instance.english)
    scores_list.append(score_instance.physics)
    scores_list.append(score_instance.chemistry)
    scores_list.append(score_instance.biology)
    scores_list.append(score_instance.politics)
    scores_list.append(score_instance.history)
    scores_list.append(score_instance.geography)
    scores_list.append(score_instance.computer)
    scores_list.append(score_instance.music)
    scores_list.append(score_instance.art)
    scores_list.append(score_instance.pe)

    for i in scores_list:
        if i <= 0:
            continue
        tmp += i

    return tmp


def cnt_score(request):
    # 计算考试总成绩
    data_list = ScoresModel.objects.all()
    for i in data_list:
        tmp_sum = get_sum_score(i)
        ScoresModel.objects.filter(id=i.id).update(sum_score=tmp_sum)
        print('{}分数已更新'.format(i))

    return HttpResponse("ok")


def update_sort_index(score_objects):
    for num, i in enumerate(score_objects):
        ScoresModel.objects.filter(id=i.id).update(sort_index=num + 1)


def exam_details(request, pk):
    data_list = ScoresModel.objects.all()
    for i in data_list:
        tmp_sum = get_sum_score(i)
        ScoresModel.objects.filter(id=i.id).update(sum_score=tmp_sum)
    data_list = ScoresModel.objects.filter(exam_id=pk).order_by(
        '-sum_score', '-chinese', '-math', '-english')
    update_sort_index(data_list)
    data_list = ScoresModel.objects.filter(exam_id=pk).order_by(
        '-sum_score', '-chinese', '-math', '-english')
    # print(data_list[0].score_num)
    return render(request, "exam/exam-details.html", {'data_list': data_list})
