#!python3
# coding:gbk
# guiСdemo
import threading
from tkinter import *

import time
import tushare as ts
import sched

# ɭ��
sente   = '603098'
# ��Ͽ
haixia  = '603817'
# ���
chongda = '002815'

schedule = sched.scheduler(time.time, time.sleep)


# ��ȡ�ҵĹ�Ʊ����
def get_my_stock():

    df_sente = ts.get_realtime_quotes(sente)
    df_haixia = ts.get_realtime_quotes(haixia)
    df_chongda = ts.get_realtime_quotes(chongda)

    res = dict()
    res[sente] = {'time':df_sente.ix[0, 'time'], 'price':df_sente.ix[0, 'price'], 'open':df_sente.ix[0, 'open']}
    res[haixia] = {'time':df_haixia.ix[0, 'time'], 'price':df_haixia.ix[0, 'price'], 'open':df_haixia.ix[0, 'open']}
    res[chongda] = {'time':df_chongda.ix[0, 'time'], 'price':df_chongda.ix[0, 'price'], 'open':df_chongda.ix[0, 'open']}

    return res


# ˢ������
def refresh_data():
    current_data = get_my_stock()

    price = float(current_data[sente]['price'])
    price_haixia = float(current_data[haixia]['price'])
    open_haixia = float(current_data[haixia]['open'])

    # ��������
    list_sente.insert(0, current_data[sente]['time'] + '  ' + current_data[sente]['price'] + '  ' + str((price - 28.006) * 200)[0:5])
    list_chongda.insert(0, current_data[chongda]['time'] + '     ' + current_data[chongda]['price'])
    list_haixia.insert(0, current_data[haixia]['time'] + '      ' + current_data[haixia]['price'])

    # �ı���ɫ
    if float(current_data[sente]['price']) > 28.006:
        list_sente.itemconfig(0, fg='red')
    else:
        list_sente.itemconfig(0, fg='green')

    #����5�վ��߾���
    if price > ma5_sente:
        list_sente.insert(0, '�������棡��   ' + str(ma5_sente))
        list_sente.itemconfig(0, fg='#345231')
    else:
        list_sente.insert(0, '   ')
        list_sente.itemconfig(0, fg='#888931')

    if open_haixia > price_haixia:
        list_haixia.insert(0, '��ǰ����   ' + str((open_haixia - price_haixia)/open_haixia * 100)[0:5] + '%')
        list_haixia.itemconfig(0, fg='green')
    else:
        list_haixia.insert(0, '��ǰ�Ƿ�   ' + str(-(open_haixia - price_haixia) / open_haixia * 100)[0:5] + '%')
        list_haixia.itemconfig(0, fg='red')

    schedule.enter(5, 0, refresh_data, ())
    schedule.run()



# ------------------------��������----------------------
root = Tk()

root.title("ʵʱ���")

list_sente  = Listbox(root, width=30)
list_chongda = Listbox(root, width=30)
list_haixia = Listbox(root, width=30)
label_sente = Label(text='ɭ��', highlightcolor='black')
label_chongda = Label(text='���', highlightcolor='black')
label_haixia = Label(text='��Ͽ', highlightcolor='black')

# ��С�������õ���������
label_sente.pack()
list_sente.pack()

label_haixia.pack()
list_haixia.pack()

label_chongda.pack()
list_chongda.pack()

df_hist_sente = ts.get_hist_data(code=sente, start='2017-03-20')
ma5_sente = float(df_hist_sente.ix[0, 'ma5'])

# # ����ˢ���б�
t1 = threading.Thread(target=refresh_data,args=())
t1.start()

# ������Ϣѭ��
root.mainloop()


