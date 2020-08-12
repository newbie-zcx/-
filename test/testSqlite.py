# -*- codding = utf-8 -*-


import sqlite3

conn = sqlite3.connect("test.db")       # 打开或创建数据库文件

print("Opened database successfully")

c = conn.cursor()       # 获取游标

sql = '''
    create table company
        (id int primary key not null,
        name text not null,
        age int not null,
        address char(50),
        salary real);
'''

c.execute(sql)          # 执行sql语句
conn.commit()           # 提交数据库操作
conn.close()            # 关闭数据库连接


print("Create table successfully")