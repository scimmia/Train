from io import BytesIO

import xlrd
import xlsxwriter
from django.test import TestCase

# Create your tests here.

def classes_format():
    list1 = ['晨曦', '晨光', '曙光', '朝阳', '旭日']
    x_io = BytesIO()
    # work_book = xlsxwriter.Workbook(x_io)
    work_book = xlsxwriter.Workbook('h:\\0625-format.xlsx')
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
    book = xlrd.open_workbook('h:\\0625.xls')
    sheets = book.sheets()
    for sheet in sheets:
        name = sheet.name
        print(sheet.name)
        if name in list1:
            ws = work_book.add_worksheet(name)
            ws.default_row_height = 20
            ws.set_column(0,1, 18,normal_format)
            ws.set_column(2,2, 32,normal_format)
            ws.set_column(3,3, 18,normal_format)
            ws.set_column(4,4, 24,normal_format)
            ws.set_column(5,5, 18,normal_format)
            for rx in range(sheet.nrows):
                row = (sheet.row_values(rx))
                ws.write_row(rx, 0, row)
        elif name in ['刘建光', '班主任']:
            continue
        else:
            ws = work_book.add_worksheet(name)
            ws.default_row_height = 20
            ws.default_row_height = 20
            # ws.set_column(0,4, 14)
            ws.set_column(0,4, 14,normal_format)
            for rx in range(sheet.nrows):
                row = (sheet.row_values(rx))
                ws.write_row(rx, 0, row)

    work_book.close()

classes_format()