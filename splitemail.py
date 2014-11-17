#!/usr/bin/python

def writeEmail(emailaddress):
        domainName = emailaddress.split('@')[1].strip()
        fg = open(domainName,'a')
        fg.write(emailaddress)
        fg.close()


emailfile='/home/jianye/xiaomiemail/xiaomiemail.txt'

fg  = open(emailfile)

emailaddressall = fg.readlines()

domain = []

for emailAddress in   emailaddressall:
        emaillist = emailAddress.split('@')
        if len(emaillist) > 1:
                if emaillist[1] in domain:
                        writeEmail(emailAddress)
                else:
                        writeEmail(emailAddress)
                        domain.append(emaillist[1])
