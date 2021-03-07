#Description

#This Python3 script combines Afterglow PS3 USB button-press data with 2 motor activation. 



#testbed information

#This was developed as a deliberately low powered and lightweight combination. It is also affordable at near $200 USD current pricing for all the parts. The Pi3 is used for it's common use, versatility, and teachability. (An Arduino can't easily be substituted because of the other existing hardware. The GPIO pins use different wires. Power is wired differenly, etc. This is really meant for the Python and Pi crowd.)

#The advantage of using a Pi powered setup like this is the available computing power. Every compatible mod, sensor, and binary package can still be used. There is just enough code and parts here to make something drivable. You, the tinkerer, can make it smarter, faster, and stronger with what you can do. There is plenty of Pi battery power left to support extra sensors, actuators, and servos. 


#Hardware used is: 
	#$35 RPI3
	#$ 7 L298N motor controller ($10 for 2, but you only need 1 to drive the treads with.)
	#$10 5v 2.5a 3800mAH phone charger battery
	#$25 7.2v 1200mAH Traxxas NimH #2925X. 
	#$25 Afterglow PS3 gamepad clone. Wireless USB equipped. Not bluetooth capable. (ONLY BUTTONS WORK AT THIS TIME 02/2021)
	#$10 Pi wire kit

 
# Only 18 wires were used on this chassis. 
# QTY 7 from the pi to the motor controller. 
# QTY 8 from the motor controller to the Traxxas battery. 
# QTY 2 on the motor battery.
# QTY 1 from the phone charger to the Pi3B+.
# The other advantage of this simpler initial setup is the room for growth. You can still add



#SAFETY warning.
#No warranty of parts, labor, or service is guaranteed or implied with use of this information. Safety is up to you first. Don't drink and drive. Don't use higher current unless necessary, either. These are purposely sourced as friendly parts for hobbyist and experimental use.




#BATTERY INFO VERY IMPORTANT
#The Pi should run for 4+ hours on a 3800mAH battery. The motors for about 30-45 minutes. The drive battery is admittedly small even on a basic chassis with low weight. It is about as fast as a slow-normal walking speed. 100% motor usage is like a brisk walk. This setup uses a 7.2v. You could easily use an 11.4v RC battery, but be sure to dial the motors back. 

#If a larger battery is used, turn the power down!
	#7.2v is a slow walk and makes for easy turning.
	#p.start(60) 
	#p2.start(65)
	
	#turn down the commanded power like this.
	#p.start(30) for 11.2v should keep the speed down.
	#p2.start(35) for 11.2v should keep the speed down.

	#the current settings of (60-65) for the 2 drive motors ensure easier turning. Just enough power is requested to avoid stalling the motors during steering or pivoting. Low RPM and power usage makes for 				#easier transition of motor direction. That is how the tank chassis steers.  
	 
	#Usage on carpet isn't advised due to static moreso than hair and dirt. (Don't chase dogs, either. Chewing and drool isn't good for electronics.)  
 	
 
# 2 motor instructions to work with in the gamepad scripting.  Currently analog sticks do not function.

#(select) stop, (start) exit, forward, back, 3 speeds lo-med-hi

#import evdev
from evdev import InputDevice, categorize, ecodes

import RPi.GPIO as GPIO
from time import sleep
import pygame

#creates object 'gamepad' to store the data
#you can call it whatever you like
gamepad = InputDevice('/dev/input/event0')

#button code variables (change to suit your device)
aBtn = 305
bBtn = 307
xBtn = 304
yBtn = 308

up = 46
down = 32
left = 317
right = 318

#'select' is for stop function.
# 'start' is for gpio cleanup.
select = 314
start = 315


lTrig = 310
rTrig = 311

#analog stick press. Might not work yet.
left = 317
right = 318

#middle buttons
start = 315
select = 314

#upper triggers
lTrig = 310
rTrig = 311

#These are GPIO output addresses for each motor.

in1 = 24 # R Motor GPIO address
in2 = 23 # R Motor GPIO address
in3 = 17 # L Motor GPIO address
in4 = 27 # L Motor GPIO address
en = 25
en2 = 22
temp1=1

GPIO.setmode(GPIO.BCM)
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(en,GPIO.OUT)
GPIO.setup(in3,GPIO.OUT)
GPIO.setup(in4,GPIO.OUT)
GPIO.setup(en2,GPIO.OUT)
GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)
GPIO.output(in3,GPIO.LOW)
GPIO.output(in4,GPIO.LOW)
p=GPIO.PWM(en,1000)
p2=GPIO.PWM(en2,1000)

#Motor power setup here. Just one speed.
p.start(60)
p2.start(65) #l motor is a little weaker on my setup.
#Compensate with slightly more juice going to the weaker motor to help it drive straighter.

print("\n")
print("The default speed & direction of motor is Medium & Forward.....")
print("r-run s-stop f-forward y-forward motor-2 b-backward l-low m-medium h-high e-exit")
print("\n")    

#prints out device info at start
print(gamepad)

#loop and filter by event code and print the mapped label
for event in gamepad.read_loop():
    if event.type == ecodes.EV_KEY:
        if event.value == 1:
            if event.code == yBtn:
                print("Y = Forward")
                #if(temp1==1):
                GPIO.output(in1,GPIO.LOW)
                GPIO.output(in2,GPIO.HIGH)
                GPIO.output(in3,GPIO.LOW)
                GPIO.output(in4,GPIO.HIGH)
                x='z' #very important! Motor "runs away" without this code in every instruction!
            elif event.code == bBtn:
                print("B = Pivot Left")
                GPIO.output(in3,GPIO.LOW)
                GPIO.output(in4,GPIO.HIGH)
                #Below is from Backwards function to spin inside motor backwards, bit like an e-brake."
                GPIO.output(in1,GPIO.HIGH)
                GPIO.output(in2,GPIO.LOW)
                x='z'
            elif event.code == aBtn:
                print("A = Pivot Right")
                GPIO.output(in1,GPIO.LOW)
                GPIO.output(in2,GPIO.HIGH)
                #Below is from Backwards function to spin inside motor backwards, bit like an e-brake."
                GPIO.output(in3,GPIO.HIGH)
                GPIO.output(in4,GPIO.LOW)
                x='z'
            elif event.code == xBtn:
                print("X = Backwards")
                GPIO.output(in1,GPIO.HIGH)
                GPIO.output(in2,GPIO.LOW)
                GPIO.output(in3,GPIO.HIGH)
                GPIO.output(in4,GPIO.LOW)
                x='z'
            elif event.code == up:
                print("up")
            elif event.code == down:
                print("down")
            elif event.code == left:
                print("left")
            elif event.code == right:
                print("right")

            elif event.code == start:
                x='z'
                #elif x=='e':
                GPIO.cleanup()
                print("Start Button = GPIO Clean up")
                break
            
            elif event.code == select:
                print("Select Button = Stop")
                GPIO.output(in1,GPIO.LOW)
                GPIO.output(in2,GPIO.LOW)
                GPIO.output(in3,GPIO.LOW)
                GPIO.output(in4,GPIO.LOW)
                x='z'

            elif event.code == lTrig:
                print("Left Bumper = Left Motor Stop")
                GPIO.output(in3,GPIO.LOW)
                GPIO.output(in4,GPIO.LOW)
                x='z'
            elif event.code == rTrig:
                print("Right Bumper = Right Motor Stop")
                GPIO.output(in1,GPIO.LOW)
                GPIO.output(in2,GPIO.LOW)
                x='z'
