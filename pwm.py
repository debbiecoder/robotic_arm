#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  pwm.py
#  
import pigpio
import keyboard

PWM_PIN = 12
FREQ = 1000
duty_cycle = 100
step = 100

pi = pigpio.pi()
if not pi.connected:
    print("Failed to connect")
    exit()
    
pi.set_PWM_frequency(PWM_PIN, FREQ)

running = True

def increase_speed():
    global duty_cycle
    duty_cycle = min(duty_cycle + step, 255)
    pi.set_PWM_dutycycle(PWM_PIN, duty_cycle)
    print("Speed increased")


def decrease_speed():
    global duty_cycle
    duty_cycle = max(duty_cycle - step, 0)
    pi.set_PWM_dutycycle(PWM_PIN, duty_cycle)
    print("Speed decreased")

def stop_motor():
    global duty_cycle
    duty_cycle = 0
    pi.set_PWM_dutycycle(PWM_PIN, duty_cycle)
    print("Motor stopped")

while running:
    try:
        if keyboard.is_pressed("up"):
            increase_speed()
        elif keyboard.is_pressed("down"):
            decrease_speed()
        elif keyboard.is_pressed("left"):
            stop_motor()
        elif keyboard.is_pressed("q"):
            stop_motor()
            running = False
    except KeyboardInterrupt:
        stop_motor()
        break
        
pi.set_PWM_dutycycle(PWM_PIN, 0)
pi.stop()
            
