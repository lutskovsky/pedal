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

root=Tk()

counter=Label(root,text='Pedal was pressed 0 times')
counter.pack()

def start_count():
    GPIO.remove_event_detect()
    count = 0
    counter.text = 'Pedal was pressed {} times'.format(count)
    def add_count():
        count =+ 1
        counter.text = 'Pedal was pressed {} times'.format(count)
    GPIO.add_event_detect(pedal_pin, GPIO.RISING, callback=add_count, bouncetime=200)

def stop_count():
    GPIO.remove_event_detect()

start_button=Button(root,text='Start', command=start_count())
stop_button=Button(root,text='Stop', command=stop_count())
start_button.pack()
stop_button.pack()

root.mainloop()

