import os
from datetime import datetime
from io import BytesIO

import xlrd
import xlsxwriter
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

    return utils.get_paged_page(request, data, 'edu/school_list.html', context)

def school_list(request):
    form = SchoolForm(request.POST or None)
    context = {
        'form': form,
    }
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            context['message'] = u'保存成功'
    data = School.objects.all().order_by('-begin_date')

    return utils.get_paged_page(request, data, 'edu/school_list.html', context)

def school_delete(request, pk):
    School.objects.filter(pk=pk).delete()
    return redirect('school_dash')

# def school_export(request, pk):
#     datas = Student.objects.filter(school_id=pk).order_by('company', 'sex')
#     list = [[[], [], [], []], [[], [], [], []], [[], [], [], []], [[], [], [], []],[[], [], [], []]]
#     cities = {}
#     for index,data in enumerate(datas):
#         i = index % 20
#         list[i % 5][int(i/5)].append(data)
#         org = data.org_id
#         city = data.org.city_id
#         if not city in cities:
#             cities[city] = {'all':0}
#         if not org in cities[city]:
#             cities[city][org] = 0
#         cities[city][org] = cities[city][org]+1
#         cities[city]['all'] = cities[city]['all']+1
#
#     list1 = ['晨曦', '晨光', '曙光', '朝阳','旭日']
#     x_io = BytesIO()
#     work_book = xlsxwriter.Workbook(x_io)
#     head_format = work_book.add_format({
#         'font_size': '16',
#         'bold': 1,
#         'border': 1,
#         'align': 'center',
#         'valign': 'vcenter', })
#     merge_format = work_book.add_format({
#         'font_size': '12',
#         'bold': 1,
#         'border': 1,
#         'align': 'center',
#         'valign': 'vcenter', })
#     normal_format = work_book.add_format({
#         'font_size': '12',
#         'border': 1,
#         'align': 'center',
#         'valign': 'vcenter', })
#     for index, data in enumerate(list):
#         ws = work_book.add_worksheet(list1[index])
#         ws.default_row_height = 20
#         ws.set_row(0,50)
#         ws.set_column('A:A', 5)
#         ws.set_column('B:B', 15)
#         ws.set_column('C:C', 9)
#         ws.set_column('D:D', 6)
#         ws.set_column('E:E', 16)
#         ws.set_column('F:F', 19)
#         ws.set_column('G:G', 19)
#         ws.merge_range('A1:G1', '经营网点转型发展业务骨干培训班%s班学员名单' % (list1[index]), head_format)
#         ws.write('A2','序号',merge_format)
#         ws.write('B2','单位',merge_format)
#         ws.write('C2','姓名',merge_format)
#         ws.write('D2','性别',merge_format)
#         ws.write('E2','职务',merge_format)
#         ws.write('F2','手机',merge_format)
#         ws.write('G2','签到',merge_format)
#         i = 1
#         for temp in data:
#             for t in temp:
#                 ws.write(i+1, 0, i ,normal_format)
#                 ws.write(i+1, 1, t.company ,normal_format)
#                 ws.write(i+1, 2, t.name ,normal_format)
#                 ws.write(i+1, 3, t.sex ,normal_format)
#                 ws.write(i+1, 4, t.job ,normal_format)
#                 ws.write(i+1, 5, t.phone ,normal_format)
#                 ws.write(i+1, 6, '' ,normal_format)
#                 i = i+1
#
#     ws = work_book.add_worksheet('按地市汇总')
#     ws.default_row_height = 20
#     ws.set_column('A:D', 12)
#     m = 0
#     for keyT, valueT in cities.items():
#         n = 0
#         for key, value in valueT.items():
#             if key == 'all':
#                 continue
#             if n == 0:
#                 size = len(valueT)
#                 if size > 2:
#                     a = 'A%d:A%d' % (m+1,m+size-1)
#                     b = 'B%d:B%d' % (m+1,m+size-1)
#                     ws.merge_range(a, keyT, normal_format)
#                     ws.merge_range(b, valueT['all'], normal_format)
#                 else:
#                     ws.write(m, 0, keyT ,normal_format)
#                     ws.write(m, 1, valueT['all'] ,normal_format)
#             ws.write(m, 2, key ,normal_format)
#             ws.write(m, 3, value ,normal_format)
#             m = m + 1
#             n = n + 1
#     work_book.close()
#     res = HttpResponse()
#     res["Content-Type"] = "application/octet-stream"
#     res["Content-Disposition"] = 'filename="userinfos.xlsx"'
#     res.write(x_io.getvalue())
#     return res
#
#     # return render(request, 'edu/school_list.html', locals())

