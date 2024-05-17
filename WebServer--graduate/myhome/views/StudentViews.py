from django.shortcuts import render
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt

from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Q
from ..models import *
from ..utils.func import upload  # 引入自定义上传模块
import math
import datetime


# 个人信息
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
    return render(request,'student/index.html',{'data_list':data_list,'show_data':show_data})
# 选择信息
# (1.选题信息
def select_title(request):
    id = request.session["userinfo"].get("id",None)
    name = request.session["userinfo"].get("name",None)

    # 先检查是否有当前教师的开题设计记录，
    data_obj1 = StudentSelectTitle.objects.filter(student_id=id).first()
    data_obj2 = StudentGraduateArticle.objects.filter(student_id=id).first()
    data_obj3 = StudentTitleMsg.objects.filter(student_id=id).first()

    data = {
        'task_docx':data_obj1.task_docx if data_obj1 else None,
        'guide_docx':data_obj1.guide_docx if data_obj1 else None,

        'article_docx':data_obj2.article_docx if data_obj2 else None,

        'title_docx':data_obj3.title_docx if data_obj3 else None,
        'english_docx':data_obj3.english_docx if data_obj3 else None,
        'apply_docx':data_obj3.apply_docx if data_obj3 else None,

        'id':data_obj3.id if data_obj3 else None,
        'name':data_obj3.name if data_obj3 else None,
        'brief':data_obj3.brief if data_obj3 else None,
        'student_id':data_obj3.student_id if data_obj3 else None,
        'student_name':data_obj3.student_name if data_obj3 else None,
        'teacher_id':data_obj3.teacher_id if data_obj3 else None,
        'teacher_name':data_obj3.teacher_name if data_obj3 else None,
    }


    return render(request,'student/select_title.html',{'data':data})
@csrf_exempt # 允许跨站上传
def doUploadTitle(request):
    id = request.session["userinfo"].get("id",None)

    file = request.FILES.get("file")
    fileDir = upload(file)
    print('1上传的结果',fileDir)
    StudentTitleMsg.objects.filter(student_id=id).update(title_docx=fileDir)
    return JsonResponse({'msg':"上传成功",'data':fileDir,'code':200})
@csrf_exempt # 允许跨站上传
def doUploadEnglish(request):
    id = request.session["userinfo"].get("id",None)

    file = request.FILES.get("file")
    fileDir = upload(file)
    print('2上传的结果',fileDir)
    StudentTitleMsg.objects.filter(student_id=id).update(english_docx=fileDir)
    return JsonResponse({'msg':"上传成功",'data':fileDir,'code':200}) 
@csrf_exempt # 允许跨站上传
def doUploadApply(request):
    id = request.session["userinfo"].get("id",None)

    file = request.FILES.get("file")
    fileDir = upload(file)
    print('2上传的结果',fileDir)
    StudentTitleMsg.objects.filter(student_id=id).update(apply_docx=fileDir)
    return JsonResponse({'msg':"上传成功",'data':fileDir,'code':200}) 
@csrf_exempt # 允许跨站上传
def doUploadArticle(request):
    id = request.session["userinfo"].get("id",None)

    file = request.FILES.get("file")
    fileDir = upload(file)
    print('2上传的结果',fileDir)
    StudentGraduateArticle.objects.filter(student_id=id).update(article_docx=fileDir)
    return JsonResponse({'msg':"上传成功",'data':fileDir,'code':200}) 
# (2.分组选择
def group(request):
    id = request.session["userinfo"].get("id",None)
    name = request.session["userinfo"].get("name",None)

    # 先获取教师人数，保存对应的组
    count1 = Student.objects.all().count()
    count2 = StudentGroup.objects.all().count()
    count_len = math.ceil(count1 / 3)
    need_len = count_len - count2
    print("组是",count2,count_len)
    if need_len:
        for i in range(count2+1,count_len+1):
            data = {
                'name':f'第{i}组',
                'count':0
            }
            StudentGroup (**data).save()
    # 查询所有记录
    data_list = StudentGroup.objects.all()
    # 查询当前教师的小组身份
    data1 = StudentGroup.objects.filter(student_id__icontains=id,student_name__icontains=name).first()
    data = {
        'group_name' : data1.name if data1 else None
    }
    return render(request,'student/group.html',{'data_list':data_list,'data':data})
