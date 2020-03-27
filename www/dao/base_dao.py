"""定义DAO基类"""
import pymysql
import configparser

class BaseDao(object):
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read("config.ini",encoding='utf-8')
        host = self.config['db']['host']
        user = self.config['db']['user']
        port = self.config.getint('db', 'port')
        password = self.config['db']['password']
        database = self.config['db']['database']
        charset = self.config['db']['charset']
        # 1 建立数据库连接
        self.conn = pymysql.connect(host=host,
                                    user=user,
                                    port=port,
                                    password=password,
                                    database=database,
                                    charset=charset)


    def close(self):
        self.conn.close()