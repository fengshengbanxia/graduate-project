from django.shortcuts import render
from django.core import serializers

# Create your views here.

from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Q
from ..models import *
import datetime
import math


# 管理平台主页
def index(request):
    # data = request.session.get("userinfo",None)
    # 1.获取5个最新的数据(教师和学生信息)
    data_len = 5
    data_list = []
    # （1.学生信息
    data_list1 = Student.objects.filter ().order_by ('register_time')[:data_len]
    for item in data_list1:
        data_list.append({
            'number':item.number,
            'name':item.name,
            'register_time':item.register_time,
            'type':'学生',
        })
    # （2.教师信息（如果数量不够，则教师来补）
    if len(data_list) < data_len:
        last_len = data_len - len(data_list)
        data_list2 = Teacher.objects.filter ().order_by ('register_time')[:last_len]
        for item in data_list2:
            data_list.append({
                'number':item.number,
                'name':item.name,
                'register_time':item.register_time,
                'type':'教师',
            })
    # 2.获取展示栏信息
    last_time = datetime.datetime.now() - datetime.timedelta(days=90)
    data1_1 = Student.objects.all ().count ()
    data1_2 = len(Student.objects.filter (register_time__gte=last_time).values())
    data2_1 = Teacher.objects.all ().count ()
    data2_2 = len(Teacher.objects.filter (register_time__gte=last_time).values())
    data3_1 = StudentGraduateArticle.objects.all ().count ()
    data3_2 = math.ceil(StudentGraduateArticle.objects.all ().count ()  / 2)
    show_data = {
        'show_count1':data1_1,
        'show_add1':data1_2,
        'show_count2':data2_1,
        'show_add2':data2_2,
        'show_count3':data3_1,
        'show_add3':data3_2,
    }

    return render(request,'admin/index.html',{'data_list':data_list,'show_data':show_data})
# 教师管理
def teacher_list(request):
    data_list = Teacher.objects.all()
    return render(request,'admin/teacher_list.html',{'data_list':data_list})
def doDeleteTeacher(request):
    data = request.POST.dict()
    print(data)
    Teacher.objects.filter(id = data['id']).delete()
    return JsonResponse({'msg':"删除成功",'code':200})
def doSearchTeacher(request):
    data = request.POST.dict()
    keywords_name = data['keywords_name']
    keywords_value = data['keywords_value']
    searchdata = {f'{keywords_name}__icontains': keywords_value}
    data_list = Teacher.objects.filter(**searchdata)
    return JsonResponse({'msg':"查询成功",'data':serializers.serialize("json",data_list),'code':200})
# 学生管理
def student_list(request):
    data_list = Student.objects.all()
    return render(request,'admin/student_list.html',{'data_list':data_list} )
def doDeleteStudent(request):
    data = request.POST.dict()
    Student.objects.filter(id = data['id']).delete()
    return JsonResponse({'msg':"删除成功",'code':200})
def doSearchStudent(request):
    data = request.POST.dict()
    keywords_name = data['keywords_name']
    keywords_value = data['keywords_value']
    searchdata = {f'{keywords_name}__icontains': keywords_value}
    data_list = Student.objects.filter(**searchdata)
    return JsonResponse({'msg':"查询成功",'data':serializers.serialize("json",data_list),'code':200})
# 课题管理
def title_list(request):
    data_list = StudentGraduateArticle.objects.all()
    return render(request,'admin/title_list.html',{'data_list':enumerate(data_list)})
def doDeleteTitle(request):
    data = request.POST.dict()
    StudentGraduateArticle.objects.filter(id = data['id']).delete()
    return JsonResponse({'msg':"删除成功",'code':200})
def doSearchTitle(request):
    data = request.POST.dict()
    keywords_name = data['keywords_name']
    keywords_value = data['keywords_value']
    searchdata = {f'{keywords_name}__icontains': keywords_value}
    data_list = StudentGraduateArticle.objects.filter(**searchdata)
    return JsonResponse({'msg':"查询成功",'data':serializers.serialize("json",data_list),'code':200})