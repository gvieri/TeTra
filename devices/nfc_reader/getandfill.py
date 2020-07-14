# (c) vieri giovambattista 2020
# license GPL
# no guarantee as in GPL ... if you use this program you use at you own risk. 

import serial.tools.list_ports
import requests
import serial
import re
import pprint

# default values for communications with nfc reader
#port='COM1'
port='/dev/ttyUSB0'
speed=9600
startchar=0
endchar =-1
####################################################

# dafault values to post values in db 
dburl = 'http://localhost:5000/insertvalue'
#data = {"name": , 
#"value": }

####################################################





datasource=serial.Serial(port, speed, timeout=.1)

while True:
	data = datasource.readline()[startchar:endchar] #the last bit gets rid of the new-line chars
	if data:
                d=str(data)
                p=re.compile('id=(\w+)')
                q=re.compile('body_temp=(\w+)')
                name=str(p.findall(d)).replace("'","")
                value=str(q.findall(d)).replace("'","")
                pprint.pprint(value)
                value=value[1:-1]
                name=name[1:-1]
                print (str(d)+' '+name+' '+value)
                data = {"name":name,"value":value,"pin":"0000"}
                requests.post(dburl, data).text
