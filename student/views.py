from django.shortcuts import render
from django.http import HttpResponse

import pandas as pd
import os
from student.models import StudentModel, GradeClassModel
from exam.models import ScoresModel, ExamModel


def index(request):
    return HttpResponse("index")


def excel_sheet(file_path):
    """
    读取excel文件的所有工作簿
    :param file_path: excel路径
    :return: 返回pandas的数据帧
    """
    f = pd.ExcelFile(url)

    data = pd.DataFrame()
    for i in f.sheet_names:
        d = pd.read_excel(url, sheet_name=i)
        data = pd.concat([data, d])

    return data


url = r"D:\QQChatNotes\807015872\FileRecv\20201018第一次月考.xls"
# url = r"D:\QQChatNotes\807015872\FileRecv\20201113期中考试成绩.xls"
# url = r"D:\Documents\Workspaces\Excel\测试数据.xlsx"
# url = r"D:\QQChatNotes\807015872\FileRecv\zhoulian.xlsx"
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

    exam_name = url.split("\\")[-1].split('.')[0]
    map_table = {header[0]: '考号',
                 header[1]: '姓名',
                 header[2]: '班级',

                 header[5]: '语文',
                 header[6]: '数学',
                 header[7]: '英语',

                 # header[]: '物理',
                 # header[]: '化学',
                 # header[18]: '生物',

                 # header[12]: '政治',
                 # header[21]: '历史',
                 # header[24]: '地理',

                 # header[2]: '体育',

                 # header[2]: '其他',
                 }

    table.rename(columns=map_table, inplace=True)
    response = []

    obj_exam = ExamModel.objects.filter(exam_name=exam_name)
    if not obj_exam:
        ExamModel.objects.create(
            exam_name=exam_name,
            exam_date='2020-09-01',
            remark="请校验",
        )

    for i in range(0, row):
        score_num, grand, name, = table['考号'].iloc[i], table['班级'].iloc[i], table['姓名'].iloc[i]
        msg = '{}:{}-{}'.format(i, score_num, name)

        chinese, math, english = table['语文'].iloc[i], table['数学'].iloc[i], table['英语'].iloc[i]
        # biology = table['生物'].iloc[i]
        # politics = table['政治'].iloc[i]
        # history = table['历史'].iloc[i]
        # geography = table['地理'].iloc[i]

        get_grand = '{}班'.format(grand)
        obj_score = ScoresModel.objects.filter(score_num=score_num, student__student_name=name,
                                               exam__exam_name=exam_name)

        response.append((name, get_grand, obj_score))
        # 当前成绩不在数据库
        if not obj_score:
            obj_student = StudentModel.objects.filter(student_name=name, in_class__student_class=get_grand).first()
            obj_exam = ExamModel.objects.filter(exam_name=exam_name).first()
            msg = msg + "添加成绩"
            # 为新同学分配进班信息
            if not obj_student:
                tmp = list(StudentModel.objects.filter(in_class__student_class=get_grand).values('student_name'))
                student_name_list = [v.values() for v in tmp]

                if name in student_name_list:
                    # 存在重名
                    msg = msg + '存在重名现象需要处理：待处理------'
                    return HttpResponse((msg, get_grand, name,))
                else:
                    # 班级总人数,注意学生在班级的状态
                    cnt = StudentModel.objects.filter(in_class__student_class=get_grand, status='0').count()
                    cnt += 1

                    # 分配系统唯一id
                    uuid = '96{}{}'.format(str(grand).zfill(3), str(cnt).zfill(3))

                    msg = msg + '新同学分配系统级id: {}'.format(uuid)

                    obj = GradeClassModel.objects.filter(student_grade='七年级', student_class=get_grand).first()
                    # 添加同学
                    StudentModel.objects.create(student_uuid=uuid, student_name=name, in_class=obj, )
                    # 更新班级人数
                    GradeClassModel.objects.filter(student_grade="七年级", student_class=get_grand).update(
                        student_cnt=cnt)

                    obj_student = StudentModel.objects.filter(student_name=name, in_class__student_class=get_grand,
                                                              status='0').first()

            ScoresModel.objects.create(
                student=obj_student, exam=obj_exam,
                chinese=chinese, math=math, english=english,
                # biology=biology,
                # politics=politics,
                # score_num=score_num,
                # history=history,
                # geography=geography,
            )

        print(msg)

    return HttpResponse((response, row))


def excel_data2(request):
    url = r"D:\Documents\zhoulian.xlsx"
    table = pd.read_excel(url, header=None, sep="")
    table = table.dropna(axis=0)
    map_table = {23: '学号',
                 0: '姓名',
                 1: '班级',
                 4: '语文',
                 5: '数学',
                 6: '英语',
                 20: '其他'}
    table.rename(columns=map_table, inplace=True)

    row, column = table.shape

    num = 1
    last_grand = ''
    for i in range(1, row):
        name = table['姓名'].iloc[i]
        if name == 'nan':
            continue
        grand = table['班级'].iloc[i]
        chinese = table['语文'].iloc[i]
        math = table['数学'].iloc[i]
        english = table['英语'].iloc[i]
        if last_grand == grand:
            num += 1
        else:
            num = 1

        get_grand = '{}班'.format(grand)
        uuid = '96{}{}'.format(str(grand).zfill(3), str(num).zfill(3))
        print(uuid, name, get_grand)
        last_grand = grand

        obj = GradeClassModel.objects.filter(student_grade__exact='七年级', student_class__exact=get_grand).first()
        StudentModel.objects.create(student_uuid=uuid, student_id='no', student_name=name, in_class=obj, )

        obj_score = ScoresModel.objects.filter(student__student_name=name, exam__exam_name='七年级第一次周练').first()
        if not obj_score:
            obj_student = StudentModel.objects.filter(student_name=name).first()
            obj_exam = ExamModel.objects.filter(exam_name='七年级第一次周练').first()
            ScoresModel.objects.create(
                student=obj_student, exam=obj_exam, chinese=chinese, math=math, english=english,
            )
        print("新建完成")

    return HttpResponse('OOk')


def student_list(request):
    return HttpResponse("学生列表")


def details(request, pk):
    return HttpResponse("详情表{}".format(pk))
