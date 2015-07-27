#!/usr/bin/env python

import sys
import pymysql.cursors
import RPi.GPIO as GPIO
import atexit

if sys.version_info[0]<3:
    from Tkinter import *
else:
    from tkinter import *

@atexit.register
def cleanup():
    global cursor, db
    GPIO.cleanup()
    cursor.close()

username    = 'root'
password    = '123456'
database    = 'pedal'
this_station_id = 'station1'

db = pymysql.connect (host='localhost', user=username, passwd=password, db=database, autocommit=True)
cursor = db.cursor()

pedal = 23
red = 24
green = 25

GPIO.setmode(GPIO.BCM)
GPIO.setup(pedal, GPIO.IN)
GPIO.setup(red, GPIO.OUT)
GPIO.setup(green, GPIO.OUT)

GPIO.output(red, True)
GPIO.output(green, False)

root = Tk()

counter_label = StringVar()
counter = Label(root, textvariable=counter_label)
counter.pack()


def set_counter(count):
    if count == 1:
        t = 'time'
    else:
        t = 'times'
    counter_label.set('Pedal was pressed {} {}'.format(count, t))

count = 0
set_counter(count)


def add_count(channel):
    global count
    count += 1
    set_counter(count)
    sql = "INSERT INTO pedal_presses (station_id, timestamp) VALUES ('{}', NOW())".format(this_station_id)
    cursor.execute(sql)

def start_count():
    try:
        GPIO.remove_event_detect(pedal)
    except Exception:
        pass
    global count
    count = 0
    set_counter(count)
    GPIO.add_event_detect(pedal, GPIO.RISING, callback=add_count, bouncetime=200)
    GPIO.output(red, False)
    GPIO.output(green, True)


def stop_count():
    try:
        GPIO.remove_event_detect(pedal)
    except Exception:
        pass
    GPIO.output(red, True)
    GPIO.output(green, False)

start_button=Button(root,text='Start', command=start_count)
stop_button=Button(root,text='Stop', command=stop_count)
start_button.pack()
stop_button.pack()

root.mainloop()
