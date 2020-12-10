#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""

# @Time    : 2020/11/28 3:17
# @Author  : Shyazhut.ZT
# @File    : urls
# @Project : StudentManagement

"""

from django.contrib import admin
from django.urls import path, include

from exam import views

app_name = 'exam'
urlpatterns = [
    path('index/', views.index),
    path('list/', views.exam_list, name='exam-list'),
    path('score/', views.exam_score, name='exam-score'),
    path('detail/<int:pk>', views.exam_details, name='exam-details'),
    path('sum/', views.cnt_score, name='待定'),

    path('ranking/', views.update_ranking),
    # path('excel_data/', admin.site.urls),
]
