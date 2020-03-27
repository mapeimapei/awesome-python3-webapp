import re, time, datetime, uuid, json, hashlib, base64, asyncio

import logging;

logging.basicConfig(level=logging.INFO)
from www.coroweb import get, post
from www.dao.product_dao import ProductDao
from www.dao.cart_dao import CartDao
from www.dao.order_dao import OrderDao


def datetimeFn(t=int(time.time())):
    timeArray = time.localtime(t)
    datetime = time.strftime("%Y.%m.%d %H:%M:%S", timeArray)
    return datetime

#删除订单中的商品
@post('/api/deleteProductInOrderDetails')
def api_deleteProductInOrderDetails(**kw):
    try:
        orderObj = {}
        orderObj["orderid"] = kw["orderid"]
        orderObj["productid"] = kw["productid"]
        orderObj["userid"] = kw["user_id"]

        orderDao = OrderDao()
        orderDao.deleteProductInOrderDetails(orderObj)
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
# 删除订单
@post('/api/deleteOrder')
def api_deleteOrder(**kw):
    try:
        orderObj = {}
        orderObj["orderid"] = kw["orderid"]
        orderObj["userid"] = kw["user_id"]

        orderDao = OrderDao()
        orderDao.deleteOrder(orderObj)
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


@post('/api/getOrdersDetailsById')
def api_getOrdersDetailsById(**kw):
    try:
        userid = kw["user_id"]
        orderid = kw["orderid"]
        orderDao = OrderDao()

        obj = {
            "resultCode": "20000",
            "message": "ok",
            "result": orderDao.getOrdersDetailsById(userid, orderid)
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


@get('/api/getOrderList/{user_id}')
def api_get_order_list(user_id):
    obj = {}
    orderDao = OrderDao()
    try:
        obj["resultCode"] = "20000"
        obj["message"] = "ok"
        obj["result"] = orderDao.getOrderList(user_id)
    except BaseException as e:
        obj["resultCode"] = "00000"
        obj["message"] = "faild"
        obj["result"] = ""
    return obj


@post('/api/addOrder')
def api_addOrder(**kw):
    try:
        orderObj = {}
        orderObj["orderid"] = str(uuid.uuid4().hex)
        orderObj["orderdate"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        orderObj["status"] = 0
        orderObj["userid"] = kw["user_id"]
        orderObj["productList"] = json.dumps(kw["productList"])
        orderObj["amount"] = 0

        for item in kw["productList"]:
            orderObj["amount"] += item["listprice"] * item["quantity"]

        orderDao = OrderDao()
        orderDao.addOrder(orderObj)

        obj = {
            "resultCode": "20000",
            "message": "ok",
            "result": {"orderid": orderObj["orderid"]}
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


@post('/api/deleteCart')
def api_deleteCart(**kw):
    try:
        cartObj = {}
        cartObj["productids"] = kw["productids"]
        cartObj["userid"] = kw["user_id"]
        cartDao = CartDao()
        cartDao.deleteCart(cartObj)
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


@get('/api/getCartList/{user_id}')
def api_get_cart_list(user_id):
    obj = {}
    cartDao = CartDao()
    try:
        obj["resultCode"] = "20000"
        obj["message"] = "ok"
        obj["result"] = cartDao.getCartList(user_id)
    except BaseException as e:
        obj["resultCode"] = "00000"
        obj["message"] = "faild"
        obj["result"] = null
    return obj


@post('/api/addCart')
def api_addCart(**kw):
    try:
        cartObj = {}
        cartObj["productid"] = kw["productid"]
        cartObj["quantity"] = kw["quantity"]
        cartObj["userid"] = kw["user_id"]
        cartDao = CartDao()
        cartDao.addCart(cartObj)
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


@get('/api/getProducts')
async def api_get_products():
    obj = {}
    products = ProductDao()
    try:
        obj["resultCode"] = "20000"
        obj["message"] = "ok"
        obj["result"] = products.findall()
    except BaseException as e:
        obj["resultCode"] = "00000"
        obj["message"] = "faild"
        obj["result"] = null

    return obj
