#!/usr/bin/env python

import pymysql.cursors
import RPi.GPIO as GPIO
import atexit
import time

@atexit.register
def cleanup():
    global cursor, db
    GPIO.cleanup()
    cursor.close()

username    = 'root'
password    = '123456'
database    = 'pedal'
this_station_id = 'station1'
normally_open = True  # set to True if the switch is normally open, to False if normally closed
bouncetime=1000

pedal = 23
red = 24
green = 25

db = pymysql.connect (host='localhost', user=username, passwd=password, db=database, autocommit=True)
cursor = db.cursor()


GPIO.setmode(GPIO.BCM)
GPIO.setup(pedal, GPIO.IN)
GPIO.setup(red, GPIO.OUT)
GPIO.setup(green, GPIO.OUT)


def red_led(channel):
    GPIO.output(red, True)
    GPIO.output(green, False)
    
def green_led(channel):
    GPIO.output(red, False)
    GPIO.output(green, True)

def add_record(channel):
    sql = "INSERT INTO pedal_presses (station_id, timestamp) VALUES ('{}', NOW())".format(this_station_id)
    cursor.execute(sql)

red_led()

GPIO.add_event_detect(pedal, GPIO.RISING if normally_open else GPIO.FALLING)
GPIO.add_event_callback(pedal, callback=green_led)
GPIO.add_event_callback(pedal, callback=add_record, bouncetime=bouncetime)

GPIO.add_event_detect(pedal, GPIO.FALLING if normally_open else GPIO.RISING, callback=red_led)

while True:
    pass
