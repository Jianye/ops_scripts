#!/usr/bin/python
# -*- coding: utf8 -*-
import time
import os
import shutil
import smtplib
from email.mime.text import MIMEText

def getTimeSptam():
    return time.strftime('%Y-%m-%d,%H:%M:%S',time.gmtime())

def getTraffic(filepath):
    ''' Get the net traffic from filepath
        Return a dic
    '''
    dev = 'eth0'
    traffic = {}
    net_f = open(filepath)
    netinfo = net_f.readlines()
    net_f.close()
    
    for line in netinfo:
        if dev in line:
              traffic['rx'],traffic['tx'] = line.split(':')[1].split()[0],line.split(':')[1].split()[8]
    return traffic
# send Message
def sendMessage(receiver,message):
    host = 'smtp.gmail.com'
    port = 465
    sender = 'www.nikksy.com@gmail.com'
    pwd = 'mkjogo-deploy'
    #FOR 126 pwd 'MKJOGO-PDELOY'
    msg = MIMEText(message)
    msg['subject'] = 'Server NetTraffic Stats'
    msg['from'] = sender
    msg['to'] = receiver

    s = smtplib.SMTP_SSL(host,port)
    s.login(sender,pwd)
    s.sendmail(sender,receiver,msg.as_string())
    s.quit
# get syshostname
def getHostName():
    filepath = '/proc/sys/kernel/hostname'
    hostname_f = open(filepath)
    hostname=hostname_f.readlines()
    hostname_f.close()
    return hostname
def writeLog(net):
    logfilepath='/var/log/nettraffic.log'
    sysrecordinfo = net['time']+','+str(net['rx_sub'])+','+str(net['tx_sub'])+','+str(net['rx_sum'])+','+str(net['tx_sum'])+'\n'
    log_f = open(logfilepath,'aw')
    log_f.write(sysrecordinfo)
    log_f.close()

if os.path.exists('/tmp/dev'):
    net_now = getTraffic('/proc/net/dev')
    net_last= getTraffic('/tmp/dev')
    net= {}
   
    net['Hostname']=''.join(getHostName()) 
    net['time'] = getTimeSptam()
    net['rx_sub'] = round((float(net_now['rx']) - int(net_last['rx']))/1024/1024,5)
    net['tx_sub'] = round((float(net_now['tx']) - int(net_last['tx']))/1024/1024,5)
    net['rx_sum'] = round(float(net_now['rx'])/1024/1024/1024,5)
    net['tx_sum'] = round(float(net_now['tx'])/1024/1024/1024,5)

    
    shutil.copyfile('/proc/net/dev','/tmp/dev')
    writeLog(net)
 
    message = ''.join(getHostName())
    message += getTimeSptam() + '\n'
    message += 'Receive: ' + str(net['rx_sub']) +' MB\n'
    message +='Translate: '+ str(net['tx_sub']) + 'MB\n'
    message += 'Receive Total: ' + str(net['rx_sum']) + 'GB\n'
    message += 'Translate Total: ' + str(net['tx_sum']) + 'GB\n' 
    
    sendMessage('mkjogo@126.com',message)    
    
else :
    shutil.copyfile('/proc/net/dev','/tmp/dev')
