#!/usr/local/bin/python

import RPi.GPIO as GPIO
import time
from gpiozero import Buzzer
'''
__author__ = 'Gus (Adapted from Adafruit)'
__license__ = "GPL"
__maintainer__ = "pimylifeup.com"'''

GPIO.setmode(GPIO.BOARD)

#define the pin that goes to the circuit
pin_to_circuit = 7
buzzer = 11


def setup(pin):
    global BuzzerPin
    BuzzerPin = pin
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(BuzzerPin, GPIO.OUT)
    GPIO.output(BuzzerPin, GPIO.HIGH)

def rc_time (pin_to_circuit):
    count = 0
  
    #Output on the pin for 
    GPIO.setup(pin_to_circuit, GPIO.OUT)
    GPIO.output(pin_to_circuit, GPIO.LOW)
    time.sleep(0.1)

    #Change the pin back to input
    GPIO.setup(pin_to_circuit, GPIO.IN)
  
    #Count until the pin goes high
    while (GPIO.input(pin_to_circuit) == GPIO.LOW):
        count += 1

    return count

#Catch when script is interupted, cleanup correctly
try:
    setup(buzzer)
    # Main loop
    while True:
        lightVal = rc_time(pin_to_circuit) 
        print(lightVal)
        if(lightVal < 10):
            GPIO.output(BuzzerPin, GPIO.LOW)
            #buzzer.on()
        else:
            GPIO.output(BuzzerPin, GPIO.HIGH)
            #buzzer.off()
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()#!/usr/local/bin/python


