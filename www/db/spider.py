import pymysql
import logging
import time, uuid

logging.basicConfig(level=logging.DEBUG)



def update_single_data(obj):
    """  更新文章数据 """
    # 1 建立数据库连接
    connection = pymysql.connect(host='127.0.0.1',
                                 port=3306,
                                 user='root',
                                 password='mapei123',
                                 db='awesome',
                                 charset='utf8')
    affectedcount= 0
    try:
        # 创建游标对象
        with connection.cursor() as cursor:
            # 3 执行sql操作
            sql = 'update blogs set content = "{0}" WHERE content = "{1}"'.format(obj["content"],obj["url"])
            affectedcount = cursor.execute(sql)
            logging.info("影响的数据行数{0}".format(affectedcount))
            # 4 提交数据库事务
            connection.commit()
    except pymysql.DatabaseError as error:
        # 5 回滚数据库事务
        connection.rollback()
        logging.debug('插入数据失败' + error)
    finally:
        # 6 关闭数据库连接
        connection.close()
        return affectedcount




def get_spider_content_list():
    """ 查找爬虫文章列表数据 """
    # 1 建立数据库连接
    connection = pymysql.connect(host='127.0.0.1',
                                 port=3306,
                                 user='root',
                                 password='mapei123',
                                 db='awesome',
                                 charset='utf8')
    # 要返回的数据
    data = []
    try:
        # 创建游标对象
        with connection.cursor() as cursor:
            # 3 执行sql操作
            sql = 'SELECT id,content FROM blogs WHERE content LIKE "http://%"'
            cursor.execute(sql)
            # 4. 提取结果集
            result_set = cursor.fetchall()
            for row in result_set:
                fields = {}
                fields['id'] = row[0]
                fields['url'] = row[1]
                data.append(fields)
    except pymysql.DatabaseError as error:
        print('数据查询失败' + error)
    finally:
        # 6 关闭数据库连接
        connection.close()
    return data






def insert_single_list(list,pastsIdArr):
    """  插入文章数据 """
    # 1 建立数据库连接
    connection = pymysql.connect(host='127.0.0.1',
                                 port=3306,
                                 user='root',
                                 password='mapei123',
                                 db='awesome',
                                 charset='utf8')
    affectedcount= 0
    valStr = ""
    for item in list:
        if item["name"] not in pastsIdArr:
            valStr += f',(\'{item["id"]}\',\'{item["user_id"]}\',\'{item["user_name"]}\',\'{item["user_image"]}\',\'{item["name"]}\',\'{item["summary"]}\',\'{item["content"]}\',\'{item["created_at"]}\')'

    try:
        # 创建游标对象
        with connection.cursor() as cursor:
            # 3 执行sql操作
            sql = 'insert into blogs ' \
                  '(id,user_id,user_name,user_image,name,summary,content,created_at)' \
                  ' VALUES ' + valStr[1:]
            print("sql", sql)

            affectedcount = cursor.execute(sql)
            logging.info("影响的数据行数{0}".format(affectedcount))
            # 4 提交数据库事务
            connection.commit()
    except pymysql.DatabaseError as error:
        # 5 回滚数据库事务
        connection.rollback()
        logging.debug('插入数据失败' + error)
    finally:
        # 6 关闭数据库连接
        connection.close()
        return affectedcount