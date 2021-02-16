#!/usr/bin/python
from binance.client import Client
import re
import matplotlib.pyplot as plt
from mpl_finance import candlestick_ohlc
import pandas as pd
import numpy as np
import time # für die aktuelle Zeit
import datetime # für die Datumsumrechnung
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from smtplib import SMTP
import smtplib
import sys

client = Client("Binance-API Username", "Binance-API Password")

### TIME
UnixTime = int(time.time())
currentdate = datetime.datetime.fromtimestamp(UnixTime).strftime('%Y-%m-%d')

CrashAlert_newrow = ([UnixTime, int(datetime.datetime.fromtimestamp(UnixTime).strftime('%Y')), int(datetime.datetime.fromtimestamp(UnixTime).strftime('%m')), int(datetime.datetime.fromtimestamp(UnixTime).strftime('%d')), int(datetime.datetime.fromtimestamp(UnixTime).strftime('%H' + "00"))])

COINS = ['DOGEUSDT']
for COIN in COINS:
    scraping_ohlc_coin = client.get_klines(symbol=COIN, interval=Client.KLINE_INTERVAL_30MINUTE)
    scraping_ohlc_coin = np.asarray(scraping_ohlc_coin)
    scraping_ohlc_coin = scraping_ohlc_coin[:,:5]
    Index = np.unique([scraping_ohlc_coin[:,0]], return_index=True)
    close = scraping_ohlc_coin[Index[1],:][-1][4]
    CrashAlert_newrow.append(float(close))
    CrashAlert_newrow.append(float(0)) # is needed for the counter whether a hint was already sent, so that one is not spammed
	
	
if CrashAlert_newrow[-2] < 0.0026:
    CrashAlert_newrow[-1] = 1

path_ = "C:/#########################/DOGE_CrashAlert.csv"

CrashAlert = np.loadtxt(path_, delimiter=",")
CrashAlert = np.flipud(CrashAlert)
CrashAlert = np.vstack([CrashAlert, CrashAlert_newrow])
CrashAlert = np.flipud(CrashAlert)
fmt = '%d', '%d', '%d', '%d','%d', '%1.4f', '%1.0f'
np.savetxt(path_, CrashAlert, delimiter=",", fmt=fmt)

if CrashAlert[0,-1] != CrashAlert[1,-1]:
    Name = 'DOGECOIN cheaper than 0.0026 USD: ' + str(CrashAlert_newrow[-2]) +  'USD'
    fromaddr = '########@gmail.com' #Sender email address
    toaddr = '######@gmail.com' # Target email adress
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = currentdate + ": " + Name
    body = ''
    msg.attach(MIMEText(body, 'plain'))
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, '############') # Sender email address password
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()