#!/usr/bin/env python
# encoding: utf-8
'''
@author: yuxiaoqi
@contact: rpyxqi@gmail.com
@file: order_processing.py
@time: 20-02-27 下午9:03
@desc:
'''

import requests
import pprint
import json
import time
import datetime

opt_url = "http://119.147.211.207:8090//TradeGW/Oper/CreateAccount"
order_url = "http://119.147.211.207:8090//TradeGW/Trade/PlaceXHOrder"
query_url_prefix = "http://119.147.211.207:8090//TradeGW/Query/"


def crate_account():
    data = {'Username': 'kiki', 'Loginname': 'kiki', 'Telephone': '13760456157', 'Usertype': 0}
    headers = {'Content-type': 'application/json'}
    r = requests.post(opt_url, data=json.dumps(data), headers=headers)
    pprint.pprint(r.content)


def place_order(security_id='', order_vol=100, side='1', price=13.0, biz_action=2):
    headers = {'Content-type': 'application/json'}
    data = {'userID': '34', 'assetAccount': '010000003402', 'market': 'SZ', 'security': '300641.SZ',
            'side': '1', 'bizID': '010', 'bizAction': 4, 'orderQty': 100, 'price': 13.0}
    ticker, market = security_id.split('.')
    data.update({'security': security_id, 'side': side, 'price': price, 'market': market, 'bizAction': biz_action})
    now = datetime.datetime.now()
    # each_vol = int(total_vol / 48 / 100) * 100
    data.update({'orderQty': order_vol})
    while now.hour < 15 and now.minute < 57:
        r = requests.post(order_url, data=json.dumps(data), headers=headers)
        now = datetime.datetime.now()
        time.sleep(300)


def query_daily_reports(query_suffix="QueryCurRptList", mode='r', date=None):
    '''
    # QueryCurRptList:日回报明细；QueryCurOrdList:日委托明细；QuerySecurityAssetsList：账户持仓
    '''
    headers = {'Content-type': 'application/json'}
    data = {'userID': '34', 'assetAccount': '010000003402'}
    f_name = "data/{}_{}.json".format(query_suffix, date or datetime.date.today().strftime("%Y%m%d"))
    if mode == 'w':
        r = requests.post(query_url_prefix + query_suffix, data=json.dumps(data), headers=headers)
        with open(f_name, 'w') as outfile:
            outfile.write(r.content.decode('utf-8'))
        return json.loads(r.content.decode('utf-8'))
    elif mode == 'r':
        # load the jason file contents
        with open(f_name) as infile:
            contents = infile.read()
            return json.loads(contents)


if __name__ == '__main__':
    # place_order(security_id='000001.SZ', order_vol=30000, side='2', price=14.50, biz_action=2)
    ret = query_daily_reports(query_suffix="QuerySecurityAssetsList", mode='r', date='20200228')
    pprint.pprint(ret)