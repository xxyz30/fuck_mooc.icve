import pymysql

host = ""
user = "root"
pwd = ""
db = "mooc"
conn = pymysql.connect(user=user, host=host, db=db, password=pwd)

# 使用cursor()方法获取操作游标
cursor = conn.cursor()


def insert(resList):
    for i in resList.keys():
        try:
            sql = f"insert into question values('{i}', '{resList[i]}')"
            cursor.execute(sql)
            conn.commit()
        except Exception as ex:
            print(ex)
