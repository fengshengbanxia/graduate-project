from django.contrib.auth.hashers import make_password,check_password


pas = '123456'
test = make_password(pas,None,'pbkdf2_sha256')#   13 + 75 = 88，  密码加密

print("加密的数据",test)
# res = check_password(pas,test)    # 验证密码   返回结果
# print("匹配结果是",res)
