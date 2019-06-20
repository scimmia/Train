import datetime
import json
import os
from decimal import Decimal

import xlrd
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
from django.shortcuts import render

from django.db.models import Aggregate, CharField

def get_query(request):
    kwargs = {}
    query = ''
    for key in request.GET.keys():
        value = request.GET[(key)]
        # 刨去其中的token和page选项
        if key != 'csrfmiddlewaretoken' and key != 'page' and (len(value) > 0):
            kwargs[key] = value
            query += '&' + key + '=' + value
    return kwargs, query


def get_paged_page(request, raw_data, list_template, context={}):
    kwargs, query = get_query(request)
    data = raw_data.filter(**kwargs)
    data_list, page_range, count, page_nums = pagination(request, data, 100)
    context['data'] = data_list
    context['query'] = query
    context['page_range'] = page_range
    context['count'] = count
    context['page_nums'] = page_nums
    return render(request, list_template, context)


# 分页函数
def pagination(request, queryset, display_amount=10, after_range_num=5, before_range_num=4):
    # 按参数分页

    try:
        # 从提交来的页面获得page的值
        page = int(request.GET.get("page", 1))
        # 如果page值小于1，那么默认为第一页
        if page < 1:
            page = 1
    # 若报异常，则page为第一页
    except ValueError:
        page = 1
    # 引用Paginator类
    paginator = Paginator(queryset, display_amount)
    # 总计的数据条目
    count = paginator.count
    # 合计页数
    num_pages = paginator.num_pages

    try:
        # 尝试获得分页列表
        objects = paginator.page(page)
    # 如果页数不存在
    except EmptyPage:
        # 获得最后一页
        objects = paginator.page(paginator.num_pages)
    # 如果不是一个整数
    except PageNotAnInteger:
        # 获得第一页
        objects = paginator.page(1)
    # 根据参数配置导航显示范围
    temp_range = paginator.page_range

    # 如果页面很小
    if (page - before_range_num) <= 0:
        # 如果总页面比after_range_num大，那么显示到after_range_num
        if temp_range[-1] > after_range_num:
            page_range = range(1, after_range_num + 1)
        # 否则显示当前页
        else:
            page_range = range(1, temp_range[-1] + 1)
    # 如果页面比较大
    elif (page + after_range_num) > temp_range[-1]:
        # 显示到最大页
        page_range = range(page - before_range_num, temp_range[-1] + 1)
    # 否则在before_range_num和after_range_num之间显示
    else:
        page_range = range(page - before_range_num + 1, page + after_range_num)
    # 返回分页相关参数
    return objects, page_range, count, num_pages


class GroupConcat(Aggregate):
    function = 'GROUP_CONCAT'
    template = '%(function)s(%(distinct)s%(expressions)s%(ordering)s%(separator)s)'

    def __init__(self, expression, distinct=False, ordering=None, separator=',', **extra):
        super(GroupConcat, self).__init__(
            expression,
            distinct='DISTINCT ' if distinct else '',
            ordering=' ORDER BY %s' % ordering if ordering is not None else '',
            separator=' SEPARATOR "%s"' % separator,
            output_field=CharField(),
            **extra)


class Concat(Aggregate):
    function = 'GROUP_CONCAT'
    template = '%(function)s(%(distinct)s%(expressions)s)'

    def __init__(self, expression, distinct=False, **extra):
        super(Concat, self).__init__(
            expression,
            distinct='DISTINCT ' if distinct else '',
            output_field=CharField(),
            **extra)

def save_uploaded_excel(f):
    path = '\\csvs\\'  # 上传文件的保存路径，可以自己指定任意的路径
    if not os.path.exists(path):
        os.makedirs(path)
    with open(path + 'tmp.xls', 'wb+')as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return xlrd.open_workbook(path + 'tmp.xls')
