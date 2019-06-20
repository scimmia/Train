from django.forms import ModelForm
from django import forms

from edu.models import School


class UserCreatForm(forms.Form):
    username = forms.CharField(label="姓名", required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    loginname = forms.CharField(label="账号", required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))


class UserManageForm(forms.Form):
    operation = forms.ChoiceField(label="操作类型",
                                  choices=(
                                      (1, "重置密码"),
                                      (2, "启用"),
                                      (3, "停用"),
                                  ),
                                  widget=forms.RadioSelect,
                                  initial='1',
                                  )


class UserChangePasswordForm(forms.Form):
    old_password = forms.CharField(label="旧密码", required=True, widget=forms.PasswordInput(attrs={'autofocus': True}), )
    new_password = forms.CharField(label="新密码", required=True, widget=forms.PasswordInput(), )
    new_password_2 = forms.CharField(label="新密码确认", required=True, widget=forms.PasswordInput(), )


class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()

class ImportStudentForm(forms.Form):
    file = forms.FileField()