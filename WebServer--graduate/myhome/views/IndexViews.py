from django.shortcuts import render

# Create your views here.

# 导入Django的render和redirect函数，用于处理HTTP请求并返回响应
from django.shortcuts import render, redirect
# 导入Django的密码处理函数，用于加密和验证密码
from django.contrib.auth.hashers import make_password, check_password
# 导入Django的JsonResponse类，用于返回JSON格式的HTTP响应
from django.http import JsonResponse
# 导入当前应用下的模型，用于数据库操作
from ..models import *
# 导入time模块，用于时间相关操作
import time


# 登录页
def login(request):
    return render(request,'login.html')


# 执行登录
def doLogin(request):
    """
    处理用户登录请求。

    参数:
    - request: HTTP请求对象，包含登录表单数据。

    返回值:
    - JsonResponse对象，包含登录结果信息和状态码。
    """
    data = request.POST.dict()  # 从请求中获取表单数据
    data.pop("csrfmiddlewaretoken", None)  # 移除CSRF令牌
    isAuth = False  # 初始化认证标志为False

    # 首先尝试在学生表中验证用户
    type = 'student'  # 默认用户类型为学生
    user_obj = Student.objects.filter(number=data['number']).first()  # 查询学生信息
    if not user_obj:
        isAuth = False
    else:
        isAuth = True
        # 验证密码是否正确
        res = check_password(data['password'], user_obj.password)
        if not res:
            return JsonResponse({'msg': '登录失败！密码错误！', 'code': 403})

    # 如果学生表验证失败，尝试在教师表中验证用户
    if not isAuth:
        type = 'teacher'  # 用户类型改为教师
        user_obj = Teacher.objects.filter(number=data['number']).first()  # 查询教师信息
        if user_obj:
            isAuth = True
            # 验证密码是否正确
            res = check_password(data['password'], user_obj.password)
            if not res:
                return JsonResponse({'msg': '登录失败！密码错误！', 'code': 403})

    # 如果教师表验证失败，尝试在管理员表中验证用户
    if not isAuth:
        type = 'admin'  # 用户类型改为管理员
        user_obj = Admin.objects.filter(number=data['number']).first()
        if user_obj:
            isAuth = True
            # 验证密码是否正确
            res = check_password(data['password'], user_obj.password)
            if not res:
                return JsonResponse({'msg': '登录失败！密码错误！', 'code': 403})

    # 如果用户在任一表中通过验证，则设置会话认证信息
    if isAuth:
        # 生成会话身份认证数据
        data['type'] = type
        data['name'] = user_obj.name
        data['id'] = user_obj.id
        request.session['userinfo'] = data  # 将用户信息存储在会话中
        return JsonResponse({'msg': '登录成功！', 'type': type, 'code': 200})
    else:
        # 如果所有验证都失败，则返回登录失败信息
        return JsonResponse({'msg': '登录失败！帐号不存在！', 'code': 403})


# 注册页
def register(request):
    return render(request,'register.html')


# 执行注册
def doRegister(request):
    data = request.POST.dict()
    data.pop("csrfmiddlewaretoken",None)
    # 添加注册时间
    isExist = False
    data['register_time'] = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
    # 密码加密
    data['password'] = make_password(data['password'], None, 'pbkdf2_sha256')
    if data['type'] == 'student':
        data.pop("type")
        data['cross'] = '0'
        # 查询是否帐号已经被注册
        obj = Student.objects.filter(number=data['number']).first()
        if not obj:
            Student(**data).save()
        else:
            isExist = True
    elif data['type'] == 'teacher':
        data.pop("type")
        # 查询是否帐号已经被注册
        obj = Teacher.objects.filter(number=data['number']).first()
        if not obj:
            Teacher(**data).save()
        else:
            isExist = True
    elif data['type'] == 'admin':
        data.pop("type")
        # 查询是否帐号已经被注册
        obj = Admin.objects.filter(number=data['number']).first()
        if not obj:
            Admin(**data).save()
        else:
            isExist = True
    else:
        return JsonResponse ({'msg': '注册失败！身份类型参数没有传递', 'code': 403})
    if not isExist:
        return JsonResponse ({'msg': '注册成功！', 'code': 200})
    else:
        return JsonResponse ({'msg': '当前ID已经被注册，请重新输入！', 'code': 403})


# 执行退出登录
def doLogout(request):
    request.session.flush()
    print("退出登录成功")
    return redirect("myhome_login")


# 后台主页
def index(request):
    return render(request,'index.html')


# 404页
def empty(request):
    return render(request,'404error.html')

