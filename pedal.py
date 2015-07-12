#!/usr/bin/env python

import sys

if(sys.version_info[0]<3):
    from Tkinter import *
else:
    from tkinter import *

import RPi.GPIO as GPIO

pedal = 23
red = 24
green = 25

GPIO.setmode(GPIO.BCM)
GPIO.setup(pedal,GPIO.IN)
GPIO.setup(red,GPIO.OUT)
GPIO.setup(green,GPIO.OUT)


GPIO.output(red, True)
GPIO.output(green, False)

root = Tk()


counter_label = StringVar()
counter = Label(root, textvariable=counter_label)
counter.pack()

def set_counter(count):
    counter_label.set('Pedal was pressed {} times'.format(count))

count = 0
set_counter(count)

def add_count(channel):
    global count
    count += 1
    set_counter(count)

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

