# -*- codding = utf-8 -*-

from bs4 import BeautifulSoup  # 网页解析
import re  # 正则表达式，进行文字匹配的
import urllib.request, urllib.error  # 制定URL，获取网页数据
import xlwt  # 进行excel操作
import sqlite3  # 进行数据库操作


# 主方法
def main():
    baseurl = "https://movie.douban.com/top250?start="
    datalist = getData(baseurl)

    savePath = "豆瓣电影TOP250.xls"
    saveData(datalist, savePath)

    dbPath = "movieTop250.db"
    saveDataToDB(datalist, dbPath)


# 解析网页
findLink = re.compile(r'<a href="(.*?)">')
findImgSrc = re.compile(r'<img.*src="(.*?)"', re.S)  # re.S让换行符包含在字符中
findTitle = re.compile(r'<span class="title">(.*)</span>')
findRating = re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')
findJudge = re.compile(r'<span>(\d*)人评价</span>')
findInq = re.compile(r'<span class="inq">(.*)</span>')
findBd = re.compile(r'<p class="">(.*?)</p>', re.S)


# 爬取网页
def getData(baseurl):
    datalist = []
    for i in range(0, 10):  # 调用获取页面信息的函数：10次
        url = baseurl + str(i * 25)
        html = askURL(url)  # 保存获取到的网页源码
        # 逐一解析数据
        soup = BeautifulSoup(html, "html.parser")
        for item in soup.findAll('div', class_="item"):
            data = []
            items = str(item)

            link = re.findall(findLink, items)[0]
            data.append(link)  # 添加影片地址
            imgSrc = re.findall(findImgSrc, items)[0]
            data.append(imgSrc)  # 添加图片地址
            titles = re.findall(findTitle, items)
            if len(titles) == 2:
                ctitle = titles[0]
                data.append(ctitle)  # 添加中文名
                otitle = titles[1].replace("/", "")
                data.append(otitle)  # 添加外国名
            else:
                data.append(titles[0])
                data.append(' ')  # 外国名留空
            rating = re.findall(findRating, items)[0]
            data.append(rating)  # 添加评分
            judgeNum = re.findall(findJudge, items)[0]
            data.append(judgeNum)  # 添加评价人数
            inq = re.findall(findInq, items)
            if len(inq) != 0:
                inq = inq[0].replace("。", "")  # 去掉句号
                data.append(inq)  # 添加概述
            else:
                data.append(" ")  # 留空
            bd = re.findall(findBd, items)[0]
            bd = re.sub(r'<br(\s+)?/>(\s+)?', " ", bd)  # 去掉<br/>
            bd = re.sub('/', " ", bd)  # 替换/
            data.append(bd.strip())  # 去空格
            datalist.append(data)
    return datalist


# 保存至表格
def saveData(datalist, savePath):
    print("保存中......")
    book = xlwt.Workbook(encoding="utf-8", style_compression=0)  # 创建workbook对象
    sheet = book.add_sheet('豆瓣电影Top250', cell_overwrite_ok=True)
    col = ("电影详情链接", "封面链接", "影片中文名", "影片外国名", "评分", "评价人数", "影片概述", "影片信息")
    for i in range(0, 8):
        sheet.write(0, i, col[i])  # 列名
    for i in range(0, 250):
        data = datalist[i]
        for j in range(0, 8):
            sheet.write(i + 1, j, data[j])

    book.save(savePath)


# 保存至SQLite数据库
def saveDataToDB(datalist, dbPath):
    init_db(dbPath)
    conn = sqlite3.connect(dbPath)
    cur = conn.cursor()

    for data in datalist:
        for index in range(len(data)):
            if index == 4 or index == 5:
                continue
            data[index] = '"' + data[index] + '"'
        sql = '''
            insert into movieTop250 (
            movie_info_link, movie_pic_link, movie_cn_name, movie_en_name, movie_score, movie_rated, movie_introduction, movie_info
            )values(%s)
        ''' % ",".join(data)
        cur.execute(sql)
        conn.commit()
    cur.close()
    conn.close()


# def movieIsExit():
# 初始化数据库
def init_db(dbPath):
    sql = '''
        create table movieTop250
        (
        id integer primary key  autoincrement,
        movie_info_link text,
        movie_pic_link text,
        movie_cn_name varchar,
        movie_en_name varchar,
        movie_score numeric,
        movie_rated numeric,
        movie_introduction text,
        movie_info text
        )
    '''
    conn = sqlite3.connect(dbPath)
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    conn.close()


# 获取网页链接
def askURL(url):
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:79.0) Gecko/20100101 Firefox/79.0"
    }
    request = urllib.request.Request(url, headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(request, timeout=1)
        html = response.read().decode("utf-8")
        return html
        # print(html)
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)


# 启动口
if __name__ == "__main__":
    # 调用函数
    main()
    print("爬取成功！")
    # init_db("movieTop250.db")