def school_export(request, pk):
    datas = Student.objects.filter(school_id=pk).order_by('org__city','org','sex')
    list1 = ['晨曦', '晨光', '曙光', '朝阳','旭日']
    list2 = ['A组', 'B组', 'C组', 'D组']

    x_io = BytesIO()
    work_book = xlsxwriter.Workbook(x_io)
    head_format = work_book.add_format({
        'font_size': '16',
        'bold': 1,
        'border': 1,
        'align': 'center',
        'valign': 'vcenter', })
    merge_format = work_book.add_format({
        'font_size': '12',
        'bold': 1,
        'border': 1,
        'align': 'center',
        'valign': 'vcenter', })
    normal_format = work_book.add_format({
        'font_size': '12',
        'border': 1,
        'align': 'center',
        'valign': 'vcenter', })
    ws = work_book.add_worksheet('全部')
    ws.default_row_height = 20
    ws.set_row(0, 50)
    ws.set_column('A:A', 5)
    ws.set_column('C:C', 15)
    ws.set_column('D:D', 9)
    ws.set_column('E:E', 6)
    ws.set_column('F:F', 19)
    ws.set_column('G:G', 19)
    ws.merge_range('A1:J1', '经营网点转型发展业务骨干培训班学员名单', head_format)
    temp = []
    temp.append('序号')
    temp.append('地市')
    temp.append('单位')
    temp.append('姓名')
    temp.append('性别')
    temp.append('职务')
    temp.append('手机')
    temp.append('签到')
    temp.append('班级')
    temp.append('分组')
    ws.write_row(1,0,temp,merge_format)
    for j,t in enumerate(datas):
        theindex = j % 20
        theClass = theindex%5
        theGroup = int(theindex/5)
        i = j+1
        temp = []
        temp.append(i)
        temp.append(t.org.city.name)
        temp.append(t.company)
        temp.append(t.name)
        temp.append(t.sex)
        temp.append(t.job)
        temp.append(t.phone)
        temp.append('')
        temp.append(list1[theClass])
        temp.append(list2[theGroup])
        ws.write_row(i+1,0,temp,normal_format)


    list = [[[], [], [], []], [[], [], [], []], [[], [], [], []], [[], [], [], []], [[], [], [], []]]
    cities = {}

    for index, data in enumerate(datas):
        i = index % 20
        list[i % 5][int(i / 5)].append(data)
        org = data.org_id
        city = data.org.city_id
        if not city in cities:
            cities[city] = {'all': 0}
        if not org in cities[city]:
            cities[city][org] = 0
        cities[city][org] = cities[city][org] + 1
        cities[city]['all'] = cities[city]['all'] + 1

    for index, data in enumerate(list):
        ws = work_book.add_worksheet(list1[index])
        ws.default_row_height = 20
        ws.set_row(0, 50)
        ws.set_column('A:A', 5)
        ws.set_column('B:B', 15)
        ws.set_column('C:C', 9)
        ws.set_column('D:D', 6)
        ws.set_column('E:E', 16)
        ws.set_column('F:F', 19)
        ws.set_column('G:G', 19)
        ws.merge_range('A1:G1', '经营网点转型发展业务骨干培训班%s班学员名单' % (list1[index]), head_format)
        ws.write('A2', '序号', merge_format)
        ws.write('B2', '单位', merge_format)
        ws.write('C2', '姓名', merge_format)
        ws.write('D2', '性别', merge_format)
        ws.write('E2', '职务', merge_format)
        ws.write('F2', '手机', merge_format)
        ws.write('G2', '签到', merge_format)
        i = 1
        for temp in data:
            for t in temp:
                ws.write(i + 1, 0, i, normal_format)
                ws.write(i + 1, 1, t.company, normal_format)
                ws.write(i + 1, 2, t.name, normal_format)
                ws.write(i + 1, 3, t.sex, normal_format)
                ws.write(i + 1, 4, t.job, normal_format)
                ws.write(i + 1, 5, t.phone, normal_format)
                ws.write(i + 1, 6, '', normal_format)
                i = i + 1

    ws = work_book.add_worksheet('按地市汇总')
    ws.default_row_height = 20
    ws.set_column('A:D', 12)
    m = 0
    for keyT, valueT in cities.items():
        n = 0
        for key, value in valueT.items():
            if key == 'all':
                continue
            if n == 0:
                size = len(valueT)
                if size > 2:
                    a = 'A%d:A%d' % (m + 1, m + size - 1)
                    b = 'B%d:B%d' % (m + 1, m + size - 1)
                    ws.merge_range(a, keyT, normal_format)
                    ws.merge_range(b, valueT['all'], normal_format)
                else:
                    ws.write(m, 0, keyT, normal_format)
                    ws.write(m, 1, valueT['all'], normal_format)
            ws.write(m, 2, key, normal_format)
            ws.write(m, 3, value, normal_format)
            m = m + 1
            n = n + 1
    work_book.close()
    res = HttpResponse()
    res["Content-Type"] = "application/octet-stream"
    res["Content-Disposition"] = 'filename="userinfos.xlsx"'
    res.write(x_io.getvalue())
    return res

    # return render(request, 'edu/school_list.html', locals())

def school_detail(request, pk):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)  # 注意获取数据的方式
        if form.is_valid():
            book = utils.save_uploaded_excel(request.FILES['file'])
            print("The number of worksheets is {0}".format(book.nsheets))
            print("Worksheet name(s): {0}".format(book.sheet_names()))
            sh = book.sheet_by_index(0)
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
        'pk': pk,
    }
    return utils.get_paged_page(request, raw_data, 'edu/student_imports.html', context)


