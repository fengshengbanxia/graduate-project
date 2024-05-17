import re
from django.http import JsonResponse
from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin

# 对请求进行拦截
class LoginCheckMiddleware(MiddlewareMixin):
  def process_request(self, request):
    # 允许登录的路由
    allow = [
      '/login',
      '/login/doLogin',
      '/register',
      '/register/doRegister',
      '/doLogout',
      '/',
    ]
    # 检验路由，和session
    route = request.path
    userinfo = request.session.get('userinfo',None)
    haveAuth = True if(userinfo) else False
    for item in allow:
      if route == item:
        haveAuth = True
    # 没有访问权限，则直接拦截，返回信息
    if not haveAuth:
        # return JsonResponse({'msg':'没有访问权限！请登录','code':403})
        return redirect('myhome_login')