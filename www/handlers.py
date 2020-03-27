#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Michael Liao'
' url handlers '
import logging;
logging.basicConfig(level=logging.INFO)
from coroweb import get, post
from models import User, Comment, Blog, next_id
from config import configs

from db.db_access import get_blog_data,get_single_data

COOKIE_NAME = 'awesession'
_COOKIE_KEY = configs.session.secret

@get('/')
def index(request):
    blogData = get_blog_data()
    return {
        '__template__': 'index.html',
        'blogData': blogData
    }


@get('/single/{id}')
def single(id):
    print("single",id)
    singleData = get_single_data(id)
    return {
        '__template__': 'single.html',
        'singleData': singleData
    }
@get('/register')
def register(request):
    return {
        '__template__': 'register.html',
    }

@get('/login')
def login():
    return {
        '__template__': 'login.html',
    }


@get('/list')
async def list():
    users = await User.findAll()
    return {
        '__template__': 'list.html',
        'users': users
    }

@get('/admin')
def admin():
    return {
        '__template__': 'admin.html',
    }

