# 导入Django序列化器，用于数据的序列化处理
from django.core import serializers
# 导入CSRF装饰器，用于指定视图免受跨站请求伪造攻击
from django.views.decorators.csrf import csrf_exempt

# 导入Django短路径，用于快速响应请求
from django.shortcuts import render
# 导入JsonResponse，用于返回JSON格式的响应
from django.http import JsonResponse
# 导入Django的Q对象，用于构建复杂的查询
from django.db.models import Q
# 引入内部模型，用于数据库操作
from ..models import *
# 引入自定义上传模块，用于文件上传处理
from ..utils.func import upload

# 导入math模块，用于数学计算
import math
# 导入datetime模块，用于日期和时间操作
import datetime



# 个人信息
def index(request):

    # 初始化数据长度和数据列表
    data_len = 5
    data_list = []

    # 获取最新的学生信息
    data_list1 = Student.objects.filter().order_by('register_time')[:data_len]
    for item in data_list1:
        data_list.append({
            'number': item.number,
            'name': item.name,
            'register_time': item.register_time,
            'type': '学生',
        })

    # 计算和组织展示栏信息
    last_time = datetime.datetime.now() - datetime.timedelta(days=90)
    data1_1 = Student.objects.all().count()  # 总学生数
    data1_2 = len(Student.objects.filter(register_time__gte=last_time).values())  # 90天内新增学生数
    data2_1 = Teacher.objects.all().count()  # 总教师数
    data2_2 = len(Teacher.objects.filter(register_time__gte=last_time).values())  # 90天内新增教师数
    data3_1 = StudentGraduateArticle.objects.all().count()  # 总毕业论文数
    data3_2 = math.ceil(StudentGraduateArticle.objects.all().count()/2)  # 按篇数计算的毕业论文展示数（每两篇展示一次）
    show_data = {
        'show_count1': data1_1,
        'show_add1': data1_2,
        'show_count2': data2_1,
        'show_add2': data2_2,
        'show_count3': data3_1,
        'show_add3': data3_2,
    }

    # 渲染并返回主页模板
    return render(request, 'student/index.html', {'data_list': data_list, 'show_data': show_data})

# 选择信息
# (1.选题信息
def select_title(request):
    """
    根据学生信息，从数据库中选取相关的标题信息和文档，用于在前端页面展示。

    参数:
    - request: HttpRequest对象，包含客户端请求的信息。

    返回值:
    - HttpResponse对象，渲染的select_title.html页面，其中包含学生选题相关的信息。
    """

    # 从request.session中获取学生id和姓名
    id = request.session["userinfo"].get("id", None)
    name = request.session["userinfo"].get("name", None)

    # 查询学生在三个不同表中的选题记录，获取第一条记录
    data_obj1 = StudentSelectTitle.objects.filter(student_id=id).first()
    data_obj2 = StudentGraduateArticle.objects.filter(student_id=id).first()
    data_obj3 = StudentTitleMsg.objects.filter(student_id=id).first()

    # 将查询结果整理成字典格式，用于前端展示
    data = {
        'task_docx': data_obj1.task_docx if data_obj1 else None,
        'guide_docx': data_obj1.guide_docx if data_obj1 else None,

        'article_docx': data_obj2.article_docx if data_obj2 else None,

        'title_docx': data_obj3.title_docx if data_obj3 else None,
        'english_docx': data_obj3.english_docx if data_obj3 else None,
        'apply_docx': data_obj3.apply_docx if data_obj3 else None,

        'id': data_obj3.id if data_obj3 else None,
        'name': data_obj3.name if data_obj3 else None,
        'brief': data_obj3.brief if data_obj3 else None,
        'student_id': data_obj3.student_id if data_obj3 else None,
        'student_name': data_obj3.student_name if data_obj3 else None,
        'teacher_id': data_obj3.teacher_id if data_obj3 else None,
        'teacher_name': data_obj3.teacher_name if data_obj3 else None,
    }

    # 渲染并返回select_title.html页面，携带数据data
    return render(request,'student/select_title.html',{'data':data})

@csrf_exempt # 允许跨站上传
def doUploadTitle(request):
    id = request.session["userinfo"].get("id", None)

    file = request.FILES.get("file")
    fileDir = upload(file)
    print('1上传的结果', fileDir)
    StudentTitleMsg.objects.filter(student_id=id).update(title_docx=fileDir)
    return JsonResponse({'msg': "上传成功", 'data': fileDir, 'code': 200})
