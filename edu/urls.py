from django.conf.urls import url

from edu import views_import
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

    url(r'^edu/org_imports', views_import.org_imports, name='org_imports'),
    url(r'^edu/student_imports', views_import.student_imports, name='student_imports'),
    url(r'^edu/student_imports_detail/(?P<pk>\d+)/$', views_import.student_imports_detail, name='student_imports_detail'),

]