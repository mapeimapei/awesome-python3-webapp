"""商品管理DAO"""
import pymysql
from www.dao.base_dao import BaseDao

class ProductDao(BaseDao):
    def __init__(self):
        super().__init__()

    def findall(self):
        """查询所有商品信息"""
        products = []
        try:
            # 创建游标对象
            with self.conn.cursor() as cursor:
                # 3 执行sql操作
                sql = 'select productid,category,cname,ename,image,listprice,unitcost,descn from products'
                print("sql",sql)
                cursor.execute(sql)
                # 4. 提取结果集
                result_set = cursor.fetchall()
                for row in result_set:
                    product = {}
                    product['productid'] = row[0]
                    product['category'] = row[1]
                    product['cname'] = row[2]
                    product['ename'] = row[3]
                    product['image'] = row[4]
                    product['listprice'] = row[5]
                    product['unitcost'] = row[6]
                    product['descn'] = row[7]
                    products.append(product)
        except pymysql.DatabaseError as error:
            print('数据查询失败' + error)
        finally:
            # 6 关闭数据库连接
            self.close()
        return products













