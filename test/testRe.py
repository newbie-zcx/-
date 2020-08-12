

# 正则表达式：字符串模式

# import re
#
# pat = re.compile("zcx-")
# m = pat.search("vvvzcx-zcxzzz")
# print(m)


import xlwt

workbook = xlwt.Workbook(encoding="utf-8")          # 创建workbook对象
worksheet = workbook.add_sheet('测试创建表格')
worksheet.write(0, 0, '测试一行一列')
workbook.save('ceshi.xls')