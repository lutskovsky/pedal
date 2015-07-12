#!/usr/bin/env python

import sys

if(sys.version_info[0]<3):
    from Tkinter import *
else:
    from tkinter import *

import RPi.GPIO as GPIO

pedal_pin = 23
red = 24
green = 25

GPIO.setmode(GPIO.BCM)
GPIO.setup(pedal_pin,GPIO.IN)
GPIO.setup(24,GPIO.OUT)
GPIO.setup(25,GPIO.OUT)


GPIO.output(red, True)
GPIO.output(green, False)

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
    GPIO.output(red, False)
    GPIO.output(green, True)

def stop_count():
    try:
        GPIO.remove_event_detect(pedal_pin)
    except Exception:
        pass
    GPIO.output(red, True)
    GPIO.output(green, False)

start_button=Button(root,text='Start', command=start_count)
stop_button=Button(root,text='Stop', command=stop_count)
start_button.pack()
stop_button.pack()

root.mainloop()

