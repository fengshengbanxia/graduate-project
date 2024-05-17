<div align="center"> 
    <h1> 毕业设计管理系统 </h1>
    <h5> 基于Django的全栈平台</h5>
    <img src="https://img.shields.io/badge/django-3.2.7+-green.svg"/>  
    <img src="https://img.shields.io/badge/python-3.8.6+-green.svg"/>  
    <img src="https://img.shields.io/badge/layui-2.6.2+-green.svg"/>  
    <img src="https://img.shields.io/badge/jquery-3.6.0+-green.svg"/>  
    <img src="https://gitee.com/MiniWildCat/graduate-project/raw/master/%E9%A1%B9%E7%9B%AE%E5%B1%95%E7%A4%BA%E5%9B%BE%E7%89%87/登录页.jpg"/>   
    <img src="https://gitee.com/MiniWildCat/graduate-project/raw/master/%E9%A1%B9%E7%9B%AE%E5%B1%95%E7%A4%BA%E5%9B%BE%E7%89%87/管理员-首页.jpg"/>  
    <img src="https://gitee.com/MiniWildCat/graduate-project/raw/master/%E9%A1%B9%E7%9B%AE%E5%B1%95%E7%A4%BA%E5%9B%BE%E7%89%87/教师-首页.jpg"/>   
    <img src="https://gitee.com/MiniWildCat/graduate-project/raw/master/%E9%A1%B9%E7%9B%AE%E5%B1%95%E7%A4%BA%E5%9B%BE%E7%89%87/学生-首页.jpg"/>   
</div>








### 一、项目介绍

#### 1.项目简介

​		基于Django打造的高校毕业设计管理系统，完整地展示了目前高校与毕业生的交互流程。前端采用jquery+layui进行页面的创建，后端使用django提供数据接口的支持。

#### 2.项目优点

1. 完整性：有完整的前后台系统，自由管理数据

2. 稳定性：项目有异常处理机制，有比较完善的处理方案

   


#### 3.博客文章

- **Django学习：https://blog.csdn.net/qq_50792097/article/details/126565005** 
- **MySQL学习：https://blog.csdn.net/qq_50792097/article/details/126527104**



#### 4.测试产品

毕业设计管理系统：http://tdmin.fastcat.top/(未开放) 


#### 5.项目架构

**1.毕业设计管理系统**

```
WebServer--graduate            Django全栈系统
│  db.sqlite3
│  django-graduate.sql        sql文件
│  manage.py                 启动器
│  requirements.txt          依赖包
├─myhome                     应用程序代码
│  │  admin.py
│  │  apps.py
│  │  models.py             模型
│  │  __init__.py 
│  ├─middleware             中间件   
│  │     LoginCheckMiddleware.py        登录中间件
│  │     __init__.py 
│  ├─migrations             映射
│  │     __init__.py  
│  ├─routes                 自定义封装路由
│  │     IndexUrls.py
│  │     __init__.py 
│  ├─utils                  工具函数
│  │     func.py
│  │     __init__.py 
│  ├─views                  视图函数(类似于控制器)
│  │     AdminViews.py          封装Admin
│  │     IndexViews.py          封装Index
│  │     StudentViews.py        封装Student
│  │     TeacherViews.py        封装Teacher
│  │     __init__.py 
├─static                    公有访问静态资源文件
│  ├─assets                     保存的文件路径
│  │  └─file
│  │          1657051206.909655.jpg
│  │          1657065859.9794888.jpg
│  │          1657081535.9102411.jpg 
│  ├─css                       公有样式
│  │      comm.css 
│  ├─images                    公有图片
│  │      bg-login.png
│  │      bg-main.png
│  │      bg-white.png
│  │      logo.png
│  │      logo2.png
│  │      logo3.png  
│  ├─js                        公有js
│  │      index.js 
│  └─lib                       公有类库
│      ├─admin-assets 
│      ├─JQuery3.6.0 
│      └─layui-v2.6.8  
├─templates              模板视图
│  │  404error.html            404空页面
│  │  index.html               首页
│  │  login.html               登录页
│  │  register.html            注册页
│  ├─admin                     管理员相关页面
│  │      index.html
│  │      student_list.html
│  │      teacher_list.html
│  │      title_list.html 
│  ├─public                   公有页面
│  │      aside.html
│  │      header.html
│  │      script.html
│  │      style.html
│  │      theme.html 
│  ├─student                 学生相关页面
│  │      graduate_answer.html
│  │      graduate_article.html
│  │      group.html
│  │      index.html
│  │      middle_check.html
│  │      select_title.html
│  │      title_msg.html 
│  └─teacher                 教师相关页面
│          design_title.html
│          graduate_answer.html
│          graduate_article.html
│          group.html
│          index.html
│          middle_check.html
│          student_score.html
│          title_msg.html 
├─tests                    自定义测试文件夹
│      index.py 
├─web_template             模板文件
└─WebServer                项目配置项
    │  asgi.py
    │  settings.py            设置
    │  urls.py                路由入口 
    │  wsgi.py                项目启动
    └─  __init__.py 
```





