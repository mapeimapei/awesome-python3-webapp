import config
import time

import logging; logging.basicConfig(level=logging.INFO)

import asyncio, os, json, time
from datetime import datetime

from aiohttp import web
from jinja2 import Environment, FileSystemLoader

from config import configs

import orm
from coroweb import add_routes, add_static, add_vue_static

from api_handlers import cookie2user, COOKIE_NAME


print(time.time())
@get("/")
async def parse_data(request):
    cookie_str = request.cookies.get(COOKIE_NAME)
    if cookie_str:
        user = await cookie2user(cookie_str)
        if user:
            logging.info('set current user: %s' % user.email)
            request.__user__ = user
        print(user)
loop = asyncio.get_event_loop()
loop.run_until_complete(parse_data())
loop.run_forever()