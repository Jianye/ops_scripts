#!/usr/bin/python
# -*- coding: utf8 -*-
import time
import os
import smtplib
from email.mime.text import MIMEText

# get date,time,timespace
def getTime():
    todayTime = []
    timpeStamp=int(time.time())
    timeDate = time.strftime("%Y-%m-%d",time.localtime(timpeStamp))
    timeTime = time.strftime("%H:%M:%S",time.localtime(timpeStamp))
    todayTime = [timpeStamp,timeDate,timeTime]   
    return todayTime

# get system load  1min 5min 15min
def getLoad():
    filepath = '/proc/loadavg'
    sysload = []
    f = open(filepath)
    loadinfo = f.read()
    f.close()
    sysload = loadinfo.split()[0:3]
    return sysload

# get memory used
def getMemUsed():
    filepath = '/proc/meminfo'
    mem = {}
    mem_f = open(filepath)
    meminfo = mem_f.readlines()
    mem_f.close()
    for line in meminfo:
        name,value = line.split(':')[0],int(line.split(':')[1].split()[0])
        mem[name]=value
    mem['Used'] = mem['MemTotal']-mem['MemFree']-mem['Buffers']-mem['Cached']
    mem['Used_per'] = round((float(mem['Used'])/mem['MemTotal']*100),2)
    return mem['Used_per']

# get network traffic rz and tx speed
def getNetTraffic():
    filepath = '/proc/net/dev'
    interface = 'eth0'
    traffic = {}
    trafficOld_f = open(filepath)
    trafficinfo =trafficOld_f.readlines()
    trafficOld_f.close()
    
    for line in trafficinfo:
        if interface in line:
            traffic['rx_value_old'],traffic['tx_value_old'] = line.split(':')[1].split()[0],line.split(':')[1].split()[8]
    
    time.sleep(1)

    trafficNew_f = open(filepath)
    trafficinfo = trafficNew_f.readlines()
    trafficNew_f.close()
    
    for line in trafficinfo:
        if interface in line:
            traffic['rx_value_new'],traffic['tx_value_new'] = line.split(':')[1].split()[0],line.split(':')[1].split()[8]

    rxspeed = round((int(traffic['rx_value_new'])-int(traffic['rx_value_old']))/1024,5)
    txspeed = round((int(traffic['tx_value_new'])-int(traffic['tx_value_old']))/1024,5)
    
    return [rxspeed,txspeed]

# get socket number by the spefic
def getSocketNum():
    socketinfo=os.popen('ss -an').readlines()
    port = '22'
    status = 'ESTAB'
    socketNum = 0
    for socket in socketinfo:
        if status in socket:
            if port in socket.split()[3].split(':')[1]:
                socketNum += 1
    return socketNum 

# flatten the list
def flatten(l):  
    for el in l:  
        if hasattr(el, "__iter__") and not isinstance(el, basestring):  
            for sub in flatten(el):  
                yield sub  
        else:  
            yield el 

# write the info to log
def writeLog():
    logfilepath='/var/log/syscheck.log'
    sysrecord = []

    sysrecord.append(getTime())
    sysrecord.append(getLoad())
    sysrecord.append(getMemUsed())
    sysrecord.append(getNetTraffic())
    sysrecord.append(getSocketNum())
    
    sysrecordinfo = ','.join([str(x) for x in flatten(sysrecord)])+'\n'
    log_f = open(logfilepath,'aw')
    log_f.write(sysrecordinfo)
    log_f.close()

# send Message
def sendMessage(receiver,message):
    host = 'smtp.gmail.com'
    port = 465
    sender = 'fajianren@gmail.com'
    pwd = 'fajianrenmima'
    #FOR 126 pwd 'MKJOGO-PDELOY'
    msg = MIMEText(message)
    msg['subject'] = 'Server Alert'
    msg['from'] = sender
    msg['to'] = receiver

    s = smtplib.SMTP_SSL(host,port)
    s.login(sender,pwd)
    s.set_debuglevel(1)
    s.sendmail(sender,receiver,msg.as_string())
    s.quit

# send the mail list
def mailSender(message):
    tosendlist=['shoujianren1@126.com','shoujianren2@qq.com','shoujianren3@139.com']
    for receiver in tosendlist:
        sendMessage(receiver,message)
    

datetime = getTime()
sysload = getLoad()
memused = getMemUsed()
nettraffic = getNetTraffic()
socketnum = getSocketNum()
writeLog()

sys = {}
sys['loadcritical'] = 8
sys['memcritical'] = 95
sys['speedcritical'] = 1000*1024/8*0.8 #千兆网卡1000Mb/s 换算成 KB
sys['socketnumcri'] = 950
altermsg = ''

if float(sysload[0]) >= sys['loadcritical']:
    altermsg = 'sysLoad: '+str(sysload[0])+'\n'

if int(memused) >= sys['memcritical']:
    altermsg += 'memUsed: '+str(memused)+'\n'

if int(nettraffic[0]) >= sys['speedcritical']:
    altermsg += 'rxSpeed: '+str(nettraffic[0])+'\n'

if int(nettraffic[1]) >= sys['speedcritical']:
    altermsg += 'txSpeed: '+str(nettraffic[0])+'\n'

if int(socketnum) >= sys['socketnumcri']:
    altermsg += 'socketNum: '+str(socketnum)+'\n'

if altermsg.strip() !='':
    mailSender(altermsg)
else:
    print 'altermsg is null'
