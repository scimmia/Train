import os

import xlrd
from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import views
from django.contrib.auth.decorators import login_required
# Create your views here.
from edu import utils
from edu.models import City, Org
from .forms import UploadFileForm
from .forms import UserCreatForm, UserManageForm, UserChangePasswordForm


# 用户登陆
def login(request):
    template_response = views.login(request, extra_context={'next': '/t/dashboard/'})
    return template_response


# 用户退出
def logout(request):
    # logout_then_login表示退出即跳转至登陆页面，login_url为登陆页面的url地址
    template_response = views.logout_then_login(request, login_url='/t/login/')
    return template_response


@login_required
def user_list(request):
    form = UserCreatForm(request.POST or None)
    oper_form = UserManageForm(request.POST or None)
    context = {}
    if request.method == 'POST':
        if form.is_valid():
            oper_form = UserManageForm()
            loginname = form.cleaned_data.get('loginname')
            try:
                user = User.objects.create_user(loginname, None, 'abcd1111')
                user.last_name = form.cleaned_data.get('username')
                user.save()
                context['message'] = u'保存成功'
            except:
                context['errormsg'] = u'该用户已存在'
        elif oper_form.is_valid():
            form = UserCreatForm()
            operation = oper_form.cleaned_data.get('operation')
            ids = request.POST['ids']
            if len(ids) > 0:
                if operation == '1':
                    users = User.objects.filter(id__in=ids.split(','))
                    for u in users:
                        u.set_password('abcd1111')
                        u.save()
                    context['message'] = u'重置成功，密码为abcd1111'
                elif operation == '2':
                    User.objects.filter(id__in=ids.split(',')).update(is_active=True)
                    context['message'] = u'启用成功'
                    pass
                elif operation == '3':
                    User.objects.filter(id__in=ids.split(',')).update(is_active=False)
                    context['message'] = u'停用成功'
                    pass
            else:
                context['errormsg'] = u'请选择至少一个账号'

    context['form'] = form
    context['oper_form'] = oper_form
    raw_data = User.objects.filter(is_superuser=False)
    list_template = 'edu/user_list.html'
    return utils.get_paged_page(request, raw_data, list_template, context)


# 密码更改
@login_required
def change_password(request):
    form = UserChangePasswordForm(request.POST or None)
    context = {
        'form': form,
    }
    if request.method == 'POST':
        if form.is_valid():
            u = request.user
            if u.check_password(form.cleaned_data.get('old_password')):
                password1 = form.cleaned_data.get('new_password')
                password2 = form.cleaned_data.get('new_password_2')
                if password1 and password2 and len(password1)>0 and password1 == password2:
                    u.set_password(password1)
                    u.save()
                    context['message'] = u'修改成功'
                else:
                    context['errormsg'] = u'新密码不一致或错误'

            else:
                context['errormsg'] = u'旧密码错误'

    return render(request, 'edu/user_change_password.html', context)


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