#### 6.项目截图 

**1.毕业设计管理系统**

|                                                              |                                                              |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| ![输入图片说明](https://gitee.com/MiniWildCat/graduate-project/raw/master/%E9%A1%B9%E7%9B%AE%E5%B1%95%E7%A4%BA%E5%9B%BE%E7%89%87/登录页.jpg "屏幕截图.png") | ![输入图片说明](https://gitee.com/MiniWildCat/graduate-project/raw/master/%E9%A1%B9%E7%9B%AE%E5%B1%95%E7%A4%BA%E5%9B%BE%E7%89%87/注册页.jpg "屏幕截图.png") |
| ![输入图片说明](https://gitee.com/MiniWildCat/graduate-project/raw/master/%E9%A1%B9%E7%9B%AE%E5%B1%95%E7%A4%BA%E5%9B%BE%E7%89%87/管理员-首页.jpg "屏幕截图.png") | ![输入图片说明](https://gitee.com/MiniWildCat/graduate-project/raw/master/%E9%A1%B9%E7%9B%AE%E5%B1%95%E7%A4%BA%E5%9B%BE%E7%89%87/教师管理-教师列表.jpg "屏幕截图.png") |
| ![输入图片说明](https://gitee.com/MiniWildCat/graduate-project/raw/master/%E9%A1%B9%E7%9B%AE%E5%B1%95%E7%A4%BA%E5%9B%BE%E7%89%87/学生管理-学生列表.jpg "屏幕截图.png") | ![输入图片说明](https://gitee.com/MiniWildCat/graduate-project/raw/master/%E9%A1%B9%E7%9B%AE%E5%B1%95%E7%A4%BA%E5%9B%BE%E7%89%87/课题管理-课题列表.jpg "屏幕截图.png") |
| ![输入图片说明](https://gitee.com/MiniWildCat/graduate-project/raw/master/%E9%A1%B9%E7%9B%AE%E5%B1%95%E7%A4%BA%E5%9B%BE%E7%89%87/教师-首页.jpg "屏幕截图.png") | ![输入图片说明](https://gitee.com/MiniWildCat/graduate-project/raw/master/%E9%A1%B9%E7%9B%AE%E5%B1%95%E7%A4%BA%E5%9B%BE%E7%89%87/选题信息-设计开题.jpg "屏幕截图.png") |
| ![输入图片说明](https://gitee.com/MiniWildCat/graduate-project/raw/master/%E9%A1%B9%E7%9B%AE%E5%B1%95%E7%A4%BA%E5%9B%BE%E7%89%87/选题信息-设计开题2.jpg "屏幕截图.png") | ![输入图片说明](https://gitee.com/MiniWildCat/graduate-project/raw/master/%E9%A1%B9%E7%9B%AE%E5%B1%95%E7%A4%BA%E5%9B%BE%E7%89%87/选题信息-分组选择.jpg "屏幕截图.png") |
| ![输入图片说明](https://gitee.com/MiniWildCat/graduate-project/raw/master/%E9%A1%B9%E7%9B%AE%E5%B1%95%E7%A4%BA%E5%9B%BE%E7%89%87/毕业评分-学生成绩.jpg "屏幕截图.png") | ![输入图片说明](https://gitee.com/MiniWildCat/graduate-project/raw/master/%E9%A1%B9%E7%9B%AE%E5%B1%95%E7%A4%BA%E5%9B%BE%E7%89%87/小组任务-开题答辩.jpg "屏幕截图.png") |
| ![输入图片说明](https://gitee.com/MiniWildCat/graduate-project/raw/master/%E9%A1%B9%E7%9B%AE%E5%B1%95%E7%A4%BA%E5%9B%BE%E7%89%87/小组任务-中期检查.jpg "屏幕截图.png") | ![输入图片说明](https://gitee.com/MiniWildCat/graduate-project/raw/master/%E9%A1%B9%E7%9B%AE%E5%B1%95%E7%A4%BA%E5%9B%BE%E7%89%87/小组任务-毕业答辩.jpg "屏幕截图.png") |
| ![输入图片说明](https://gitee.com/MiniWildCat/graduate-project/raw/master/%E9%A1%B9%E7%9B%AE%E5%B1%95%E7%A4%BA%E5%9B%BE%E7%89%87/小组任务-论文查阅.jpg "屏幕截图.png") | ![输入图片说明](https://gitee.com/MiniWildCat/graduate-project/raw/master/%E9%A1%B9%E7%9B%AE%E5%B1%95%E7%A4%BA%E5%9B%BE%E7%89%87/学生-首页.jpg "屏幕截图.png") |
| ![输入图片说明](https://gitee.com/MiniWildCat/graduate-project/raw/master/%E9%A1%B9%E7%9B%AE%E5%B1%95%E7%A4%BA%E5%9B%BE%E7%89%87/选题信息-查看选题.jpg "屏幕截图.png") | ![输入图片说明](https://gitee.com/MiniWildCat/graduate-project/raw/master/%E9%A1%B9%E7%9B%AE%E5%B1%95%E7%A4%BA%E5%9B%BE%E7%89%87/选题信息-分组选择-1.jpg "屏幕截图.png") |

|                                                              |                                                              |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| ![输入图片说明](https://gitee.com/MiniWildCat/graduate-project/raw/master/%E9%A1%B9%E7%9B%AE%E5%B1%95%E7%A4%BA%E5%9B%BE%E7%89%87/毕业信息-开题信息.jpg "屏幕截图.png") | ![输入图片说明](https://gitee.com/MiniWildCat/graduate-project/raw/master/%E9%A1%B9%E7%9B%AE%E5%B1%95%E7%A4%BA%E5%9B%BE%E7%89%87/毕业信息-中期检查.jpg "屏幕截图.png") |
| ![输入图片说明](https://gitee.com/MiniWildCat/graduate-project/raw/master/%E9%A1%B9%E7%9B%AE%E5%B1%95%E7%A4%BA%E5%9B%BE%E7%89%87/毕业信息-毕业论文.jpg "屏幕截图.png") | ![输入图片说明](https://gitee.com/MiniWildCat/graduate-project/raw/master/%E9%A1%B9%E7%9B%AE%E5%B1%95%E7%A4%BA%E5%9B%BE%E7%89%87/毕业信息-毕业答辩.jpg "屏幕截图.png") |







### 二、项目安装


#### 1.开始使用

使用git拉取当前项目

```

git clone https://gitee.com/MiniWildCat/graduate-project.git

```

使用pip3 对 django系统安装包

```

django接口模板系统/毕业设计管理系统

pip install -r requirements.txt 

```

执行数据库反映射成模型

```

python manage.py inspectdb > myhome/models.py

```

运行项目

```
 
毕业设计管理系统
python manage.py runserver 8080

```

项目开启后，可以通过以下url访问

```

毕业设计管理系统
http://localhost:8080/  

```

默认帐号

```
管理员：admin123456
密码：123456

教师：teacher123456
密码：123456

学生：student123456
密码：123456
```


#### 2.使用说明

1. 项目的架构可以下载使用。
3. 经过本项目二次开发的项目，本项目不承担任何法律责任！！！



#### 3.开源许可 

毕业设计管理系统采用 [Apache 2.0](http://www.apache.org/licenses/) 开源许可证。

​                        
