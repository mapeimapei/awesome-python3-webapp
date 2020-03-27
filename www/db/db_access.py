import pymysql
import logging;
logging.basicConfig(level=logging.DEBUG)
import time, uuid


def delete_single_data(single):
    """  删除文章数据 """
    # 1 建立数据库连接
    connection = pymysql.connect(host='127.0.0.1',
                                 port=3306,
                                 user='root',
                                 password='mapei123',
                                 db='awesome',
                                 charset='utf8')
    affectedcount = 0
    try:
        # 创建游标对象
        with connection.cursor() as cursor:
            # 3 执行sql操作
            sql = 'DELETE from blogs WHERE id = %(id)s'
            print("sql", sql)
            affectedcount = cursor.execute(sql, single)
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


def get_user_data(user):
    """ 获取用户数据 """
    # 1 建立数据库连接
    connection = pymysql.connect(host='127.0.0.1',
                                 port=3306,
                                 user='root',
                                 password='mapei123',
                                 db='awesome',
                                 charset='utf8')
    # 要返回的数据
    fields = {}
    try:
        # 创建游标对象
        with connection.cursor() as cursor:
            # 3 执行sql操作
            sql = 'select id,name,address,tel from users where (name = %(account)s or email=%(account)s) And passwd = %(passwd)s '
            affectedcount = cursor.execute(sql, user)
            if (affectedcount == 1):
                # 4. 提取结果集
                result_set = cursor.fetchall()[0]
                fields['id'] = result_set[0]
                fields['name'] = result_set[1]
                fields['address'] = result_set[2]
                fields['tel'] = result_set[3]
                fields['token'] = str('%015d%s000' % (int(time.time() * 1000), uuid.uuid4().hex))
    except pymysql.DatabaseError as error:
        print('数据查询失败' + error)
    finally:
        # 6 关闭数据库连接
        connection.close()

    return fields


def insert_single_data(single):
    """  插入文章数据 """
    # 1 建立数据库连接
    connection = pymysql.connect(host='127.0.0.1',
                                 port=3306,
                                 user='root',
                                 password='mapei123',
                                 db='awesome',
                                 charset='utf8')
    try:
        # 创建游标对象
        with connection.cursor() as cursor:
            # 3 执行sql操作


            selectSql = 'select * from blogs WHERE id = %(id)s'
            selectcount = cursor.execute(selectSql, single)
            affectedcount = ""
            sql = ""

            # 如果文章存在，则更新文章
            if selectcount == 1:
                sql = 'update blogs set ' \
                      'user_name = %(user_name)s,' \
                      'user_id = %(user_id)s,' \
                      'user_image = %(user_image)s,' \
                      'name = %(name)s,' \
                      'summary = %(summary)s,' \
                      'content = %(content)s,' \
                      'created_at = %(created_at)s' \
                      ' WHERE id = %(id)s'
            else:
                sql = 'insert into blogs ' \
                      '(id,user_id,user_name,user_image,name,summary,content,created_at)' \
                      ' VALUES (%(id)s,%(user_id)s,%(user_name)s,%(user_image)s,%(name)s,%(summary)s,%(content)s,%(created_at)s)'


            print("sql", sql)
            affectedcount = cursor.execute(sql, single)
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


def insert_register_data(user):
    """  插入用户注册数据 """
    # 1 建立数据库连接
    connection = pymysql.connect(host='127.0.0.1',
                                 port=3306,
                                 user='root',
                                 password='mapei123',
                                 db='awesome',
                                 charset='utf8')
    try:
        # 创建游标对象
        with connection.cursor() as cursor:
            # 3 执行sql操作
            sql = 'insert into users ' \
                  '(id,email,passwd,admin,name,image,created_at,address,tel)' \
                  ' VALUES (%(id)s,%(email)s,%(passwd)s,%(admin)s,%(name)s,%(image)s,%(created_at)s,%(address)s,%(tel)s)'

            affectedcount = cursor.execute(sql, user)
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


def get_blog_data():
    """ 获取列表数据 """
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
            sql = 'select id,name,summary,content,created_at,user_name from blogs order by created_at desc'
            cursor.execute(sql)
            # 4. 提取结果集
            result_set = cursor.fetchall()
            for row in result_set:
                fields = {}
                fields['id'] = row[0]
                fields['name'] = row[1]
                fields['summary'] = row[2]
                fields['content'] = row[3]
                fields['created_at'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(row[4]))
                fields['user_name'] = row[5]
                data.append(fields)
    except pymysql.DatabaseError as error:
        print('数据查询失败' + error)
    finally:
        # 6 关闭数据库连接
        connection.close()
    return data


def get_single_data(id):
    """ 获取文章数据 """
    # 1 建立数据库连接
    connection = pymysql.connect(host='127.0.0.1',
                                 port=3306,
                                 user='root',
                                 password='mapei123',
                                 db='awesome',
                                 charset='utf8')
    # 要返回的数据
    fields = {}
    try:
        # 创建游标对象
        with connection.cursor() as cursor:
            # 3 执行sql操作
            sql = 'select id,name,summary,content,created_at,user_name from blogs where id = %s'
            cursor.execute(sql, id)
            # 4. 提取结果集
            result_set = cursor.fetchall()[0]
            fields['id'] = result_set[0]
            fields['name'] = result_set[1]
            fields['summary'] = result_set[2]
            fields['content'] = result_set[3]
            fields['created_at'] = result_set[4]
            fields['user_name'] = result_set[5]

    except pymysql.DatabaseError as error:
        print('数据查询失败' + error)
    finally:
        # 6 关闭数据库连接
        connection.close()
    return fields
