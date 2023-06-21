#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

import menus, lib
from menus import mod_inc, mod_dec

motor_ports = ['A', 'B', 'C', 'D']
motor_port_options = [['None', 'Motor']] * len(motor_ports)
sensor_ports = ['S1', 'S2', 'S3', 'S4']
sensor_port_options = [['None', 'Touch', 'Sonar', 'Color']] * len(sensor_ports)

def main():
    ev3 = EV3Brick()
    ev3.speaker.beep()

    while True:
        motors = menus.menuManyOptions(ev3, motor_ports, motor_port_options)
        if any(motor != 'None' for motor in motors):
            break

    while True:
        sensors = menus.menuManyOptions(ev3, sensor_ports, sensor_port_options)
        if any(sensor != 'None' for sensor in sensors):
            break

    program = lib.Program(ev3, motors, sensors)
    while True:
        choice = menus.menuShowAll(ev3, ['Conditions', 'Actions', 'Rows', 'Start'])
        if choice == 0:
            condition_menu(ev3, program)
        elif choice == 1:
            action_menu(ev3, program)
        elif choice == 2:
            row_menu(ev3, program)
        elif choice == 3:
            print(program.conditions)
            print(program.actions)
            print(program.rows)
            program.execute(ev3)


def condition_menu(ev3, program):
    menus.wait_until_clear(ev3)
    rows = ['Name', 'Port', 'Op', 'Threshold']
    names = ["C" + str(i + 1) for i in range(max(1, program.num_conditions()))]
    ports = program.live_sensors()
    name = 0
    row = 0
    down = False
    refresh = True
    while True:
        if refresh:
            multi_option_list, choices = program.condition_option_list_and_choices(names[name])
            menus.refreshMany(ev3, rows, multi_option_list, row, choices)
            refresh = False
 
        pressed = ev3.buttons.pressed()
        if len(pressed) > 0:
            if not down:
                ev3.speaker.beep()
                down = True
                updated = None
                if Button.CENTER in pressed:
                    break
                elif Button.UP in pressed:
                    row = mod_dec(row, len(rows))
                elif Button.DOWN in pressed:
                    row = mod_inc(row, len(rows))
                elif Button.LEFT in pressed:
                    updated = mod_dec(choices[row], len(multi_option_list[row]))
                elif Button.RIGHT in pressed:
                    print("right", row, choices[row], program.num_conditions())
                    if row == 0 and choices[row] + 1 == len(names):
                        names.append("C" + str(len(names) + 1))
                        multi_option_list[row].append(names[-1])
                    updated = mod_inc(choices[row], len(multi_option_list[row]))
                if updated is not None:
                    if row == 0:
                        name = updated
                    elif row == 1:
                        program.change_condition_port(names[name], multi_option_list[1][updated])
                    elif row == 2:
                        program.conditions[names[name]].op = multi_option_list[2][updated]
                    elif row == 3:
                        program.conditions[names[name]].threshold = multi_option_list[3][updated]
                refresh = True
        else:
            down = False

    lib.waitNonePressed(ev3)


def action_menu(ev3, program):
    menus.wait_until_clear(ev3)
    rows = ['Name', 'Port', 'Deg/Sec']
    names = ["A" + str(i + 1) for i in range(max(1, program.num_actions()))]
    ports = program.live_motors()
    name = 0
    row = 0
    down = False
    refresh = True
    multi_option_list = [names, ports, lib.VELOCITIES]
    while True:
        if refresh:
            choices = program.action_choices(names[name])
            menus.refreshMany(ev3, rows, multi_option_list, row, choices)
            refresh = False

        pressed = ev3.buttons.pressed()
        if len(pressed) > 0:
            if not down:
                ev3.speaker.beep()
                down = True
                updated = None
                if Button.CENTER in pressed:
                    break
                elif Button.UP in pressed:
                    row = mod_dec(row, len(rows))
                elif Button.DOWN in pressed:
                    row = mod_inc(row, len(rows))
                elif Button.LEFT in pressed:
                    updated = mod_dec(choices[row], len(multi_option_list[row]))
                elif Button.RIGHT in pressed:
                    if row == 0 and choices[row] + 1 == len(names):
                        names.append("A" + str(len(names) + 1))
                    updated = mod_inc(choices[row], len(multi_option_list[row]))
                if updated is not None:
                    if row == 0:
                        name = updated
                    elif row == 1:
                        program.change_action_port(names[name], multi_option_list[1][updated])
                    elif row == 2:
                        program.actions[names[name]].velocity = multi_option_list[2][updated]
                refresh = True
        else:
            down = False

    lib.waitNonePressed(ev3)
        

def row_menu(ev3, program):
    menus.wait_until_clear(ev3)
    rows = ['Name', 'Condition', 'Inverted', 'Action1', 'Action2', 'Action3', 'Action4']
    names = ["R" + str(i + 1) for i in range(max(1, program.num_rows()))]
    name = 0
    row = 0
    down = False
    refresh = True
    multi_option_list = [names, sorted(program.conditions), ["False", "True"], program.action_list(), program.action_list(), program.action_list(), program.action_list()]
    while True:
        if refresh:
            choices = program.row_choices(names[name])
            menus.refreshMany(ev3, rows, multi_option_list, row, choices)
            refresh = False

        pressed = ev3.buttons.pressed()
        if len(pressed) > 0:
            if not down:
                ev3.speaker.beep()
                down = True
                updated = None
                if Button.CENTER in pressed:
                    break
                elif Button.UP in pressed:
                    row = mod_dec(row, len(rows))
                elif Button.DOWN in pressed:
                    row = mod_inc(row, len(rows))
                elif Button.LEFT in pressed:
                    updated = mod_dec(choices[row], len(multi_option_list[row]))
                elif Button.RIGHT in pressed:
                    if row == 0 and choices[row] + 1 == len(names):
                        names.append("R" + str(len(names) + 1))
                    updated = mod_inc(choices[row], len(multi_option_list[row]))
                if updated is not None:
                    if row == 0:
                        name = updated
                    elif row == 1:
                        program.rows[names[name]].condition = multi_option_list[1][updated]
                    elif row == 2:
                        program.rows[names[name]].invert = multi_option_list[2][updated]
                    elif row == 3:
                        program.rows[names[name]].action1 = multi_option_list[3][updated]
                    elif row == 4:
                        program.rows[names[name]].action2 = multi_option_list[4][updated]
                    elif row == 5:
                        program.rows[names[name]].action3 = multi_option_list[5][updated]
                refresh = True
        else:
            down = False

    lib.waitNonePressed(ev3)

if __name__ == '__main__':
    main()