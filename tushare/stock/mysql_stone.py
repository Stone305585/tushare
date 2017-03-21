#!python3
# coding:gbk

# 存储数据至mysql

# code,代码
# name,名称
# industry,所属行业
# area,地区
# pe,市盈率
# outstanding,流通股本(亿)
# totals,总股本(亿)
# totalAssets,总资产(万)
# liquidAssets,流动资产
# fixedAssets,固定资产
# reserved,公积金
# reservedPerShare,每股公积金
# esp,每股收益
# bvps,每股净资
# pb,市净率
# timeToMarket,上市日期
# undp,未分利润
# perundp, 每股未分配
# rev,收入同比(%)
# profit,利润同比(%)
# gpr,毛利率(%)
# npr,净利润率(%)
# holders,股东人数t

import sched
import threading
import time
import tkinter
from sqlalchemy import create_engine

import tushare as ts

# 森特
sente = '603098'

engine = create_engine('mysql://root:root@127.0.0.1/stock?charset=utf8')

schedule = sched.scheduler(time.time, time.sleep)


# 保存所有股票的基本数据
def save_all_stock():

    df = ts.get_stock_basics()

    df = df[['name', 'area', 'industry', 'pe', 'outstanding', 'totals',
             'totalAssets', 'liquidAssets', 'fixedAssets', 'reserved',
             'reservedPerShare', 'pb', 'bvps', 'timeToMarket', 'profit', 'holders']]
    #
    # #     db = MySQLdb.connect(host='127.0.0.1',user='root',passwd='jimmy1',db="mystock",charset="utf8")
    # #     df.to_sql('TICK_DATA',con=db,flavor='mysql')
    # #     db.close()
    df.to_sql('stock_all', engine, if_exists='append')

    print(df.ix[1:4, :])


# 创建对应股票的表
def create_stock_hist_table(code):

    conn = engine.connect()

    str = 'create table stock_' + code + ' ( id INTEGER not NULL , s_date VARCHAR(50) not NULL , open FLOAT , ' \
          'high FLOAT , close FLOAT , low FLOAT , volume FLOAT , price_change FLOAT , ' \
          'p_change FLOAT , ma5 FLOAT , ma10 FLOAT , ma20 FLOAT , v_ma5 FLOAT , ' \
          'v_ma10 FLOAT , v_ma20 FLOAT , turnover FLOAT , primary key(id))engine=innodb ' \
          'default charset=utf8 auto_increment=1'

    conn.execute(str)


# 获取股票的历史数据并存储
def save_stock_date_data(code):
    df = ts.get_hist_data(code=code, start='2012-01-01')

    try:
        create_stock_hist_table(sente)

    except Exception as e:
        # do noting
        print(str(e))
    finally:

        df.to_sql('stock_' + code, engine, if_exists='append')


# 定时刷新当前某只股票价钱,并通知我盈利亏损
def refresh_stock_price(code):

    df = ts.get_realtime_quotes(code)

    buy = 28.006

    current = float(df.ix[0, 'price'])

    if current > buy:
        print(code + 'XXXXXXX->' + str((current - buy) * 200))
    else:
        print(code + 'ooooooo->' + str((current - buy) * 200))

    schedule.enter(5, 0, refresh_stock_price, (code,))

    schedule.run()


# 获取各种k线相关数据
def get_my_k():

    df = ts.get_k_data(sente)

    print(df)

# ------------------保存所有股票数据-----------------
# save_all_stock()

# ------------------保存某只股票的历史数据-------------
# save_stock_date_data(sente)

# ------------------调试建立对应某只股票的表-------------
# conn = engine.connect()
#
# sql_str = 'select code from stock_all'
#
# ss = conn.execute(sql_str)
#
# for code in ss:
#     code_s = str(code)[2:8]
#     # print(code_s)
#     create_stock_hist_table(code_s)


# ------------------监控股价--------------
timer = threading.Timer(1, refresh_stock_price(sente))

timer.start()

# -----------------调试 k线---------------
# get_my_k()

# -----------------增加监控界面----------------
# top = tkinter.Tk()
# # 进入消息循环
# top.mainloop()


