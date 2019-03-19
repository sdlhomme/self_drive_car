# -*- coding: utf-8 -*-
"""
Created on Sat Mar  9 13:41:38 2019

@author: lhomme
"""

import cv2 
import time
import thread
import socket
import numpy
import hashlib
from evdev import InputDevice
from select import select

def control():
    global key,ture
    key = -1
    ture = 0
    print("control")
    serversocket_control = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket_control.bind(('192.168.1.7',6008))
    serversocket_control.listen(1)
    clientsocket_control,addr = serversocket_control.accept() 
    dev = InputDevice('/dev/input/event3')
    while True:  
        select([dev],[],[])
        for event in dev.read():
            if (event.value == 1 or event.value == 0) and event.code != 0:
                clientsocket_control.sendall(str(event.value)+str(event.code))
                if(event.value == 1):
                    ture = 1
                    if(event.code == 17):
                        key = 2
                    elif(event.code == 30):
                        key = 0
                    elif(event.code == 31):
                        key = 3
                    elif(event.code == 32):
                        key = 1
                else:
                    ture = 2                             
    clientsocket_control.close()

def photo_collect_pc():
    global key,ture
    print("collect")
    serversocket_video = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    serversocket_video.bind(('192.168.1.7',6006))
    serversocket_video.listen(1)
    clientsocket,addr = serversocket_video.accept()      
    print("连接地址: %s" % str(addr)) 
    
    while(1):        
        info = clientsocket.recv(4)       
        #md5  = clientsocket.recv(32)
        bufSize = int(info)                         
        if bufSize:
            buf=''                
            tempBuf=''              
            while(bufSize):                
                tempBuf = clientsocket.recv(bufSize)              
                bufSize -= len(tempBuf)                   
                buf += tempBuf
            data = numpy.fromstring(buf,dtype='uint8')
            image=cv2.imdecode(data,1) 
            #m1 = hashlib.md5()
            #m1.update(buf)
            reimg = cv2.resize(image,(1280,960),cv2.INTER_LINEAR)
            cv2.imshow("open",reimg)
            cv2.waitKey(1)
            if(ture == 1):
                print("photo"+str(key))
                #print(md5)
                #print(m1.hexdigest())
                #if(md5 == m1.hexdigest()):
                cv2.imwrite('/home/lhomme/LHOMME/self_drive-master/train_data/%s_image%s.jpg' % (key,time.time()),image)
                #print("ok")
    clientsocket.close()
          
try:
   thread.start_new_thread( control, () )
   thread.start_new_thread( photo_collect_pc, () )
except:
   print "Error: unable to start thread"
 
while 1:
   pass
