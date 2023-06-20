#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

import menus, lib

def main():
    ev3 = EV3Brick()

    motors = menus.menuManyOptions(ev3, ['A', 'B', 'C', 'D'], [['None', 'Motor']] * 4)
    sensors = menus.menuManyOptions(ev3, ['1', '2', '3', '4'], [['None', 'Touch', 'Sonar']] * 4)

    program = lib.Program(motors, sensors)
    start = False
    while not start:
        choice = menus.menuShowAll(ev3, ['Conditions', 'Actions', 'Tables', 'Start'])
        if choice == 0:
            pass
        elif choice == 1:
            pass
        elif choice == 2:
            pass
        elif choice == 3:
            start = True


def condition_menu(ev3, program):
    menus.wait_until_clear(ev3)
    rows = ['Name', 'Port', 'Op', 'Threshold']
    names = ["C" + str(i + 1) for i in range(program.num_conditions() + 1)]
    ports = program.live_sensors()
    name = 0
    row = 0
    down = False
    multi_option_list, choices = program.condition_option_list_and_choices(program.sensor_ports[0])
    menus.refreshMany(ev3, rows, multi_option_list, row, choices)
    while True:
        pressed = ev3.buttons.pressed()
        if len(pressed) > 0:
            if not down:
                ev3.speaker.beep()
                down = True
                if Button.CENTER in pressed:
                    break
                elif Button.UP in pressed:
                    row = mod_dec(row, len(rows))
                elif Button.DOWN in pressed:
                    row = mod_inc(row, len(rows))
                elif Button.LEFT in pressed:
                    choices[row] = mod_dec(choices[row], len(multi_option_list[row]))
                elif Button.RIGHT in pressed:
                    choices[row] = mod_inc(choices[row], len(multi_option_list[row]))
                multi_option_list, choices = program.condition_option_list_and_choices(program.sensor_ports[choices[1]])
                menus.refreshMany(ev3, rows, multi_option_list, row, choices)
        else:
            down = False

    lib.waitNonePressed(ev3)
    return lib.Condition()
    return choices



if __name__ == '__main__':
    main()