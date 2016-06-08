import os
import xlsxwriter
import calendar
import configparser
import random
import argparse
import re
import sys
from __init__ import __version__

conf = configparser.ConfigParser()
conf.read('F:/python/mytool/work_overtime/conf/genxml.ini')

def genWorkTime(sublist):
    randnum = random.randrange(0,59)

    if randnum < 10:
        minut = '0' + str(randnum)
    else:
        minut = str(randnum)

    if sublist[1] == 5:
        start_time = '8:30'
        end_time = '19:' + minut
    else:
        start_time = '18:30'
        end_time = '21:' + minut

    workdatetime = start_time + '-' + end_time
    sublist[4] = workdatetime

    return sublist


def filterContent(initlist):
    holiday_list = []
    extent_work_list = []
    result_list = []
    last_saturday = []
    del_list = []

    for key in conf['holiday']:
        holiday_list.append(conf['holiday'][key])

    for key in conf['extent_work']:
        extent_work_list.append(conf['extent_work'][key])
    
    for item in initlist:
        if item[0] in holiday_list or item[0] in extent_work_list or item[1] == 2 or item[1] == 6:
            del_list.append(item)
        
        if item[1] == 5:
            last_saturday.append(item)

    for item in del_list:
        initlist.remove(item)

    for item in initlist:
        if item[1] == 5:
            item[5] = 40.00
        else:
            item[5] = 20.00
        
        item = genWorkTime(item)
        result_list.append(item)

    result_list.remove(last_saturday.pop())

    return result_list

def fillContent(worksheet,bold,year,month,sheetflag,money=0.0):
    row = 0
    col = 0
    datelist = []
    all_date_list = []
    content = []
    name = conf['userinfo']['name']
    myid = conf['userinfo']['id']
    depart = conf['userinfo']['department']
    mastername = conf['userinfo']['master']
    total_money = 0

    if sheetflag == 'sheet1':
        head = ['姓名','员工号','合计']
        for item in head:
            worksheet.write(row,col,item,bold)
            col += 1
        
        row += 1
        col = 0
        worksheet.write(row,col,name)
        worksheet.write(row,col + 1,myid)
        worksheet.write(row,col + 2,money)
        return
    else:
        head = ['姓名','员工','部门','加班日期','加班时间','报销金额（元）','审批主管']

        for l in calendar.monthcalendar(year,month):
            datelist += [x for x in l if x != 0]

        for item in datelist:
            initlist = []
            #date FORMAT:YYYY/MM/DD
            initlist.append(str(year) + '/' + str(month) + '/' + str(item))
            #week
            initlist.append(calendar.weekday(year,month,item))
            #holiday
            initlist.append(1)
            #extent work
            initlist.append(1)
            #datetime
            initlist.append('08:30')
            #money
            initlist.append(0.00)

            all_date_list.append(initlist)

        content = filterContent(all_date_list)

        for item in (head):
            worksheet.write(row,col,item,bold)
            col += 1

        row += 1
        col = 0

        for tmplist in content: 
            worksheet.write(row,col,name)
            worksheet.write(row,col + 1,myid)
            worksheet.write(row,col + 2,depart)
            worksheet.write(row,col + 3,tmplist[0])
            worksheet.write(row,col + 4,tmplist[4])
            worksheet.write(row,col + 5,tmplist[5])
            worksheet.write(row,col + 6,mastername)
            total_money += tmplist[5]
            row += 1
        
        return total_money
    
def createXslFile(filename,year,month):
    sheet1_name = '合计'
    sheet2_name = '明细'
    total_money = 0.0

    #delete the file.
    if os.path.exists(filename):
        os.remove(filename)

    # Create a workbook and add a worksheet.
    workbook = xlsxwriter.Workbook(filename)
    worksheet = workbook.add_worksheet(sheet1_name)
    worksheet2 = workbook.add_worksheet(sheet2_name)
    bold = workbook.add_format({'bold': True})

    #Fill in the content of the sheets.
    total_money = fillContent(worksheet=worksheet2,bold=bold,year=year,month=month,sheetflag='sheet2')
    fillContent(worksheet=worksheet,bold=bold,year=year,month=month,sheetflag='sheet1',money=total_money)

    print('[SUCCESSFUL]:The file name is %s'%filename)
    workbook.close()

def get_parser():
    parser = argparse.ArgumentParser(description='general xlsx file for work orver time .')
    parser.add_argument('-d', '--datetime', type=str, help='specify the datetime FORMAT:YYYY-MM \nfor example:2016-06')
    parser.add_argument('-v', '--version', help='displays the current version of generate xlsx file.',action='store_true')
    return parser

def command_line_runner():
    parser = get_parser()
    args = vars(parser.parse_args())
    prog = re.compile('^[0-9]{4}-[0-9]{2}$')

    if args['version']:
        print(__version__)
        return

    if prog.match(args['datetime']) != None:
        str_datetime = args['datetime']
        year = str_datetime[0:str_datetime.find('-')]
        month = str_datetime[str_datetime.find('-') + 1:]

        if month not in ('01','02','03','04','05','06','07','08','09','10','11','12'):
            print('The argument of month is illegal !')
            sys.exit(1)
    else:
        print('The argument of datetime\'s format is illegal !\nThe FORMAT is: YYYY-MM')
        sys.exit(1)

    workpath = 'E:/公司相关/加班餐补/' + year
    filename = '加班餐补申请表' + month + '月份.xlsx'

    if os.path.isdir(workpath):
        os.chdir(workpath)
    else:
        print('The work dir is not exist !')
        sys.exit(1)

    createXslFile(filename,int(year),int(month))

if __name__ == '__main__':
    command_line_runner()