def doConfirmGroup(request):
    id = request.session["userinfo"].get("id",None)
    name = request.session["userinfo"].get("name",None)

    data = request.POST.dict()
    data.pop("csrfmiddlewaretoken",None)
    data['count'] = int(data['count']) + 1
    # 更新所有的数量
    obj = StudentGroup.objects.filter(id=data['id'],name=data['name']).first()
    # 更新当前教师的职位
    new_data = {}
    if data['count'] == 1:
        data['student_id'] = id
        data['student_name'] = name
        new_data = {
            'group_name':data['name'],
        }
    elif data['count'] == 2:
        data['student_id'] = obj.student_id + f',{id}'
        data['student_name'] = obj.student_name + f',{name}'
        new_data = {
            'group_name':data['name'],
        }
    elif data['count'] == 3:
        data['student_id'] = obj.student_id + f',{id}'
        data['student_name'] = obj.student_name + f',{name}'
        new_data = {
            'group_name':data['name'],
        }

    StudentGroup.objects.filter (name=data['name']).update (**data)
    Student.objects.filter (id=id).update (**new_data)
    return JsonResponse({'msg':"提交成功",'data':data,'new_data':new_data,'code':200})
# 毕业信息
# (1.开题信息
def title_msg(request):
    id = request.session["userinfo"].get("id",None)
    name = request.session["userinfo"].get("name",None)

    # # 小组内的学生组信息
    group_student_arr= Student.objects.filter(id=id,name=name)
    graduate_data= []
    score_data= []
    for item in group_student_arr:
        t_item = StudentGraduateArticle.objects.filter(student_id=item.id).values()
        if t_item:
            graduate_data.append(t_item[0])
            # 继续获取开题信息
            tt_item = StudentTitleMsg.objects.filter(student_id=item.id).values()
            score_data.append(tt_item[0])
    return render(request,'student/title_msg.html',{'graduate_data':enumerate(graduate_data),'score_data':enumerate(score_data)})
# (2.中期检查
def middle_check(request):
    id = request.session["userinfo"].get("id",None)
    name = request.session["userinfo"].get("name",None)

    # # 小组内的学生组信息
    group_student_arr= Student.objects.filter(id=id,name=name)
    graduate_data= []
    score_data= []
    for item in group_student_arr:
        t_item = StudentGraduateArticle.objects.filter(student_id=item.id).values()
        if t_item:
            graduate_data.append(t_item[0])
            # 继续获取开题信息
            tt_item = StudentMiddleCheck.objects.filter(student_id=item.id).values()
            score_data.append(tt_item[0])
    return render(request,'student/middle_check.html',{'graduate_data':enumerate(graduate_data),'score_data':enumerate(score_data)})
# (3.毕业答辩
def graduate_answer(request):
    id = request.session["userinfo"].get("id",None)
    name = request.session["userinfo"].get("name",None)
 
    # # 小组内的学生组信息
    group_student_arr= Student.objects.filter(id=id,name=name)
    graduate_data= []
    score_data= []
    for item in group_student_arr:
        t_item = StudentGraduateArticle.objects.filter(student_id=item.id).values()
        if t_item:
            graduate_data.append(t_item[0])
            # 继续获取开题信息
            tt_item = StudentGraduateAnswer.objects.filter(student_id=item.id).values()
            score_data.append(tt_item[0])
    return render(request,'student/graduate_answer.html',{'graduate_data':enumerate(graduate_data),'score_data':enumerate(score_data)})
# (4.毕业论文
def graduate_article(request):
    id = request.session["userinfo"].get("id",None)
    name = request.session["userinfo"].get("name",None)

    # # 小组内的学生组信息
    group_student_arr= Student.objects.filter(id=id,name=name)
    graduate_data= []
    score_data= []
    for item in group_student_arr:
        t_item = StudentGraduateArticle.objects.filter(student_id=item.id).values()
        if t_item:
            graduate_data.append(t_item[0])
            # 继续获取开题信息
            tt_item = StudentGraduateArticle.objects.filter(student_id=item.id).values()
            score_data.append(tt_item[0])
    return render(request,'student/graduate_article.html',{'graduate_data':enumerate(graduate_data),'score_data':enumerate(score_data)})