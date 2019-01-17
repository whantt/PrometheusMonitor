#!/usr/bin/python
#coding=utf-8

import psycopg2
import psycopg2.extras
import xlsxwriter
import sys
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header

defaultencoding = 'utf-8'
if sys.getdefaultencoding() != defaultencoding:
    reload(sys)
    sys.setdefaultencoding(defaultencoding)

name = 'report' + time.strftime('%Y%m%d',time.localtime(time.time())) + '.xls'


def getDbResult():
    conn = psycopg2.connect(host="172.16.24.196", port=5432, user="postgres", password="postgres", database="promethues")
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    sql = "select content , count(*) from pending_messages where create_time > now() -interval '7 day' group by content order by 2 desc;"
    cur.execute(sql)
    _list = cur.fetchall()
    conn.close()
    return _list

rs = getDbResult()
title = [u'告警内容',u'数量']
buname = []
data = [
]

for info in rs:
    countlist = []
    buname.append(info[0])
    countlist.append(info[1])
    data.append(countlist)

# 创建一个excel文件
workbook = xlsxwriter.Workbook(name)
# 创建一个工作表对象,sheet栏
worksheet = workbook.add_worksheet('综合统计') #u'数据报表'
# 创建一个图表对象 type:colum(柱状图)
chart = workbook.add_chart({'type': 'column'})

worksheet.set_row(1, 20)
worksheet.set_column('A:A', 50)

# 定义format格式对象
format = workbook.add_format()
# 定义format对象单元格边框加粗(1像素)的格式
format.set_border(1)
format.set_size(15)

# 定义format_title格式对象
format_title = workbook.add_format()
format_title.set_border(1)
# 定义format_title对象单元格背景颜色
format_title.set_bg_color('#cccccc')

# 定义format_ave单元格式
format_ave = workbook.add_format()
format_ave.set_border(1)
# 定义format_ave对象单元格数字显示格式(小数点后2位)
format_ave.set_num_format('0.00')

for i in range(0,len(data)):
    worksheet.set_row(i+2, 20)
    worksheet.write_row('B'+str(i+2), data[i], format)

# 将数据,信息写入xls文件
#以行的方式写
worksheet.write_row('A1', title, format_title)
worksheet.write_column('A2', buname, format)


# 定义图表数据系列函数
def chart_series(cur_row):
    '''
    绘制柱状图
    :param cur_row:行号String类型
    :return:
    '''

    x = 2+len(data)
    worksheet.write_formula('B'+str(x), '=SUM(B2'+':B' + str(x-1) + ')', format_ave)
    worksheet.write_column('A' + str(x), [u'合计'], format)
    # 画图
    chart.add_series({
        'categories': '=综合统计!$B$1:$B$1',  # 将"星期一至星期日"作为图表数据标签(X轴)
        'values': '=综合统计!$B$'+cur_row+':$B$'+cur_row,  # 频道一周所有数据作为数据区域
        'line': {'color': 'black'},  # 线条颜色定义为black
        'name': '=综合统计!$A$'+cur_row  #引用业务名称为图例项
    })

# 数据以2-6行进行图表数据系列函数
for row in range(2, 2+len(data)):
    chart_series(str(row))


# 设置图表大小
chart.set_size({'width': 677, 'height': 387})
# 设置标题
chart.set_title({'name': u'告警统计报表'})

#将图表插入在D3单元格
worksheet.insert_chart('D2', chart)

# 创建一个图表对象
chart = workbook.add_chart({'type': 'pie'})


chart.add_series({
        'name': u'告警占比展示',
        'categories': '=综合统计!$A$2:$A$' + str(1+len(data)),
        'values':     '=综合统计!$B$2:$B$' + str(1+len(data)),
        'points':[
            {'fill': {'color': '#00CD00'}},
            {'fill': {'color': 'red'}},
            {'fill': {'color': 'yellow'}},
            {'fill': {'color': 'gray'}},
                  ],
    })
chart.set_style(2)
# 设置标题
chart.set_title({'name': u'告警占比展示'})
chart.set_size({'width': 677, 'height': 387})
#将图表插入在A8单元格
worksheet.insert_chart('D18', chart, {'x_offset': 0, 'y_offset': 0})
# 关闭xls
workbook.close()

def sendmail():
    sender = 'wml@com.cn'
    receivers = ['wml@com.cn', 'x@com.cn']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

    #创建一个带附件的实例
    message = MIMEMultipart()
    message['From'] = Header("wml@com.cn", 'utf-8')
    message['To'] =  Header("SIPCLOUD告警统计", 'utf-8')
    subject = 'SIPCLOUD告警统计'
    message['Subject'] = Header(subject, 'utf-8')

    #邮件正文内容
    message.attach(MIMEText('本周告警统计在附件中,请查看', 'plain', 'utf-8'))

    # 构造附件1，传送当前目录下的 test.txt 文件
    att1 = MIMEText(open(name, 'rb').read(), 'base64', 'utf-8')
    att1["Content-Type"] = 'application/octet-stream'
    # 这里的filename可以任意写，写什么名字，邮件中显示什么名字
    att1["Content-Disposition"] = 'attachment; filename=' + name
    message.attach(att1)

    try:
        smtp = smtplib.SMTP()
        smtp.connect('smtp.ti-net.com.cn')
        smtp.login('wml@com.cn', '')
        smtp.sendmail(sender, receivers, message.as_string())
        smtp.quit()
        print "邮件发送成功"
    except smtplib.SMTPException:
        print "Error: 无法发送邮件"

sendmail()

