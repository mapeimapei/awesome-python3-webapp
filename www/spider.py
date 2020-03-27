import urllib.request
from bs4 import BeautifulSoup
from datetime import datetime
import asyncio, os, json, time ,uuid
import re

def get_ire_content(url):
    req = urllib.request.Request(url)
    article = ""

    arr = []
    with urllib.request.urlopen(req) as res:
        data = res.read()
        htmlStr = data.decode("gbk")
        soup = BeautifulSoup(htmlStr, 'html.parser')
        arr = soup.select('.m-article p')

    for item in arr:
        article += str(item)

    return re.sub(r'"', '\'', article)

def get_ire_posts():
    url = "http://column.iresearch.cn/"
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as res:
        data = res.read()
        htmlStr = data.decode("gbk")
        soup = BeautifulSoup(htmlStr, 'html.parser')
        liArr = soup.select('div[data="rootId=2&classId=101"] li')
    postArr = []
    for item in liArr:
        obj = {}
        obj["name"] = str.strip(item.find("h3").find("a").get_text())
        summary = str.strip(item.find("p").get_text())
        obj["summary"] = summary.strip('\n\r ')
        dt = str.strip(item.find("span").get_text())
        timeArray = time.strptime(dt, "%Y/%m/%d %H:%M:%S")
        obj["created_at"] = '%f' % time.mktime(timeArray)
        obj["content"] = str.strip(item.find("h3").find("a").get("href"))
        obj["url"] = str.strip(item.find("h3").find("a").get("href"))

        obj["id"] = str('%015d%s000' % (int(time.time() * 1000), uuid.uuid4().hex))
        obj["user_id"] = "0015836752831646b98fd78b974463c9c18321cf8136eeb000"
        obj["user_name"] = "mapei"
        obj["user_image"] = "about:blank"



        #url = item.find("h3").find("a").get("href")
        #obj["content"] = getContent(url)
        postArr.append(obj)

    return postArr

if __name__ == "__main__":
    get_ire_posts()














