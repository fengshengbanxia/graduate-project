from django.shortcuts import render
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt

from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Q
from ..models import *
from ..utils.func import upload,word  # 引入自定义上传模块
import math
import datetime




# 个人信息
def index(request):
    # data = request.session.get("userinfo",None)
    # 1.获取5个最新的数据(学生信息)
    data_len = 5
    data_list = []
    # （1.教师信息
    data_list1 = Teacher.objects.filter ().order_by ('register_time')[:data_len]
    for item in data_list1:
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
    return render(request,'teacher/index.html',{'data_list':data_list,'show_data':show_data})
# 选择信息
# (1.设计开题
def design_title(request):
    id = request.session["userinfo"].get("id",None)
    name = request.session["userinfo"].get("name",None)

    # 先检查是否有当前教师的开题设计记录，
    data_obj = StudentSelectTitle.objects.filter(teacher_id=id).first()
    data = None
    if data_obj:
        data = data_obj
    else:
        # 如果没有记录，则创建一条记录
        data = StudentSelectTitle(teacher_id=id,teacher_name=name)
        data.save()
        StudentTitleMsg(teacher_id=id,teacher_name=name).save()
        StudentGraduateArticle(teacher_id=id,teacher_name=name).save()
        StudentGraduateAnswer(teacher_id=id,teacher_name=name).save()
        StudentMiddleCheck(teacher_id=id,teacher_name=name).save()
    data_list = Student.objects.all()
    return render(request,'teacher/design_title.html',{'data':data,'data_list': enumerate(data_list)})
@csrf_exempt # 允许跨站上传
def doUploadTask(request):
    id = request.session["userinfo"].get("id",None)

    file = request.FILES.get("file")
    fileDir = upload(file)
    print('1上传的结果',fileDir)
    StudentSelectTitle.objects.filter(teacher_id=id).update(task_docx=fileDir)
    return JsonResponse({'msg':"上传成功",'data':fileDir,'code':200})
@csrf_exempt # 允许跨站上传
def doUploadGuide(request):
    id = request.session["userinfo"].get("id",None)

    file = request.FILES.get("file")
    fileDir = upload(file)
    print('2上传的结果',fileDir)
    StudentSelectTitle.objects.filter(teacher_id=id).update(guide_docx=fileDir)
    return JsonResponse({'msg':"上传成功",'data':fileDir,'code':200})
def doConfirmStudent(request):
    id = request.session["userinfo"].get("id",None)

    data = request.POST.dict()
    data.pop("csrfmiddlewaretoken",None)
    StudentSelectTitle.objects.filter(teacher_id=id).update(**data)
    StudentTitleMsg.objects.filter(teacher_id=id).update(**data)
    StudentGraduateArticle.objects.filter(teacher_id=id).update(**data)
    StudentGraduateAnswer.objects.filter(teacher_id=id).update(**data)
    StudentMiddleCheck.objects.filter(teacher_id=id).update(**data)
    return JsonResponse({'msg':"提交成功",'code':200})
def doSubmitBrief(request):
    id = request.session["userinfo"].get("id",None)

    data = request.POST.dict()
    data.pop("csrfmiddlewaretoken",None)
    StudentSelectTitle.objects.filter(teacher_id=id).update(**data)
    StudentTitleMsg.objects.filter(teacher_id=id).update(**data)
    StudentGraduateArticle.objects.filter(teacher_id=id).update(**data)
    StudentGraduateAnswer.objects.filter(teacher_id=id).update(**data)
    StudentMiddleCheck.objects.filter(teacher_id=id).update(**data)
    return JsonResponse({'msg':"提交成功",'code':200})
# (2.分组选择
def group(request):
    id = request.session["userinfo"].get("id",None)
    name = request.session["userinfo"].get("name",None)

    # 先获取教师人数，保存对应的组
    count1 = Teacher.objects.all().count()
    count2 = TeacherGroup.objects.all().count()
    count_len = math.ceil(count1 / 3)
    need_len = count_len - count2
    print("组是",count2,count_len)
    if need_len:
        for i in range(count2+1,count_len+1):
            data = {
                'name':f'第{i}组',
                'count':0
            }
            TeacherGroup (**data).save()
    # 查询所有记录
    data_list = TeacherGroup.objects.all()
    # 查询当前教师的小组身份
    data1 = TeacherGroup.objects.filter(teacher_id__icontains=id,teacher_name__icontains=name).first()
    data = {}
    if data1:
        # 组名
        data['group_name'] = data1.name
        # 身份类型
        arr1 = data1.teacher_id.split(',')
        arr2 = data1.teacher_name.split(',')
        arr3 = data1.teacher_type.split(',')
        print(arr1,arr2,arr3)
        for item1,item2,item3 in zip(arr1,arr2,arr3):
            if int(item1)==int(id) and item2==name:
                data['group_type'] = item3
        print(data)
    return render(request,'teacher/group.html',{'data_list':data_list,'data':data})