@csrf_exempt # 允许跨站上传
def doUploadEnglish(request):
    id = request.session["userinfo"].get("id", None)

    file = request.FILES.get("file")
    fileDir = upload(file)
    print('2上传的结果', fileDir)
    StudentTitleMsg.objects.filter(student_id=id).update(english_docx=fileDir)
    return JsonResponse({'msg': "上传成功", 'data': fileDir, 'code': 200})
@csrf_exempt # 允许跨站上传
def doUploadApply(request):
    id = request.session["userinfo"].get("id",None)

    file = request.FILES.get("file")
    fileDir = upload(file)
    print('3上传的结果', fileDir)
    StudentTitleMsg.objects.filter(student_id=id).update(apply_docx=fileDir)
    return JsonResponse({'msg': "上传成功", 'data': fileDir, 'code': 200})
@csrf_exempt # 允许跨站上传
def doUploadArticle(request):
    id = request.session["userinfo"].get("id",None)

    file = request.FILES.get("file")
    fileDir = upload(file)
    print('4上传的结果', fileDir)
    StudentGraduateArticle.objects.filter(student_id=id).update(article_docx=fileDir)
    return JsonResponse({'msg': "上传成功", 'data': fileDir, 'code': 200})
# (2.分组选择
def group(request):
    """
    处理学生分组页面的请求，包括创建新的分组（如果需要）和渲染当前教师的分组信息。

    参数:
    request - HttpRequest对象，包含客户端发来的HTTP请求信息。

    返回值:
    HttpResponse对象，渲染的分组页面。
    """
    # 从会话中获取用户ID和姓名
    id = request.session["userinfo"].get("id",None)
    name = request.session["userinfo"].get("name",None)

    # 计算需要创建的分组数量，并创建新的分组
    count1 = Student.objects.all().count()  # 获取学生总数
    count2 = StudentGroup.objects.all().count()  # 获取已有的分组数
    count_len = math.ceil(count1 / 3)  # 计算理论上的分组数量
    need_len = count_len - count2  # 计算需要创建的分组数量
    print("组是", count2, count_len)
    if need_len:
        for i in range(count2+1, count_len+1):
            data = {
                'name': f'第{i}组',
                'count': 0
            }
            StudentGroup(**data).save()  # 创建新的分组

    # 查询所有分组信息
    data_list = StudentGroup.objects.all()
    # 查询当前教师所属的分组
    data1 = StudentGroup.objects.filter(student_id__icontains=id, student_name__icontains=name).first()
    data = {
        'group_name': data1.name if data1 else None  # 如果找到所属分组，则获取分组名
    }
    # 渲染分组页面
    return render(request, 'student/group.html', {'data_list': data_list, 'data': data})

def doConfirmGroup(request):
    """
    处理确认加入小组的请求。
    参数:
    - request: HTTP请求对象，包含session信息和POST数据。
    返回值:
    - JsonResponse对象，包含操作结果信息。
    """

    # 从session中获取用户id和姓名
    id = request.session["userinfo"].get("id",None)
    name = request.session["userinfo"].get("name",None)

    # 获取并处理POST数据，增加计数器
    data = request.POST.dict()
    data.pop("csrfmiddlewaretoken", None)
    data['count'] = int(data['count']) + 1

    # 根据id和name查询学生小组对象
    obj = StudentGroup.objects.filter(id=data['id'], name=data['name']).first()

    # 根据计数器更新或新增学生信息
    new_data = {}
    if data['count'] == 1:
        # 第一个加入的学生，初始化学生id和姓名
        data['student_id'] = id
        data['student_name'] = name
        new_data = {
            'group_name': data['name'],
        }
    elif data['count'] == 2:
        # 第二个加入的学生，更新学生id和姓名
        data['student_id'] = obj.student_id + f',{id}'
        data['student_name'] = obj.student_name + f',{name}'
        new_data = {
            'group_name': data['name'],
        }
    elif data['count'] == 3:
        # 第三个及以上加入的学生，同样更新学生id和姓名
        data['student_id'] = obj.student_id + f',{id}'
        data['student_name'] = obj.student_name + f',{name}'
        new_data = {
            'group_name': data['name'],
        }

    # 更新学生小组信息和学生信息
    StudentGroup.objects.filter(name=data['name']).update(**data)
    Student.objects.filter(id=id).update(**new_data)

    # 返回操作成功的信息
    return JsonResponse({'msg': "提交成功", 'data': data, 'new_data': new_data, 'code': 200})

