import os
from datetime import datetime

import xlrd
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import views
from django.contrib.auth.decorators import login_required
# Create your views here.
from xlrd import xldate_as_tuple

from edu import utils
from edu.models import City, Org, Student, School, Import_Summary
from .forms import UploadFileForm, ImportStudentForm
from .forms import UserCreatForm, UserManageForm, UserChangePasswordForm

def org_imports(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)  # 注意获取数据的方式
        if form.is_valid():
            book = utils.save_uploaded_excel(request.FILES['file'])
            print("The number of worksheets is {0}".format(book.nsheets))
            print("Worksheet name(s): {0}".format(book.sheet_names()))
            sh = book.sheet_by_index(0)
            print("{0} {1} {2}".format(sh.name, sh.nrows, sh.ncols))
            currentCity = ''
            orgs = []
            for rx in range(sh.nrows):
                row = (sh.row_values(rx))
                city = row[0]
                fa = row[1]
                if city != '':
                    currentCity = City()
                    currentCity.name = city
                    currentCity.save()
                org = Org()
                org.name = fa
                org.city = currentCity
                orgs.append(org)
            if len(orgs) > 0:
                Org.objects.bulk_create(orgs)
            return HttpResponse("Hello, world. You're at the polls index.")
    else:
        form = UploadFileForm()
    return render(request, 'edu/org_imports.html', {'form': form})

def student_imports(request):
    if request.method == 'POST':
        form = ImportStudentForm(request.POST, request.FILES)  # 注意获取数据的方式
        if form.is_valid():
            instance = form.save(commit=False)
            book = utils.save_uploaded_excel(request.FILES['file'])
            print("The number of worksheets is {0}".format(book.nsheets))
            print("Worksheet name(s): {0}".format(book.sheet_names()))
            sh = book.sheet_by_index(0)
            print("{0} {1} {2}".format(sh.name, sh.nrows, sh.ncols))
            studentImports = []
            instance.save()
            for rx in range(sh.nrows):
                row = (sh.row_values(rx))
                if isinstance(row[0],float):
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
                        s.org = Org.objects.get(name=s.company.replace("农", "").replace("商", "").replace("银", "").replace("行", ""))
                    except:
                        pass
                    # s.save()
                    studentImports.append(s)
            if len(studentImports) > 0:
                Student.objects.bulk_create(studentImports)
                instance.data_count = len(studentImports)
                instance.save()
            return redirect('student_import_detail', instance.id)
    raw_data = Import_Summary.objects.all().order_by('-pub_date')

    form = ImportStudentForm()
    context = {
        'form': form,
    }
    return utils.get_paged_page(request, raw_data, 'edu/student_imports.html', context)

def student_import_delete(request, pk):
    Import_Summary.objects.filter(pk=pk).delete()
    if 'fromurl' in request.GET.keys():
        return HttpResponseRedirect(request.GET['fromurl'])
    return redirect('student_imports')

def student_import_detail(request, pk):
    info = Import_Summary.objects.get(pk=pk)
    if request.method == "POST":
        ids = request.POST['ids']
        if len(ids) > 0:
            dele = Student.objects.filter(id__in=ids.split(',')).delete()
            info.data_count = info.data_count - dele[0]
            info.save()
            message = u'删除成功'
        else:
            message = u'请选择至少一条数据'
    data = Student.objects.filter(inport_info=pk).order_by('org')

    return render(request, 'edu/student_import_detail.html', locals())