def doConfirmGroup(request):
    id = request.session["userinfo"].get("id",None)
    name = request.session["userinfo"].get("name",None)

    data = request.POST.dict()
    data.pop("csrfmiddlewaretoken",None)
    data['count'] = int(data['count']) + 1
    # 更新所有的数量
    obj = TeacherGroup.objects.filter(id=data['id'],name=data['name']).first()
    # 更新当前教师的职位
    new_data = {}
    if data['count'] == 1:
        data['teacher_id'] = id
        data['teacher_name'] = name
        data['teacher_type'] = '组长'
        new_data = {
            'group_name':data['name'],
            'group_type':'组长',
        }
    elif data['count'] == 2:
        data['teacher_id'] = obj.teacher_id + f',{id}'
        data['teacher_name'] = obj.teacher_name + f',{name}'
        data['teacher_type'] = obj.teacher_type + f',秘书'
        new_data = {
            'group_name':data['name'],
            'group_type':'秘书',
        }
    elif data['count'] == 3:
        data['teacher_id'] = obj.teacher_id + f',{id}'
        data['teacher_name'] = obj.teacher_name + f',{name}'
        data['teacher_type'] = obj.teacher_type + f',阅卷教师'
        new_data = {
            'group_name':data['name'],
            'group_type':'阅卷教师',
        }

    TeacherGroup.objects.filter (name=data['name']).update (**data)
    Teacher.objects.filter (id=id).update (**new_data)
    return JsonResponse({'msg':"提交成功",'data':data,'new_data':new_data,'code':200})
# 毕业评分
# (1.学生成绩
def student_score(request):
    id = request.session["userinfo"].get("id",None)
    name = request.session["userinfo"].get("name",None)

    ## 毕业学生信息
    data1= StudentTitleMsg.objects.filter(teacher_id=id,teacher_name=name).first()
    data2= StudentMiddleCheck.objects.filter(teacher_id=id,teacher_name=name).first()
    data3= StudentGraduateAnswer.objects.filter(teacher_id=id,teacher_name=name).first()
    data4= StudentGraduateArticle.objects.filter(teacher_id=id,teacher_name=name).first()

    data5= Student.objects.filter(id=data4.student_id).first() if data4 else None
    total_data = {
        "first_score":data1.first_score if data1 else None,
        "first_remark":data1.first_remark if data1 else None,
        "english_score":data1.english_score if data1 else None,
        "english_remark":data1.english_remark if data1 else None,

        "second_score":data2.second_score if data2 else None,
        "second_remark":data2.second_remark if data2 else None,

        "third_score":data3.third_score if data3 else None,
        "third_remark":data3.third_remark if data3 else None,
        "third_rank":data3.graduate_rank if data3 else None,

        "guide_score":data4.guide_score if data4 else None,
        "guide_remark":data4.guide_remark if data4 else None,
        "view_score":data4.view_score if data4 else None,
        "view_remark":data4.view_remark if data4 else None,

        "name": data4.name if data4 else None,
        "brief": data4.brief if data4 else None,
        "number": data5.number if data5 else None,
        "student_name": data4.student_name if data4 else None,
        "teacher_name": data4.teacher_name if data4 else None

    }

    ## 毕业信息
    data = data1
    graduate_data = data4

    return render(request,'teacher/student_score.html',{'data':data,'graduate_data':graduate_data,'total_data':total_data})
def doSubmitEnglish(request):
    id = request.session["userinfo"].get("id",None)
    name = request.session["userinfo"].get("name",None)

    data = request.POST.dict()
    data.pop("csrfmiddlewaretoken",None)
    new_data = {
        'english_score':data['score'],
        'english_remark':data['remark']
    }
    StudentTitleMsg.objects.filter (teacher_id=id,teacher_name=name).update (**new_data)
    return JsonResponse({'msg':"提交成功",'code':200})
def doSubmitArticle(request):
    id = request.session["userinfo"].get("id",None)
    name = request.session["userinfo"].get("name",None)

    data = request.POST.dict()
    data.pop("csrfmiddlewaretoken",None)
    new_data = {
        'guide_score':data['score'],
        'guide_remark':data['remark']
    }
    StudentGraduateArticle.objects.filter (teacher_id=id,teacher_name=name).update (**new_data)
    return JsonResponse({'msg':"提交成功",'code':200})
