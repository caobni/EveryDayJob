# -*- coding: utf-8 -*-
__author__ = 'Melissa'
"""
Module: DayJob
Author: Melissa
Created: 2014/8/6 8:58
Purpose: 老孙论坛每日签到
"""


import win32api
import win32con
import ctypes
import webbrowser
import json
import threading
from time import sleep
from datetime import datetime
from datetime import timedelta


def outputJSON(obj):
    """Default JSON serializer."""
    return obj.strftime('%Y-%m-%d %H:%M:%S.%f')

def inputJSON(obj):
    try:
        datetime.strptime(obj, '%Y-%m-%d %H:%M:%S.%f')
    except TypeError:
        pass
    return obj

def WriteJson(wfile, obj):
    try:
        with open(wfile, 'wb') as fp:
            json.dump(obj, fp, default=outputJSON)
    except Exception,e:
        print str(e)

def LoadJson(rfile):
    try:
        with open(rfile) as f:
            my_datetime = (json.load(f, object_hook=inputJSON)).encode('UTF-8')
        return datetime.strptime(my_datetime, '%Y-%m-%d %H:%M:%S.%f')
    except Exception,e:
        print str(e)

def Sign():
    Signin = "http://www.sun-knife.com/u.php"
    Singin2 = "http://home.51cto.com/index.php?s=/Home/toSign"
    date_object = LoadJson(r'Mytime.json')
    if date_object.date() >= datetime.now().date():
        win32api.MessageBox(win32con.NULL, 'Finished, thanks!', 'SUN 7+1', win32con.MB_OK )
        exit()
    else:
        nextdate = date_object + timedelta(days=1, minutes=2 )
        print 'nextdate:', nextdate
        if nextdate < datetime.now():
            webbrowser.open(Signin)
            sleep(5)
            webbrowser.open(Singin2)
            sleep(5)
            win32api.MessageBox(win32con.NULL, 'Recode the timestamp to file!', 'SUN 7+1', win32con.MB_OK )
            WriteJson(r'Mytime.json', datetime.now())
        else:
            webbrowser.open(Signin)
            sleep(5)            
            webbrowser.open(Singin2)
            delttime = nextdate - datetime.now()
            deltat =  int(timedelta.total_seconds(delttime))
            win32api.MessageBox(win32con.NULL, str(delttime), 'SUN 7+1', win32con.MB_OK )
            sleep(deltat)
            webbrowser.open(Signin)
            print sleep(5)
            win32api.MessageBox(win32con.NULL, 'Recode the timestamp to file!', 'SUN 7+1', win32con.MB_OK )
            WriteJson(r'Mytime.json', datetime.now())

def bitcoin():
    url1 = "http://freebitco.in/?op=home/"
    t = "Click on FreeBitCoin!!"
    #sleep(30*60)
    Table = True
    while(Table):
        webbrowser.open(url1)
        choice = win32api.MessageBox(0, str(t), "Continue?", win32con.MB_YESNOCANCEL)
        if choice == 6:
            print "CONTINUE"
            sleep(3600)
        elif choice == 7:
            print "RETRY"
            webbrowser.open(url1)
            sleep(5)
            rechoice = win32api.MessageBox(0, str(t), "Continue?", win32con.MB_OKCANCEL)
            if rechoice == 1:
                print 'RECHOICE = OK'
                sleep(3600)
            else:
                print 'RECHOICE = CANCEL'
                Table = False
        else:
            print "CANCEL"
            Table = False

def main():
    whnd = ctypes.windll.kernel32.GetConsoleWindow()
    if whnd != 0:
        ctypes.windll.user32.ShowWindow(whnd, 0)
        ctypes.windll.kernel32.CloseHandle(whnd)
    threads = []
    t1 = threading.Thread(target=bitcoin,args=())
    t2 = threading.Thread(target=Sign,args=())
    threads.append(t1)
    threads.append(t2)
    sleep(180)
    for i in range(2):            # start threads
        threads[i].start()

    for i in range(2):            # wait for all
        threads[i].join()       # threads to finish

if __name__=='__main__':
    main()