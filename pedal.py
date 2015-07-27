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

def add_count(channel):
    GPIO.output(red, False)
    GPIO.output(green, True)
    sql = "INSERT INTO pedal_presses (station_id, timestamp) VALUES ('{}', NOW())".format(this_station_id)
    cursor.execute(sql)
    time.sleep(1)
    GPIO.output(red, True)
    GPIO.output(green, False)

GPIO.add_event_detect(pedal, GPIO.RISING if normally_open else GPIO.FALLING, callback=add_count, bouncetime=200)

while True:
    pass
