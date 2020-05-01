#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Michael Liao'

import time

' url api_handlers '
import re, uuid, json, hashlib, base64, asyncio
import logging
import threading
import datetime

logging.basicConfig(level=logging.INFO)
from coroweb import get, post 
from aiohttp import web
from models import User, Comment, Blog, next_id
from config import configs
from db.db_access import insert_register_data, insert_single_data, get_blog_data ,get_user_data,delete_single_data,get_single_data
from db.spider import insert_single_list
from spider import get_ire_posts,get_ire_content

from spiderThreading import spiderMain


from dao.product_dao import ProductDao


COOKIE_NAME = 'awesession'
_COOKIE_KEY = configs.session.secret


def user2cookie(user, max_age):
    '''
    Generate cookie str by user.
    '''
    # build cookie string by: id-expires-sha1
    expires = str(int(time.time() + max_age))
    s = '%s-%s-%s-%s' % (user.id, user.passwd, expires, _COOKIE_KEY)
    L = [user.id, expires, hashlib.sha1(s.encode('utf-8')).hexdigest()]
    return '-'.join(L)


def text2html(text):
    lines = map(lambda s: '<p>%s</p>' % s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'),
                filter(lambda s: s.strip() != '', text.split('\n')))
    return ''.join(lines)


async def cookie2user(cookie_str):
    '''
    Parse cookie and load user if cookie is valid.
    '''
    if not cookie_str:
        return None
    try:
        L = cookie_str.split('-')
        if len(L) != 3:
            return None
        uid, expires, sha1 = L
        if int(expires) < time.time():
            return None
        user = await User.find(uid)
        if user is None:
            return None
        s = '%s-%s-%s-%s' % (uid, user.passwd, expires, _COOKIE_KEY)
        if sha1 != hashlib.sha1(s.encode('utf-8')).hexdigest():
            logging.info('invalid sha1')
            return None
        user.passwd = '******'
        return user
    except Exception as e:
        logging.exception(e)
        return None


def next_id():
    return '%015d%s000' % (int(time.time() * 1000), uuid.uuid4().hex)


@post('/api/testPost')
def testPost(*, params1, params2):
    logging.info('parmas1:%s, parmas2:%s' % (params1, params2))
    obj = {
        "resultCode": "20000",
        "message": "ok",
        "data": {"params1": params1, "params2": params2, }
    }
    return obj

@get('/api/getSingleById/{id}')
async def api_get_single(id):
    obj = {}
    try:
        obj["resultCode"] = "20000"
        obj["message"] = "ok"
        obj["result"] = get_single_data(id)
    except BaseException as e:
        obj["resultCode"] = "00000"
        obj["message"] = "faild"
        obj["result"] = {}

    return obj


@post('/api/deleteSingle')
async def api_deleteSingle(**kw):
    try:
        single = {}
        single["id"] = kw["id"]
        single["user_id"] = kw["user_id"]
        row = delete_single_data(single)
        obj = {}
        if(row >=1):
            obj = {
                "resultCode": "20000",
                "message": "ok",
                "data": {}
            }
        else:
            obj = {
                "resultCode": "000001",
                "message": "faild",
                "data": {}
            }
        return obj

    except BaseException as e:
        print("error", type(e))
        obj = {
            "resultCode": "000000",
            "message": "%s" % e,
            "data": {}
        }
        return obj




@post('/api/startSpider2')
def startSpider2():
    spiderMain()
    obj = {
        "resultCode": "20000",
        "message": "小蜘蛛已如脱缰野马飞奔而出。请留意页面变化。。。",
        "result": {}
    }
    return obj



@post('/api/startSpider')
def startSpider():
    try:
        postArr =  get_ire_posts()
        blogPostArr =  get_blog_data()
        pastsNameArr = []
        for item in blogPostArr:
            pastsNameArr.append(item["name"])
        count = insert_single_list(postArr,pastsNameArr)

        obj = {
            "resultCode": "20000",
            "message": f"爬虫已经完成工作，抓取{count}条数据。",
            "result": {}
        }
        return obj
    except BaseException as e:
        print("error", type(e))
        obj = {
            "resultCode": "000000",
            "message": "%s" % e,
            "result": {}
        }
        return obj


@get('/api/getPosts')
async def api_get_posts():
    obj = {}
    try:
        obj["resultCode"] = "20000"
        obj["message"] = "ok"
        obj["result"] = get_blog_data()
    except BaseException as e:
        obj["resultCode"] = "00000"
        obj["message"] = "faild"
        obj["result"] = null

    return obj



@post('/api/login')
async def api_login(**kw):
    obj={}
    try:
        user = {}
        user["account"] = kw["account"]
        user["passwd"] = kw["passwd"]
        result = get_user_data(user)
        if(result):
            obj["resultCode"] = "20000"
            obj["message"] = "ok"
            obj["result"] = result
        else:
            obj["resultCode"] = "000000"
            obj["message"] = "faild"
            obj["result"] = result

    except BaseException as e:
        print("error", type(e))
        obj["resultCode"] = "000000"
        obj["message"] = "faild"
        obj["result"] = ""
    finally:
        return  obj


@post('/api/addSingle')
async def api_addSingle(**kw):
    try:
        single = {}
        single["id"] = kw["post_id"] if kw["post_id"] else str(next_id())
        single["user_id"] = kw["user_id"]
        single["user_name"] = kw["user_name"] if kw["user_name"] else "mapei"
        single["user_image"] = "about:blank"
        single["name"] = kw["name"]
        single["summary"] = kw["summary"]
        single["content"] = kw["content"]
        single["created_at"] = str(time.time())
        insert_single_data(single)
        obj = {
            "resultCode": "20000",
            "message": "ok",
            "data": {}
        }
        return obj
    except BaseException as e:
        print("error", type(e))
        obj = {
            "resultCode": "000000",
            "message": "%s" % e,
            "data": {}
        }
        return obj




@post('/api/register2')
async def api_register2(**kw):
    try:
        user = {}
        user["name"] = kw['name'].strip()
        user["email"] = kw['email']
        user["passwd"] = kw['passwd']
        user["address"] = kw['address']
        user["tel"] = kw['tel']
        user["id"] = str(next_id())
        user["admin"] = 0
        user["image"] = "about:blank"
        user["created_at"] = str(time.time())
        insert_register_data(user)
        obj = {
            "resultCode": "20000",
            "message": "ok",
            "data": {}
        }
        return 'redirect:/'
        #return obj
    except BaseException as e:
        print("error", type(e))
        obj = {
            "resultCode": "000000",
            "message": "%s" % e,
            "data": {}
        }
        return obj


@post('/api/register')
async def api_register(**kw):
    try:
        user = User(
            name=kw['name'].strip(),
            email=kw['email'],
            passwd=kw['passwd'],
        )
        await user.save()
        obj = {
            "resultCode": "20000",
            "message": "ok",
            "data": {}
        }
        # make session cookie:
        r = web.Response()
        r.set_cookie(COOKIE_NAME, user2cookie(user, 86400), max_age=86400, httponly=True)
        user.passwd = '******'
        r.content_type = 'application/json'
        r.body = json.dumps(user, ensure_ascii=False).encode('utf-8')
        return 'redirect:/'  # 重定向跳转
        # return r
    except BaseException as e:
        print("111", type(e))
        obj = {
            "resultCode": "000000",
            "message": "%s" % e,
            "data": {}
        }
        return obj


@get('/api/users')
async def api_get_users():
    users = await User.findAll(orderBy='created_at desc')
    for u in users:
        u.passwd = '******'
    return dict(users=users)
