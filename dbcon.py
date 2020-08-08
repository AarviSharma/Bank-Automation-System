import pymysql as sql
def getCon():
    con=sql.connect(host='localhost',port=3306,user='root',password='root',db='bank')
    return con
