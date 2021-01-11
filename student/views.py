from django.shortcuts import render
from django.http import HttpResponse

import pandas as pd
import os
from student.models import StudentModel, GradeClassModel
from exam.models import ScoresModel, ExamModel


def index(request):
    return HttpResponse("index")


def get_sum_score(scores_list):
    sum_score = 0
    for i in scores_list:
        if i <= 0:
            continue
        sum_score += i

    return sum_score


url = r"D:\QQChatNotes\807015872\FileRecv\20201018第一次月考.xls"


# url = r"D:\QQChatNotes\807015872\FileRecv\20201113期中考试成绩.xls"
# url = r"D:\Documents\Workspaces\Excel\测试数据.xlsx"
# url = r"D:\QQChatNotes\807015872\FileRecv\zhoulian.xlsx"

def excel_sheet(path):
    return 1


DataFrame = excel_sheet(url)


def excel_data(request):
    table = DataFrame
    table = table.dropna(axis=0)

    header = []
    for num, i in enumerate(table.columns):
        print(num, i)
        header.append(i)
    row, column = table.shape

    # 根据实际情况调整
    # return HttpResponse("ok")
    exam_name = url.split("\\")[-1].split('.')[0]
    # map_table = {header[0]: '考号',
    #              header[1]: '姓名',
    #              header[2]: '班级',
    #
    #              header[5]: '语文',
    #              header[6]: '数学',
    #              header[7]: '英语',
    #
    #              # header[]: '物理',
    #              # header[]: '化学',
    #              # header[18]: '生物',
    #              #
    #              # header[12]: '政治',
    #              # header[21]: '历史',
    #              # header[24]: '地理',
    #
    #              # header[2]: '体育',
    #
    #              # header[2]: '其他',
    #              }
    map_table = {header[0]: '考号',
                 header[1]: '姓名',
                 header[2]: '班级',

                 header[6]: '语文',
                 header[15]: '数学',
                 header[9]: '英语',

                 # header[]: '物理',
                 # header[]: '化学',
                 header[18]: '生物',

                 header[12]: '政治',
                 header[21]: '历史',
                 header[24]: '地理',

                 # header[2]: '体育',

                 # header[2]: '其他',
                 }

    table.rename(columns=map_table, inplace=True)

    obj_exam = ExamModel.objects.filter(name=exam_name).first()
    if not obj_exam:
        ExamModel.objects.create(
            name=exam_name,
            date='2020-09-01',
            remark="请校验,并更改考试时间",
            file_path=url
        )
        obj_exam = ExamModel.objects.filter(name=exam_name).first()
        print("已创建考试{}".format(exam_name))

    for i in range(0, row):
        kaohao, grand, name, = table['考号'].iloc[i], table['班级'].iloc[i], table['姓名'].iloc[i]
        chinese, math, english = table['语文'].iloc[i], table['数学'].iloc[i], table['英语'].iloc[i]
        biology, politics, history, geography = -1, -1, -1, -1

        # biology = table['生物'].iloc[i]
        # politics = table['政治'].iloc[i]
        # history = table['历史'].iloc[i]
        # geography = table['地理'].iloc[i]

        get_grand = 7
        get_class = grand

        obj_grand_class = GradeClassModel.objects.filter(s_class=get_class, s_grade=get_grand).first()
        if not obj_grand_class:
            GradeClassModel.objects.create(s_class=get_class, s_grade=get_grand)
            obj_grand_class = GradeClassModel.objects.filter(s_class=get_class, s_grade=get_grand).first()
            print("添加新班级：{}年级{}班".format(get_grand, get_class))

        obj_student = StudentModel.objects.filter(name=name, in_class=obj_grand_class).first()
        if not obj_student:
            tmp = list(StudentModel.objects.filter(in_class=obj_grand_class).values('name'))
            student_name_list = [v.values() for v in tmp]

            if name in student_name_list:
                # 存在重名
                print('同一个班级存在重名现象需要处理：请处理------{}'.format(name))
                return HttpResponse((get_class, name,))
            else:
                # 班级总人数,注意学生在班级的状态
                cnt = len(student_name_list)
                cnt += 1

                # 分配系统唯一id
                uuid = '960{}{}{}'.format(str(get_grand).zfill(2), str(get_class).zfill(2), str(cnt).zfill(3))
                StudentModel.objects.create(uuid=uuid, name=name, in_class=obj_grand_class, )

                # 更新班级人数
                GradeClassModel.objects.filter(s_grade=get_grand, s_class=get_class).update(cnt=cnt)

            # 务必确定班级里没有重名
            obj_student = StudentModel.objects.filter(name=name, in_class=obj_grand_class, status='0').first()
            print("添加新同学")

        obj_score = ScoresModel.objects.filter(candidate_number=kaohao, student=obj_student, exam=obj_exam,
                                               grade=obj_grand_class).first()
        if not obj_score:
            scores_list = []
            scores_list.append(chinese)
            scores_list.append(math)
            scores_list.append(english)
            # scores_list.append(physics)
            # scores_list.append(chemistry)
            scores_list.append(biology)
            scores_list.append(politics)
            scores_list.append(history)
            scores_list.append(geography)
            # scores_list.append(computer)
            # scores_list.append(music)
            # scores_list.append(art)
            # scores_list.append(pe)
            cnt_score = get_sum_score(scores_list)

            ScoresModel.objects.create(
                student=obj_student, exam=obj_exam, grade=obj_grand_class,
                chinese=chinese, math=math, english=english,
                biology=biology,
                politics=politics,
                candidate_number=kaohao,
                history=history,
                geography=geography,
                total_score=cnt_score
            )
            print("添加成绩")
        else:
            print("成绩已存在")

    # 名次排序
    get_exam = ExamModel.objects.filter(name=exam_name).first()
    get_ranking = ScoresModel.objects.filter(exam=get_exam).order_by('total_score', 'chinese', 'math', 'english')
    len_get_ranking = len(get_ranking)
    for num, j in enumerate(get_ranking):
        ScoresModel.objects.filter(exam=get_exam, student=j.student).update(ranking=len_get_ranking - num)
    print("名次排序完成")

    return HttpResponse("ok")


def student_list(request):
    return HttpResponse("学生列表")


def details(request, pk):
    import json
    exam_list = ExamModel.objects.order_by('date')

    exam_infos = []
    ranking_infos = []
    for exam in exam_list:
        exam_infos.append(exam.name)
        data = ScoresModel.objects.filter(exam=exam, student_id=pk).first()
        ranking_infos.append(data.ranking)

    return render(request, 'student/student-details.html', {'exam_infos': exam_infos, 'ranking_infos': ranking_infos, })
