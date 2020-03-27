"""购物车DAO"""
import pymysql
import time, datetime, json, decimal
import logging;

logging.basicConfig(level=logging.DEBUG)
from www.dao.base_dao import BaseDao


class OrderDao(BaseDao):
    def __init__(self):
        super().__init__()

    def deleteProductInOrderDetails(self, orderObj):
        affectedcount = 0
        try:
            # 创建游标对象
            with self.conn.cursor() as cursor:
                # 3 执行sql操作
                # 删除订单表数据
                sql = 'DELETE FROM orderdetails where orderid = %(orderid)s AND productid = %(productid)s '
                affectedcount = cursor.execute(sql, orderObj)

                # 4 提交数据库事务
                self.conn.commit()
        except pymysql.DatabaseError as error:
            print('数据查询失败' + error)
        finally:
            # 6 关闭数据库连接
            self.close()
        return affectedcount



    def deleteOrder(self, orderObj):
        # affectedcount = 0
        try:
            # 创建游标对象
            with self.conn.cursor() as cursor:
                # 3 执行sql操作
                # 插入订单详情数据
                sql = 'DELETE FROM orderdetails where orderid = %(orderid)s'
                affectedcount = cursor.execute(sql, orderObj)

                # 删除订单表数据
                sql2 = 'DELETE FROM orders where orderid = %(orderid)s AND userid = %(userid)s '
                affectedcount2 = cursor.execute(sql2, orderObj)

                # 4 提交数据库事务
                self.conn.commit()
        except pymysql.DatabaseError as error:
            print('数据查询失败' + error)
        finally:
            # 6 关闭数据库连接
            self.close()
        #return affectedcount

    def getOrderList(self, userid):
        """查询订单信息"""
        orderlist = []
        try:
            # 创建游标对象
            with self.conn.cursor() as cursor:
                # 3 执行sql操作
                sql = f'select orderid,CAST(orderdate AS CHAR),status,amount from orders where userid = \'{userid}\' ORDER BY orderdate desc'
                print("sql", sql)
                cursor.execute(sql)
                # 4. 提取结果集
                result_set = cursor.fetchall()
                for row in result_set:
                    obj = {}
                    obj['orderid'] = row[0]
                    obj['orderdate'] = row[1]
                    obj['status'] = row[2]
                    obj['amount'] = float(row[3])
                    orderlist.append(obj)
        except pymysql.DatabaseError as error:
            print('数据查询失败' + error)
        finally:
            # 6 关闭数据库连接
            self.close()
        return orderlist

    def addOrder(self, orderObj):
        orderid = orderObj["orderid"]
        userid = orderObj["userid"]
        valStr = ""
        productList = json.loads(orderObj["productList"])
        productLists = []
        for item in productList:
            productLists.append(item["productid"])
            valStr += f',(\'{orderid}\',\'{item["productid"]}\',\'{item["quantity"]}\')'
        try:
            # 创建游标对象
            with self.conn.cursor() as cursor:
                # 3 执行sql操作

                # 删除购物车的对应数据
                for productid in productLists:
                    sql3 = f'delete from cart WHERE userid=\'{userid}\' AND productid=\'{productid}\''
                    cursor.execute(sql3)
                # 插入订单数据
                sql = 'insert INTO orders (orderid,userid,orderdate,status,amount) VALUES ' \
                      '(%(orderid)s,%(userid)s,%(orderdate)s,%(status)s,%(amount)s)'
                cursor.execute(sql, orderObj)

                # 插入订单详情数据
                sql2 = 'insert INTO orderdetails (orderid,productid,quantity) ' \
                       'VALUES ' + valStr[1:]
                cursor.execute(sql2)

                # 4 提交数据库事务
                self.conn.commit()
        except pymysql.DatabaseError as error:
            # 5 回滚数据库事务
            self.conn.rollback()
            logging.debug('插入数据失败' + error)
        finally:
            # 6 关闭数据库连接
            self.close()

    def getOrdersDetailsById(self, userid, orderid):
        """查询订单信息"""

        orderObj = {}
        orderObj["orderlist"] = []
        orderObj["amount"] = 0
        try:
            # 创建游标对象
            with self.conn.cursor() as cursor:
                # 3 执行sql操作
                sql = f'select a.orderid, CAST(a.orderdate AS CHAR),a.status,a.amount,b.productid,b.quantity,c.category,c.descn,c.image, c.cname,c.listprice from (orderdetails b inner join products c on b.productid = c.productid) inner join orders a on a.orderid = b.orderid where a.userid = \'{userid}\' and a.orderid = \'{orderid}\''

                print("sql", sql)
                cursor.execute(sql)
                # 4. 提取结果集
                result_set = cursor.fetchall()
                for row in result_set:
                    obj = {}
                    obj['orderid'] = row[0]
                    obj['orderdate'] = row[1]
                    obj['status'] = row[2]
                    obj['amount'] = float(row[3])
                    obj['productid'] = row[4]
                    obj['quantity'] = row[5]
                    obj['category'] = row[6]
                    obj['descn'] = row[7]
                    obj['image'] = row[8]
                    obj['cname'] = row[9]
                    obj['listprice'] = row[10]
                    orderObj["orderlist"].append(obj)
                    orderObj["amount"] += row[10] * row[5]
        except pymysql.DatabaseError as error:
            print('数据查询失败' + error)
        finally:
            # 6 关闭数据库连接
            self.close()
        return orderObj