def doOutputArticle(request):
    id = request.session["userinfo"].get ("id", None)
    name = request.session["userinfo"].get ("name", None)

    ## 毕业学生信息
    data1 = StudentTitleMsg.objects.filter (teacher_id=id, teacher_name=name).first ()
    data2 = StudentMiddleCheck.objects.filter (teacher_id=id, teacher_name=name).first ()
    data3 = StudentGraduateAnswer.objects.filter (teacher_id=id, teacher_name=name).first ()
    data4 = StudentGraduateArticle.objects.filter (teacher_id=id, teacher_name=name).first ()

    data5 = Student.objects.filter (id=data4.student_id).first () if data4 else None

    file_list = [

        {'title': "课题", "content": data4.name if data4 else None},
        {'title': "介绍", "content": data4.brief if data4 else None},
        {'title': "学生ID", "content": data5.number if data5 else None},
        {'title': "毕业学生", "content": data4.student_name if data4 else None},
        {'title': "指导老师", "content": data4.teacher_name if data4 else None},

        {'title': "开题答辩成绩", "content": data1.first_score if data1 else None},
        {'title': "开题答辩评语", "content": data1.first_remark if data1 else None},
        {'title': "外语翻译成绩", "content": data1.english_score if data1 else None},
        {'title': "外语翻译评语", "content": data1.english_remark if data1 else None},
        {'title': "中期检查成绩", "content": data2.second_score if data2 else None},
        {'title': "中期检查评语", "content": data2.second_remark if data2 else None},
        {'title': "毕业答辩成绩", "content": data3.third_score if data3 else None},
        {'title': "毕业答辩评语", "content": data3.third_remark if data3 else None},
        {'title': "毕业答辩等级", "content": data3.graduate_rank if data3 else None},
        {'title': "毕业论文成绩", "content": data4.guide_score if data4 else None},
        {'title': "毕业论文评语", "content": data4.guide_remark if data4 else None},
        {'title': "查阅论文成绩", "content": data4.view_score if data4 else None},
        {'title': "查阅论文评语", "content": data4.view_remark if data4 else None},

    ]

    fileDir = word('毕业生文档',file_list)

    return JsonResponse({'msg':"导出成功",'data':fileDir,'code':200})
# 小组任务
# (1.开题信息
def title_msg(request):
    id = request.session["userinfo"].get("id",None)
    name = request.session["userinfo"].get("name",None)

    data= Teacher.objects.filter(id=id,name=name).first()
    # # 小组内的学生组信息
    group_student_arr= Student.objects.filter(group_name=data.group_name)
    graduate_data= []
    score_data= []
    for item in group_student_arr:
        t_item = StudentGraduateArticle.objects.filter(teacher_id=id,student_id=item.id).values()
        if t_item:
            graduate_data.append(t_item[0])
            # 继续获取开题信息
            tt_item = StudentTitleMsg.objects.filter(teacher_id=id,student_id=item.id).values()
            score_data.append(tt_item[0])
    return render(request,'teacher/title_msg.html',{'data':data,'graduate_data':enumerate(graduate_data),'score_data':enumerate(score_data)})
def doFirstScore(request):
    id = request.session["userinfo"].get("id",None)
    name = request.session["userinfo"].get("name",None)

    data = request.POST.dict()
    data.pop("csrfmiddlewaretoken",None)
    new_data = {
        'first_score':data['score'],
    }
    StudentTitleMsg.objects.filter (teacher_id=id,teacher_name=name,student_id=data['id']).update (**new_data)
    return JsonResponse({'msg':"提交成功",'code':200})
def doFirstRemark(request):
    id = request.session["userinfo"].get("id",None)
    name = request.session["userinfo"].get("name",None)

    data = request.POST.dict()
    data.pop("csrfmiddlewaretoken",None)
    new_data = {
        'first_remark':data['remark']
    }
    StudentTitleMsg.objects.filter (teacher_id=id,teacher_name=name,student_id=data['id']).update (**new_data)
    return JsonResponse({'msg':"提交成功",'code':200})
# (2.中期检查
def middle_check(request):
    id = request.session["userinfo"].get("id",None)
    name = request.session["userinfo"].get("name",None)

    data= Teacher.objects.filter(id=id,name=name).first()
    # # 小组内的学生组信息
    group_student_arr= Student.objects.filter(group_name=data.group_name)
    graduate_data= []
    score_data= []
    for item in group_student_arr:
        t_item = StudentGraduateArticle.objects.filter(teacher_id=id,student_id=item.id).values()
        if t_item:
            graduate_data.append(t_item[0])
            # 继续获取开题信息
            tt_item = StudentMiddleCheck.objects.filter(teacher_id=id,student_id=item.id).values()
            score_data.append(tt_item[0])
    return render(request,'teacher/middle_check.html',{'data':data,'graduate_data':enumerate(graduate_data),'score_data':enumerate(score_data)})
