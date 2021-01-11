#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""

# @Time    : 2020/11/28 3:19
# @Author  : Shyazhut.ZT
# @File    : urls
# @Project : StudentManagement

"""
from django.contrib import admin
from django.urls import path, include

from student import views

app_name = 'student'
urlpatterns = [
    path('', views.index),
    path('index/', views.index, name='index'),

    path('add_data/', views.excel_data, name='add-data'),
    path('list/', views.student_list, name='student-list'),

    path('details/<int:pk>', views.details, name='student-details'),
    # path()

]
