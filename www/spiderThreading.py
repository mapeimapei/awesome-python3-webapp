import time
import threading
import re
import datetime
import urllib.request
from bs4 import BeautifulSoup
from datetime import datetime
import asyncio, os, json, uuid
from db.db_access import insert_register_data, insert_single_data, get_blog_data ,get_user_data
from db.spider import insert_single_list, get_spider_content_list,update_single_data
from spider import get_ire_posts,get_ire_content
count = 0
def listSpiderThreadBody():
    ''' 列表爬虫线程体函数 '''
    t = threading.current_thread()
    print("列表爬虫线程开始", t.name)
    postArr = get_ire_posts()
    blogPostArr = get_blog_data()
    pastsNameArr = []
    for item in blogPostArr:
        pastsNameArr.append(item["name"])
    count = insert_single_list(postArr, pastsNameArr)
    print("列表爬虫线程结束",t.name,count)

def contentSpiderThreadBody():
    ''' 文章爬虫线程体函数 '''
    t = threading.current_thread()
    print("文章爬虫线程开始", t.name)
    spiderContentList = get_spider_content_list()
    global count
    count = 0
    for n in range(len(spiderContentList)):
        url = spiderContentList[n]["url"]
        content = get_ire_content(url)
        obj = {
            "content":content,
            "url":url,
        }
        print(obj["url"],obj["content"])
        count += update_single_data(obj)
        print("第{0}次执行线程{1},更新数据{2}条".format(n, t.name,count))
        time.sleep(0.4)
    print("文章爬虫线程结束", t.name)

def spiderMain():
    '''主函数'''
    # 创建列表爬虫线程 listSpiderThread
    listSpiderThread = threading.Thread(target= listSpiderThreadBody, name="ListSpiderThread")
    # 启动线程 listSpiderThread
    listSpiderThread.start()
    listSpiderThread.join()
    # 创建列表爬虫线程 contentSpiderThread
    contentSpiderThread = threading.Thread(target= contentSpiderThreadBody, name="ContentSpiderThread")
    # 启动线程 contentSpiderThread
    contentSpiderThread.start()

if __name__ == '__main__':
    spiderMain()