"""购物车DAO"""
import pymysql
import logging;

logging.basicConfig(level=logging.DEBUG)
from www.dao.base_dao import BaseDao


class CartDao(BaseDao):
    def __init__(self):
        super().__init__()

    def deleteCart(self, cartObj):
        affectedcount = 0
        try:
            # 创建游标对象
            with self.conn.cursor() as cursor:
                # 3 执行sql操作
                userid = cartObj["userid"]
                for productid in cartObj["productids"]:
                    sql = f'delete from cart WHERE userid=\'{userid}\' AND productid=\'{productid}\''
                    print("sql", sql)
                    affectedcount = cursor.execute(sql)
                    logging.info("影响的数据行数{0}".format(affectedcount))
                # 4 提交数据库事务
                self.conn.commit()
        except pymysql.DatabaseError as error:
            print('数据查询失败' + error)
        finally:
            # 6 关闭数据库连接
            self.close()
        return affectedcount

    def addCart(self, cartObj):
        try:
            # 创建游标对象
            with self.conn.cursor() as cursor:
                # 3 执行sql操作
                selectSql = 'select * from cart WHERE userid = %(userid)s AND productid = %(productid)s'
                selectcount = cursor.execute(selectSql, cartObj)
                affectedcount = ""
                sql = ""
                # 如果商品存在，则增加商品数量
                if selectcount >= 1:
                    sql = 'update cart set quantity = quantity + %(quantity)s WHERE userid = %(userid)s AND productid = %(productid)s'
                else:
                    sql = 'insert INTO cart (userid,productid,quantity) VALUES ' \
                          '(%(userid)s,%(productid)s,%(quantity)s)'
                print("sql", sql)
                affectedcount = cursor.execute(sql, cartObj)
                logging.info("影响的数据行数{0}".format(affectedcount))
                # 4 提交数据库事务
                self.conn.commit()
        except pymysql.DatabaseError as error:
            # 5 回滚数据库事务
            self.conn.rollback()
            logging.debug('插入数据失败' + error)
        finally:
            # 6 关闭数据库连接
            self.close()

    def getCartList(self, user_id):
        """查询所有商品信息"""
        cartlist = []
        try:
            # 创建游标对象
            with self.conn.cursor() as cursor:
                # 3 执行sql操作
                sql = 'SELECT c.productid,c.quantity,p.category, p.image,p.descn,p.listprice,p.cname from cart c,products p WHERE c.productid = p.productid AND c.userid = %s'
                print("sql", sql)
                cursor.execute(sql, user_id)
                # 4. 提取结果集
                result_set = cursor.fetchall()
                for row in result_set:
                    obj = {}
                    obj['productid'] = row[0]
                    obj['quantity'] = row[1]
                    obj['category'] = row[2]
                    obj['image'] = row[3]
                    obj['descn'] = row[4]
                    obj['listprice'] = row[5]
                    obj['cname'] = row[6]
                    cartlist.append(obj)
        except pymysql.DatabaseError as error:
            print('数据查询失败' + error)
        finally:
            # 6 关闭数据库连接
            self.close()
        return cartlist
