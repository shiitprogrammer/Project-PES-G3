import RPi.GPIO as GPIO
import time

motorPin = 6
stepPin12 = 4
dirPin1 = 2
dirPin2 = 3
button1 = 7


GPIO.setmode(GPIO.BCM)

for l in range(7): 
    GPIO.setup(i,GPIO.OUT)

def shoot():
    GPIO.output(enablePin,0)
    time.sleep(0.1)
    GPIO.output(motorPin,1)
    time.sleep(5)
    GPIO.output(motorPin,0)
    time.sleep(0.1)
    GPIO.output(dirPin1,1)
    GPIO.output(dirPin2,0)
    for i in range(30):
        GPIO.output(stepPin12,1)
        time.sleep(0.010)
        GPIO.output(stepPin12,0)
        time.sleep(0.010)
    GPIO.output(enablePin,1)

while True:
    if GPIO.input(7):
        shoot()
        time.sleep(100)
        
        


