#!python3
# coding:gbk

# �洢������mysql

# code,����
# name,����
# industry,������ҵ
# area,����
# pe,��ӯ��
# outstanding,��ͨ�ɱ�(��)
# totals,�ܹɱ�(��)
# totalAssets,���ʲ�(��)
# liquidAssets,�����ʲ�
# fixedAssets,�̶��ʲ�
# reserved,������
# reservedPerShare,ÿ�ɹ�����
# esp,ÿ������
# bvps,ÿ�ɾ���
# pb,�о���
# timeToMarket,��������
# undp,δ������
# perundp, ÿ��δ����
# rev,����ͬ��(%)
# profit,����ͬ��(%)
# gpr,ë����(%)
# npr,��������(%)
# holders,�ɶ�����t

import sched
import threading
import time
import tkinter
from sqlalchemy import create_engine

import tushare as ts

# ɭ��
sente = '603098'

engine = create_engine('mysql://root:root@127.0.0.1/stock?charset=utf8')

schedule = sched.scheduler(time.time, time.sleep)


# �������й�Ʊ�Ļ�������
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


# ������Ӧ��Ʊ�ı�
def create_stock_hist_table(code):

    conn = engine.connect()

    str = 'create table stock_' + code + ' ( id INTEGER not NULL , s_date VARCHAR(50) not NULL , open FLOAT , ' \
          'high FLOAT , close FLOAT , low FLOAT , volume FLOAT , price_change FLOAT , ' \
          'p_change FLOAT , ma5 FLOAT , ma10 FLOAT , ma20 FLOAT , v_ma5 FLOAT , ' \
          'v_ma10 FLOAT , v_ma20 FLOAT , turnover FLOAT , primary key(id))engine=innodb ' \
          'default charset=utf8 auto_increment=1'

    conn.execute(str)


# ��ȡ��Ʊ����ʷ���ݲ��洢
def save_stock_date_data(code):
    df = ts.get_hist_data(code=code, start='2012-01-01')

    try:
        create_stock_hist_table(sente)

    except Exception as e:
        # do noting
        print(str(e))
    finally:

        df.to_sql('stock_' + code, engine, if_exists='append')


# ��ʱˢ�µ�ǰĳֻ��Ʊ��Ǯ,��֪ͨ��ӯ������
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


# ��ȡ����k���������
def get_my_k():

    df = ts.get_k_data(sente)

    print(df)

# ------------------�������й�Ʊ����-----------------
# save_all_stock()

# ------------------����ĳֻ��Ʊ����ʷ����-------------
# save_stock_date_data(sente)

# ------------------���Խ�����Ӧĳֻ��Ʊ�ı�-------------
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


# ------------------��عɼ�--------------
timer = threading.Timer(1, refresh_stock_price(sente))

timer.start()

# -----------------���� k��---------------
# get_my_k()

# -----------------���Ӽ�ؽ���----------------
# top = tkinter.Tk()
# # ������Ϣѭ��
# top.mainloop()


