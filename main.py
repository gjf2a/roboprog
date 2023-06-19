#!/usr/bin/env python3
import time
from ev3dev2.motor import Motor, OUTPUT_A, OUTPUT_B
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import TouchSensor, UltrasonicSensor
from ev3dev2.sound import Sound
from ev3dev2.display import Display

screen = Display()
screen.text_grid("Hello")
screen.update()

spkr = Sound()
spkr.tone(440, 500)

left = Motor(OUTPUT_A)
right = Motor(OUTPUT_B)

left_bump = TouchSensor(INPUT_1)
right_bump = TouchSensor(INPUT_2)
sonar = UltrasonicSensor(INPUT_3)

start = time.time()

while time.time() - start < 5:
    if sonar.distance_centimeters < 30:
        left.on(-25)
        right.on(-25)
    else:
        if left_bump.is_pressed:
            left.on(-25)
        else:
            left.on(25)
        if right_bump.is_pressed:
            right.on(-25)
        else:
            right.on(25)

left.stop()
right.stop()