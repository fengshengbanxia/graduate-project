from django.urls import path, re_path
from ..views import *

urlpatterns = [
    # 首页
    path('', IndexViews.login),
    # 登录页
    path('login', IndexViews.login, name="myhome_login"),
    path('login/doLogin', IndexViews.doLogin, name="myhome_doLogin"),
    # 注册页
    path('register', IndexViews.register, name="myhome_register"),
    path('register/doRegister', IndexViews.doRegister, name="myhome_doRegister"),
    # 退出登录
    path('doLogout', IndexViews.doLogout, name="myhome_doLogout"),
    path('home/index', IndexViews.index, name="myhome_index"),

    # 一、学生部分
    # (1.个人信息
    path('home/student/index', StudentViews.index, name="student_index"),
    # (2.选题信息
    path('home/student/select_title', StudentViews.select_title, name="student_select_title"),
    path('home/student/doUploadTitle', StudentViews.doUploadTitle, name="student_doUploadTitle"),
    path('home/student/doUploadEnglish', StudentViews.doUploadEnglish, name="student_doUploadEnglish"),
    path('home/student/doUploadApply', StudentViews.doUploadApply, name="student_doUploadApply"),
    path('home/student/doUploadArticle', StudentViews.doUploadArticle, name="student_doUploadArticle"),
    path('home/student/group', StudentViews.group, name="student_group"),
    path('home/student/doConfirmGroup', StudentViews.doConfirmGroup, name="student_doConfirmGroup"),
    # (3.毕业信息
    path('home/student/title_msg', StudentViews.title_msg, name="student_title_msg"),
    path('home/student/middle_check', StudentViews.middle_check, name="student_middle_check"),
    path('home/student/graduate_answer', StudentViews.graduate_answer, name="student_graduate_answer"),
    path('home/student/graduate_article', StudentViews.graduate_article, name="student_graduate_article"),

    # 二、教师部分
    # (1.个人信息
    path('home/teacher/index', TeacherViews.index, name="teacher_index"),
    # (2.选题信息
    path('home/teacher/design_title', TeacherViews.design_title, name="teacher_design_title"),
    path('home/teacher/doUploadTask', TeacherViews.doUploadTask, name="teacher_doUploadTask"),
    path('home/teacher/doUploadGuide', TeacherViews.doUploadGuide, name="teacher_doUploadGuide"),
    path('home/teacher/doConfirmStudent', TeacherViews.doConfirmStudent, name="teacher_doConfirmStudent"),
    path('home/teacher/doSubmitBrief', TeacherViews.doSubmitBrief, name="teacher_doSubmitBrief"),
    path('home/teacher/group', TeacherViews.group, name="teacher_group"),
    path('home/teacher/doConfirmGroup', TeacherViews.doConfirmGroup, name="teacher_doConfirmGroup"),
    # (3.毕业评分
    path('home/teacher/student_score', TeacherViews.student_score, name="teacher_student_score"),
    path('home/teacher/doSubmitEnglish', TeacherViews.doSubmitEnglish, name="teacher_doSubmitEnglish"),
    path('home/teacher/doSubmitArticle', TeacherViews.doSubmitArticle, name="teacher_doSubmitArticle"),
    path('home/teacher/doOutputArticle', TeacherViews.doOutputArticle, name="teacher_doOutputArticle"),
    # (4.小组任务
    path('home/teacher/title_msg', TeacherViews.title_msg, name="teacher_title_msg"),
    path('home/teacher/doFirstScore', TeacherViews.doFirstScore, name="teacher_doFirstScore"),
    path('home/teacher/doFirstRemark', TeacherViews.doFirstRemark, name="teacher_doFirstRemark"),
    path('home/teacher/middle_check', TeacherViews.middle_check, name="teacher_middle_check"),
    path('home/teacher/doSecondScore', TeacherViews.doSecondScore, name="teacher_doSecondScore"),
    path('home/teacher/doSecondRemark', TeacherViews.doSecondRemark, name="teacher_doSecondRemark"),
    path('home/teacher/graduate_answer', TeacherViews.graduate_answer, name="teacher_graduate_answer"),
    path('home/teacher/doThirdScore', TeacherViews.doThirdScore, name="teacher_doThirdScore"),
    path('home/teacher/doThirdRemark', TeacherViews.doThirdRemark, name="teacher_doThirdRemark"),
    path('home/teacher/graduate_article', TeacherViews.graduate_article, name="teacher_graduate_article"),
    path('home/teacher/doViewScore', TeacherViews.doViewScore, name="teacher_doViewScore"),
    path('home/teacher/doViewRemark', TeacherViews.doViewRemark, name="teacher_doViewRemark"),

    # 三、管理员部分
    # (1.个人信息
    path('home/admin/index', AdminViews.index, name="admin_index"),
    # (2.教师管理
    path('home/admin/teacher', AdminViews.teacher_list, name="admin_teacher"),
    path('home/admin/doDeleteTeacher', AdminViews.doDeleteTeacher, name="admin_doDeleteTeacher"),
    path('home/admin/doSearchTeacher', AdminViews.doSearchTeacher, name="admin_doSearchTeacher"),
    # (3.学生管理
    path('home/admin/student', AdminViews.student_list, name="admin_student"),
    path('home/admin/doDeleteStudent', AdminViews.doDeleteStudent, name="admin_doDeleteStudent"),
    path('home/admin/doSearchStudent', AdminViews.doSearchStudent, name="admin_doSearchStudent"),
    # (4.课题管理
    path('home/admin/title', AdminViews.title_list, name="admin_title"),
    path('home/admin/doDeleteTitle', AdminViews.doDeleteTitle, name="admin_doDeleteTitle"),
    path('home/admin/doSearchTitle', AdminViews.doSearchTitle, name="admin_doSearchTitle"),


    # 404页面（/属于正则表达式的内容，而*属于非法字符）
    re_path('/', IndexViews.empty, name="myhome_empty"),
]
'''



'''