def doSecondScore(request):
    id = request.session["userinfo"].get("id",None)
    name = request.session["userinfo"].get("name",None)

    data = request.POST.dict()
    data.pop("csrfmiddlewaretoken",None)
    new_data = {
        'second_score':data['score'],
    }
    StudentMiddleCheck.objects.filter (teacher_id=id,teacher_name=name,student_id=data['id']).update (**new_data)
    return JsonResponse({'msg':"提交成功",'code':200})
def doSecondRemark(request):
    id = request.session["userinfo"].get("id",None)
    name = request.session["userinfo"].get("name",None)

    data = request.POST.dict()
    data.pop("csrfmiddlewaretoken",None)
    new_data = {
        'second_remark':data['remark']
    }
    StudentMiddleCheck.objects.filter (teacher_id=id,teacher_name=name,student_id=data['id']).update (**new_data)
    return JsonResponse({'msg':"提交成功",'code':200})
# (3.毕业答辩
def graduate_answer(request):
    id = request.session["userinfo"].get("id",None)
    name = request.session["userinfo"].get("name",None)

    data= Teacher.objects.filter(id=id,name=name).first()
    # # 小组内的学生组信息
    group_student_arr= Student.objects.filter(group_name=data.group_name)
    graduate_data= []
    score_data= []
    for item in group_student_arr:
        t_item = StudentGraduateArticle.objects.filter(teacher_id=id,student_id=item.id).values()
        if t_item:
            graduate_data.append(t_item[0])
            # 继续获取开题信息
            tt_item = StudentGraduateAnswer.objects.filter(teacher_id=id,student_id=item.id).values()
            score_data.append(tt_item[0])
    return render(request,'teacher/graduate_answer.html',{'data':data,'graduate_data':enumerate(graduate_data),'score_data':enumerate(score_data)})
def doThirdScore(request):
    id = request.session["userinfo"].get("id",None)
    name = request.session["userinfo"].get("name",None)

    data = request.POST.dict()
    data.pop("csrfmiddlewaretoken",None)
    new_data = {
        'third_score':data['score'],
        'graduate_rank':data['rank'],
    }
    StudentGraduateAnswer.objects.filter (teacher_id=id,teacher_name=name,student_id=data['id']).update (**new_data)
    return JsonResponse({'msg':"提交成功",'code':200})
def doThirdRemark(request):
    id = request.session["userinfo"].get("id",None)
    name = request.session["userinfo"].get("name",None)

    data = request.POST.dict()
    data.pop("csrfmiddlewaretoken",None)
    new_data = {
        'third_remark':data['remark']
    }
    StudentGraduateAnswer.objects.filter (teacher_id=id,teacher_name=name,student_id=data['id']).update (**new_data)
    return JsonResponse({'msg':"提交成功",'code':200})
# (4.毕业论文
def graduate_article(request):
    id = request.session["userinfo"].get("id",None)
    name = request.session["userinfo"].get("name",None)

    data= Teacher.objects.filter(id=id,name=name).first()
    # # 小组内的学生组信息
    group_student_arr= Student.objects.filter(group_name=data.group_name)
    graduate_data= []
    score_data= []
    for item in group_student_arr:
        t_item = StudentGraduateArticle.objects.filter(teacher_id=id,student_id=item.id).values()
        if t_item:
            graduate_data.append(t_item[0])
            # 继续获取开题信息
            tt_item = StudentGraduateArticle.objects.filter(teacher_id=id,student_id=item.id).values()
            score_data.append(tt_item[0])
    return render(request,'teacher/graduate_article.html',{'data':data,'graduate_data':enumerate(graduate_data),'score_data':enumerate(score_data)})
def doViewScore(request):
    id = request.session["userinfo"].get("id",None)
    name = request.session["userinfo"].get("name",None)

    data = request.POST.dict()
    data.pop("csrfmiddlewaretoken",None)
    new_data = {
        'view_score':data['score'],
    }
    StudentGraduateArticle.objects.filter (teacher_id=id,teacher_name=name,student_id=data['id']).update (**new_data)
    return JsonResponse({'msg':"提交成功",'code':200})
def doViewRemark(request):
    id = request.session["userinfo"].get("id",None)
    name = request.session["userinfo"].get("name",None)

    data = request.POST.dict()
    data.pop("csrfmiddlewaretoken",None)
    new_data = {
        'view_remark':data['remark']
    }
    StudentGraduateArticle.objects.filter (teacher_id=id,teacher_name=name,student_id=data['id']).update (**new_data)
    return JsonResponse({'msg':"提交成功",'code':200})