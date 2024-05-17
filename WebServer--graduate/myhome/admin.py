from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register([Admin, AuthGroup, AuthGroupPermissions, AuthPermission, AuthUser])

admin.site.register([DjangoSession, Student, StudentGraduateArticle, StudentGroup])

admin.site.register([StudentGraduateAnswer, AuthUserGroups, AuthUserUserPermissions])

admin.site.register([DjangoAdminLog, DjangoContentType, DjangoMigrations])

admin.site.register([StudentMiddleCheck, StudentSelectTitle, StudentTitleMsg, Teacher, TeacherGroup])