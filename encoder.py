#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  motor_movement.py
#  

'''
import RPi.GPIO as GPIO
import time
ENCODER_A = 17
ENCODER_B = 21

position = 0
last_state = 0

def encoder_position(channel):
    global position, last_state
    
    state_A = GPIO.input(ENCODER_A)
    state_B = GPIO.input(ENCODER_B)
    
    if state_A == state_B:
        position += 1
    else:
        position -= 1
        
    print(f"Position {position}")
    
GPIO.setmode(GPIO.BCM)
GPIO.setup(ENCODER_A, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(ENCODER_B, GPIO.IN, pull_up_down=GPIO.PUD_UP)
try:
    GPIO.add_event_detect(ENCODER_A, GPIO.BOTH, callback=encoder_position, bouncetime=10)
    GPIO.add_event_detect(ENCODER_B, GPIO.BOTH, callback=encoder_position, bouncetime=10)
    while True:
        pass
except Exception as e:
    print(f"Error: {e}")
finally:
    GPIO.cleanup()
    


try:
    while True:
        state_a = GPIO.input(ENCODER_A)
        state_b = GPIO.input(ENCODER_B)
        print(f"CH. A: {state_a}, Ch. B: {state_b}")
        time.sleep(0.1)
except KeyboardInterrupt:
    GPIO.cleanup()

'''


import pigpio 

ENCODER_A = 17
ENCODER_B = 21
ENCODER_RESOLUTION = (((1 + (46 / 17)) * (1 + (46 / 17))) * (1 + (46 / 11)) * 28) 


pi = None
encoder_val = 0
last_A = 0
last_B = 0

def encoder_callback(gpio, level, tick):
    global encoder_val, last_A, last_B
    
    state_A = pi.read(ENCODER_A)
    state_B = pi.read(ENCODER_B)
    
    if state_A != last_A:
        if state_A == state_B:
            encoder_val += 1 # Clockwise
        else:
            encoder_val -= 1 # Counterclockwise
    
    elif state_B != last_B:
        if state_A != state_B:
            encoder_val += 1 #Clockwise
        else:
            encoder_val -= 1 #Counterclockwise
    
    last_A = state_A
    last_B = state_B
    
    
def init_encoder():
    global pi
    pi = pigpio.pi()
    if not pi.connected:
        print("failed to connect to pigpio")
        exit(1)
    
    pi.set_mode(ENCODER_A, pigpio.INPUT)
    pi.set_mode(ENCODER_B, pigpio.INPUT)
    
    pi.set_pull_up_down(ENCODER_A, pigpio.PUD_UP)
    pi.set_pull_up_down(ENCODER_B, pigpio.PUD_UP)
    
def start_encoder_watch():
    global pi
    if pi == None:
        print("pi is None")
        return -1
    pi.callback(ENCODER_A, pigpio.EITHER_EDGE, encoder_callback)
    pi.callback(ENCODER_B, pigpio.EITHER_EDGE, encoder_callback)

def read_encoder_val():
    global encoder_val
    return encoder_val

def read_motor_pos():
    global encoder_val, ENCODER_RESOLUTION
    angle_deg = ((encoder_val / ENCODER_RESOLUTION) * 360)
    
    if angle_deg <= 0:
        angle_deg += 360
    elif angle_deg >= 360:
        angle_deg -= 360
    
    return angle_deg

def wait():
    try:
        print("Starting Encoder read")
        while True:
            print(f"Position: {read_motor_pos()} deg, Encoder_Val: {read_encoder_val()}")
            pass
    except Exception as E:
        print(f"Exception: {E}")

if __name__ == "__main__":
    init_encoder()
    start_encoder_watch()
    wait()
