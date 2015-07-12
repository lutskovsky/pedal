import sys

if(sys.version_info[0]<3):
    from Tkinter import *
else:
    from tkinter import *

import RPi.GPIO as GPIO

GPIO.add_event_detect(channel, GPIO.RISING, callback=my_callback, bouncetime=200)


root=Tk()

counter=Label(root,text='Pedal was pressed 0 times')
start_button=Button(root,text='Start')
stop_button=Button(root,text='Stop')

counter.pack()
start_button.pack()
stop_button.pack()


root.mainloop()