# 毕业信息
# (1.开题信息
"""
def title_msg(request):
    
    处理学生标题信息和开题报告信息的请求，并将这些信息渲染到对应的模板中。
    参数:
    request - HttpRequest对象，包含客户端发来的HTTP请求信息。
    返回值:
    HttpResponse对象，渲染后的学生标题信息和开题报告信息页面。
    
    # 从会话中获取学生信息
    id = request.session["userinfo"].get("id", None)  # 从会话中获取当前用户的id
    name = request.session["userinfo"].get("name", None)  # 从会话中获取当前用户的name

    # 查询小组内学生的组信息
    group_student_arr = Student.objects.filter(id=id, name=name)  # 根据id和name查询对应的学生信息

    # 初始化两个列表来存储毕业设计信息和开题报告信息
    title_report = []  # 用于存储每个学生的开题报告信息
    score_data = []  # 用于存储每个学生的开题报告评价信息

    # 遍历查询到的学生信息
    for item in group_student_arr:
        # 获取学生的毕业设计信息
        t_item = StudentTitleMsg.objects.filter(student_id=item.id).values()  # 查询该学生的开题报告信息
        if t_item:
            title_report.append(t_item[0])  # 如果有毕业设计信息，添加到 title_report列表中

            # 获取学生的开题信息
            tt_item = StudentTitleMsg.objects.filter(student_id=item.id).values()  # 查询该学生的开题报告信息
            if tt_item:
                score_data.append(tt_item[0])  # 如果有开题报告评价信息，添加到score_data列表中

    # 渲染并返回页面
    return render(request, 'student/title_msg.html', {'graduate_data': enumerate(title_report), 'score_data': enumerate(score_data)})
    # 渲染模板 'student/title_msg.html'，并传递两个枚举列表 ' title_report' 和 'score_data' 给模板进行渲染
"""


def title_msg(request):
    """
    处理学生标题信息和开题报告信息的请求，并将这些信息渲染到对应的模板中。

    参数:
    request - HttpRequest对象，包含客户端发来的HTTP请求信息。

    返回值:
    HttpResponse对象，渲染后的学生标题信息和开题报告信息页面。
    """
    # 从会话中获取用户信息字典
    user_info = request.session.get("userinfo", {})

    # 从会话字典中获取学生的ID和姓名
    student_id = user_info.get("id")
    student_name = user_info.get("name")

    # 查询学生对象，过滤条件为从会话中获取的学生ID和姓名
    group_student_arr = Student.objects.filter(id=student_id, name=student_name)

    # 初始化两个空列表，用于存储毕业设计信息和开题报告评价信息
    title_report = []  # 用于存储每个学生的开题报告信息
    score_data = []  # 用于存储每个学生的开题报告评价信息

    # 遍历查询到的学生对象
    for student in group_student_arr:
        # 查询学生的开题报告信息，过滤条件为学生ID
        student_title_msgs = StudentTitleMsg.objects.filter(student_id=student.id).values()

        # 如果查询结果存在
        if student_title_msgs.exists():
            # 将查询结果的第一条记录添加到 title_report 列表中
            title_report.append(student_title_msgs[0])
            # 同样的，将查询结果的第一条记录添加到 score_data 列表中
            score_data.append(student_title_msgs[0])

    # 使用 render 函数将查询结果传递给模板进行渲染
    # 将 title_report 和 score_data 列表分别用 enumerate 函数包装后传递给模板
    return render(request, 'student/title_msg.html', {
        'title_report': enumerate(title_report),  # 传递给模板的开题报告信息
        'score_data': enumerate(score_data)  # 传递给模板的开题报告评价信息
    })


