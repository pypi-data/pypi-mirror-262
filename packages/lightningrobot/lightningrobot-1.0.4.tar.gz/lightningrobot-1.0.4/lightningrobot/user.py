import pymysql
from lightningrobot import log 

db = pymysql.connect(host='localhost',
                         user='lightningrobot',
                         password='lightningrobot',
                         database='Robot')
cursor = db.cursor()

def initialization():
    # 删除已存在同名表
    cursor.execute("DROP TABLE IF EXISTS user")

    # 使用预处理语句创建新表
    sql = """CREATE TABLE user (
             id INT PRIMARY KEY NOT NULL,
             name CHAR(20),
             authority CHAR(20),
             password CHAR(20))"""

    # 执行创建表的SQL语句
    cursor.execute(sql)

    # 关闭数据库连接
    db.close()

def create(name):
    authority = 1
    password = 'lightningrobot'
    # 使用参数化查询构造SQL语句
    sql = "INSERT INTO user (name, authority, password) VALUES (%s, %s, %s)"
    data = (name, authority, password)

    try:
        # 执行SQL插入语句
        cursor.execute(sql, data)
        # 提交到数据库执行
        db.commit()
    except Exception as e:
        # 如果发生错误则回滚
        db.rollback()
        log.error(f"{e}")
        
    # 关闭数据库连接
    db.close()