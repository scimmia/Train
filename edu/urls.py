from django.conf.urls import url

from edu import views_import, views_school
from . import views

urlpatterns = [
    # url(r'^dashboard/', views.dashboard, name='dashboard'),

    # 用户登陆
    url(r'login/', views.login, name='login'),
    # 用户退出
    url(r'logout/', views.logout, name='logout'),
    # 密码修改
    url(r'^user/change_password', views.change_password, name='change_password'),
    url(r'^user/users/', views.user_list, name='user_list'),

    url(r'^school/school_dash', views_school.school_dash, name='school_dash'),
    url(r'^school/school_delete/(?P<pk>\d+)/$', views_school.school_delete, name='school_delete'),
    url(r'^school/school_detail/(?P<pk>\d+)/$', views_school.school_detail, name='school_detail'),

    url(r'^edu/org_imports', views_import.org_imports, name='org_imports'),
    url(r'^student_imports', views_import.student_imports, name='student_imports'),
    url(r'^student_import_delete/(?P<pk>\d+)$', views_import.student_import_delete, name='student_import_delete'),
    url(r'^student_import_detail/(?P<pk>\d+)/$', views_import.student_import_detail, name='student_import_detail'),

]