# (2.中期检查
def middle_check(request):
    # 从会话中获取用户的ID和姓名
    id = request.session["userinfo"].get("id", None)
    name = request.session["userinfo"].get("name", None)

    # 查询学生对象，过滤条件为从会话中获取的学生ID和姓名
    group_student_arr = Student.objects.filter(id=id, name=name)

    # 初始化两个空列表，用于存储毕业设计信息和中期检查评价信息
    graduate_data = []  # 用于存储每个学生的毕业设计信息
    score_data = []  # 用于存储每个学生的中期检查评价信息

    # 遍历查询到的学生对象
    for item in group_student_arr:
        # 查询学生的毕业设计信息，过滤条件为学生ID
        t_item = StudentGraduateArticle.objects.filter(student_id=item.id).values()

        # 如果查询结果存在
        if t_item:
            # 将查询结果的第一条记录添加到 graduate_data 列表中
            graduate_data.append(t_item[0])

            # 继续获取学生的中期检查评价信息
            tt_item = StudentMiddleCheck.objects.filter(student_id=item.id).values()

            # 将中期检查评价信息添加到 score_data 列表中
            score_data.append(tt_item[0])

    # 使用 render 函数将查询结果传递给模板进行渲染
    # 将 graduate_data 和 score_data 列表分别用 enumerate 函数包装后传递给模板
    return render(request, 'student/middle_check.html', {
        'graduate_data': enumerate(graduate_data),  # 传递给模板的毕业设计信息
        'score_data': enumerate(score_data)  # 传递给模板的中期检查评价信息
    })


# (3.毕业答辩
def graduate_answer(request):
    # 从 session 中获取用户的 id 和姓名
    id = request.session["userinfo"].get("id", None)
    name = request.session["userinfo"].get("name", None)

    # 查询小组内的学生信息
    group_student_arr = Student.objects.filter(id=id, name=name)

    # 初始化两个空列表，用于存储毕业设计信息和毕业答辩信息
    graduate_data = []  # 存储学生的毕业设计信息
    score_data = []  # 存储学生的毕业答辩信息

    # 遍历查询到的学生对象
    for item in group_student_arr:
        # 查询学生的毕业设计信息，过滤条件为学生ID
        t_item = StudentGraduateArticle.objects.filter(student_id=item.id).values()

        # 如果查询结果存在
        if t_item:
            # 将查询结果的第一条记录添加到 graduate_data 列表中
            graduate_data.append(t_item[0])
            # 继续获取学生的毕业答辩信息
            tt_item = StudentGraduateAnswer.objects.filter(student_id=item.id).values()
            # 将查询结果的第一条记录添加到 score_data 列表中
            score_data.append(tt_item[0])

    # 使用 render 函数将查询结果传递给模板进行渲染
    # 将 graduate_data 和 score_data 列表分别用 enumerate 函数包装后传递给模板
    return render(request, 'student/graduate_answer.html',
                  {'graduate_data': enumerate(graduate_data), 'score_data': enumerate(score_data)})


# (4.毕业论文
# 定义视图函数 graduate_article，用于处理显示学生毕业论文信息的请求
def graduate_article(request):
    # 从会话中获取用户信息字典
    id = request.session["userinfo"].get("id", None)
    name = request.session["userinfo"].get("name", None)

    # 查询小组内学生的组信息
    group_student_arr = Student.objects.filter(id=id, name=name)
    graduate_data = []  # 初始化一个空列表，用于存储学生的毕业论文信息
    score_data = []  # 初始化一个空列表，用于存储学生的毕业论文评分信息

    # 遍历查询到的学生对象
    for item in group_student_arr:
        # 查询学生的毕业论文信息，过滤条件为学生ID
        t_item = StudentGraduateArticle.objects.filter(student_id=item.id).values()
        if t_item:  # 如果查询结果存在
            graduate_data.append(t_item[0])  # 将查询结果的第一条记录添加到 graduate_data 列表中
            # 继续查询学生的毕业论文评分信息
            tt_item = StudentGraduateArticle.objects.filter(student_id=item.id).values()
            score_data.append(tt_item[0])  # 将查询结果的第一条记录添加到 score_data 列表中

    # 使用 render 函数将查询结果传递给模板进行渲染
    # 将 graduate_data 和 score_data 列表分别用 enumerate 函数包装后传递给模板
    return render(request, 'student/graduate_article.html', {'graduate_data': enumerate(graduate_data), 'score_data': enumerate(score_data)})
