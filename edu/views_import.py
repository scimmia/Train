import os

import xlrd
from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import views
from django.contrib.auth.decorators import login_required
# Create your views here.
from edu import utils
from edu.models import City, Org, Student, School
from .forms import UploadFileForm
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
                org.save()

            return HttpResponse("Hello, world. You're at the polls index.")
    else:
        form = UploadFileForm()
    return render(request, 'edu/org_imports.html', {'form': form})

def student_imports(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)  # 注意获取数据的方式
        if form.is_valid():
            book = utils.save_uploaded_excel(request.FILES['file'])
            print("The number of worksheets is {0}".format(book.nsheets))
            print("Worksheet name(s): {0}".format(book.sheet_names()))
            sh = book.sheet_by_index(2)
            print("{0} {1} {2}".format(sh.name, sh.nrows, sh.ncols))
            studentImports = []

            for rx in range(sh.nrows):
                row = (sh.row_values(rx))
                if isinstance(row[0],float):
                    s = Student()
                    s.name = row[2]
                    s.sex = row[3]
                    s.nation = row[4]
                    s.birth = row[5]
                    s.party = row[6]
                    s.job = row[7]
                    if isinstance(row[0], float):
                        s.phone = str(int(row[8]))
                    else:
                        s.phone = str(row[8])
                    s.remarks = row[9]
                    try:
                        s.org = Org.objects.get(name=row[1].replace("农", "").replace("商", "").replace("银", "").replace("行", ""))
                    except:
                        pass
                    studentImports.append(s)
            if len(studentImports) > 0:
                Student.objects.bulk_create(studentImports)
            return HttpResponse("Hello, world. You're at the polls index.")
    else:
        form = UploadFileForm()
    return render(request, 'edu/student_imports.html',
                  {'form': form,
                   })
@login_required
def ticket_import_detail(request, pk):
    info = Ticket_Import.objects.get(pk=pk)
    data = Ticket_Import_Detail.objects.filter(inport_info=pk)
    if request.method == "POST":
        if info.is_saved:
            message = u'已保存'
        else:
            message = u'保存成功'
            data.update(saved=True)
            tickets = []
            for item in data:
                m = Ticket()
                m.t_type = item.t_type
                m.qianpaipiaohao = item.qianpaipiaohao
                m.piaohao = item.piaohao
                m.chupiaohang = item.chupiaohang
                m.chupiaoriqi = item.chupiaoriqi
                m.daoqiriqi = item.daoqiriqi
                m.piaomianjiage = item.piaomianjiage
                m.gourujiage = item.gourujiage
                m.paytime = item.paytime
                m.gongyingshang = item.gongyingshang
                m.pay_status = item.pay_status
                m.maichuriqi = item.maichuriqi
                m.maichujiage = item.maichujiage
                m.maipiaoren = item.maipiaoren
                m.sell_status = item.sell_status
                m.selltime = item.selltime
                m.selltime = item.selltime
                # 入库
                if info.import_type == 1:
                    m.t_status = 1
                    pass
                # 入池
                elif info.import_type == 2:
                    m.t_status = 5
                    m.pool_in = info.pool
                    pass
                # 开票
                elif info.import_type == 3:
                    pass
                tickets.append(m)
                pass
            if len(tickets) > 0:
                Ticket.objects.bulk_create(tickets)
            info.is_saved = True
            info.save()

    list_template = 'ticket/ticket_import_detail.html'
    return render(request, 'ticket/ticket_import_detail.html', locals())
