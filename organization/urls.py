#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""

# @Time    : 2020/11/29 19:14
# @Author  : Shyazhut.ZT
# @File    : urls
# @Project : StudentManagement

"""

# BigBuddy
from django.urls import path, include

from organization import views

app_name = 'class'
urlpatterns = [
    path('list/', views.list, name='class-list'),
    path('test/', views.wqs),
    path('detail/<int:pk>', views.class_details, name='class-details'),
]
