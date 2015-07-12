#!/usr/bin/env python

import sys

if(sys.version_info[0]<3):
    from Tkinter import *
else:
    from tkinter import *

import RPi.GPIO as GPIO

pedal_pin = 23

GPIO.setmode(GPIO.BCM)
GPIO.setup(pedal_pin,GPIO.IN)

root = Tk()

count = 0
counter_label = StringVar()
counter = Label(root, textvariable=counter_label)
counter.pack()

def add_count():
    global count
    count += 1
    counter_label.set('Pedal was pressed {} times'.format(count))

def start_count():
    try:
        GPIO.remove_event_detect(pedal_pin)
    except Exception:
        pass
    global count
    count = 0
    counter_label.set('Pedal was pressed {} times'.format(count))
    GPIO.add_event_detect(pedal_pin, GPIO.RISING, callback=add_count, bouncetime=200)

def stop_count():
    try:
        GPIO.remove_event_detect(pedal_pin)
    except Exception:
        pass

start_button=Button(root,text='Start', command=start_count)
stop_button=Button(root,text='Stop', command=stop_count)
start_button.pack()
stop_button.pack()

root.mainloop()

