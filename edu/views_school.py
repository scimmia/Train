import os
from datetime import datetime

import xlrd
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import views
from django.contrib.auth.decorators import login_required
# Create your views here.
from xlrd import xldate_as_tuple

from edu import utils
from edu.models import City, Org, Student, School, Import_Summary
from .forms import UploadFileForm, ImportStudentForm, SchoolForm
from .forms import UserCreatForm, UserManageForm, UserChangePasswordForm

def school_dash(request):
    form = SchoolForm(request.POST or None)
    context = {
        'form': form,
    }
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            context['message'] = u'保存成功'
    data = School.objects.all().order_by('-begin_date')

    return utils.get_paged_page(request, data, 'edu/school_dash.html', context)

def school_delete(request, pk):
    School.objects.filter(pk=pk).delete()
    return redirect('school_dash')

    # return render(request, 'edu/school_dash.html', locals())

def school_detail(request, pk):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)  # 注意获取数据的方式
        if form.is_valid():
            book = utils.save_uploaded_excel(request.FILES['file'])
            print("The number of worksheets is {0}".format(book.nsheets))
            print("Worksheet name(s): {0}".format(book.sheet_names()))
            sh = book.sheet_by_index(2)
            print("{0} {1} {2}".format(sh.name, sh.nrows, sh.ncols))
            studentImports = []
            instance = Import_Summary()
            instance.remarks = form.cleaned_data.get('remarks')
            instance.education_id = pk
            instance.save()
            for rx in range(sh.nrows):
                row = (sh.row_values(rx))
                if isinstance(row[0], float):
                    s = Student()
                    s.inport_info_id = instance.pk
                    s.company = row[1]
                    s.name = row[2]
                    s.sex = row[3]
                    s.nation = row[4]
                    ctype = sh.cell(rx, 5).ctype
                    temp = row[5]
                    if ctype == 3:
                        date = datetime(*xldate_as_tuple(temp, 0))
                        s.birth = date.strftime('%Y.%d')
                    elif ctype == 2:
                        if temp > 3000:
                            temp = temp / 100
                        if temp > 3000:
                            temp = temp / 100
                        s.birth = ('%.2f' % temp)
                    else:
                        s.birth = row[5]
                    s.party = row[6]
                    s.job = row[7]
                    if isinstance(row[0], float):
                        s.phone = str(int(row[8]))
                    else:
                        s.phone = str(row[8])
                    s.remarks = row[9]
                    s.school = instance.education
                    try:
                        s.org = Org.objects.get(
                            name=s.company.replace("农", "").replace("商", "").replace("银", "").replace("行", ""))
                    except:
                        pass
                    # s.save()
                    studentImports.append(s)
            if len(studentImports) > 0:
                Student.objects.bulk_create(studentImports)
                instance.data_count = len(studentImports)
                instance.save()
            return redirect('student_import_detail', instance.id)
    raw_data = Import_Summary.objects.filter(education_id=pk).order_by('-pub_date')
    form = UploadFileForm()
    context = {
        'form': form,
    }
    return utils.get_paged_page(request, raw_data, 'edu/student_imports.html', context)


