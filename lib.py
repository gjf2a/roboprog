from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color

import time

TEXT_HEIGHT = 16

def waitNonePressed(ev3):
    while True:
        if len(ev3.buttons.pressed()) == 0:
            return


motor_ports = [Port.A, Port.B, Port.C, Port.D]
sensor_ports = [Port.S1, Port.S2, Port.S3, Port.S4]
CONDITION_ASPECTS = 4

def extract_port(port):
    return str(port).split('.')[1]


def extract_num(numbed):
    return int(numbed[1:]) - 1


class Program:
    def __init__(self, ev3, motors, sensors):
        self.motors = {}
        self.runners = {}
        self.motor_ports = []
        for i in range(len(motor_ports)):
            m = chr(ord('A') + i)
            if motors[i] == 'Motor':
                try:
                    self.motors[m] = Motor(motor_ports[i])
                    self.runners[m] = lambda v, m=m: self.motors[m].run(v)
                except:
                    ev3.screen.clear()
                    ev3.screen.draw_text(0, 0, "Error")
                    ev3.screen.draw_text(0, TEXT_HEIGHT, "Motor Port " + m)
                    while True: pass
                self.motor_ports.append(extract_port(motor_ports[i]))
            else:
                self.motors[m] = None

        self.sensors = {}
        self.readings = {}
        self.sensor_ports = []
        self.comparisons = {}
        self.thresholds = {}
        for i in range(len(sensor_ports)):
            s = 'S' + str(i + 1)
            try:
                if sensors[i] == 'Touch':
                    self.sensors[s] = TouchSensor(sensor_ports[i])
                    self.readings[s] = lambda s=s: 'Pressed' if self.sensors[s].pressed() else 'Open'
                    self.sensor_ports.append(extract_port(sensor_ports[i]))
                    self.comparisons[s] = ['==']
                    self.thresholds[s] = ['Pressed', 'Open']
                elif sensors[i] == 'Sonar':
                    self.sensors[s] = UltrasonicSensor(sensor_ports[i])
                    self.readings[s] = lambda s=s: str(self.sensors[s].distance())
                    self.sensor_ports.append(extract_port(sensor_ports[i]))
                    self.comparisons[s] = ['<', '>']
                    self.thresholds[s] = [str(i * 10) for i in range(1, 16)]
                elif sensors[i] == 'Color':
                    self.sensors[s] = ColorSensor(sensor_ports[i])
                    self.readings[s] = lambda s=s: str(self.sensors[s].color()).split('.')[-1]
                    self.sensor_ports.append(extract_port(sensor_ports[i]))
                    self.comparisons[s] = ['==']
                    self.thresholds[s] = ['BLACK', 'GREEN', 'BLUE', 'YELLOW', 'RED', 'WHITE', 'BROWN', 'None']
                else:
                    self.sensors[s] = None
                    self.comparisons[s] = None
                    self.thresholds[s] = None
            except:
                ev3.screen.clear()
                ev3.screen.draw_text(0, 0, "Error")
                ev3.screen.draw_text(0, TEXT_HEIGHT, "Sensor Port " + s)
                while True: pass

        self.conditions = {}
        self.actions = {}
        self.rows = {}

    def execute(self, ev3):
        waitNonePressed(ev3)
        while True:
            pressed = ev3.buttons.pressed()
            if len(pressed) > 0:
                for runner in self.runners.values():
                    runner(0)
                break
            readings = self.check_all_conditions()
            print("readings", readings)
            ev3.screen.clear()
            for i, s in enumerate(readings):
                ev3.screen.draw_text(0, i * TEXT_HEIGHT, str(readings[s][0]) + " " + str(readings[s][1]))
            for name in sorted(self.rows):
                row = self.rows[name]
                print("row", row)
                if row.is_selected(readings):
                    for action in row.actions(self):
                        print("action", action)
                        action.act(self)
                    break
            time.sleep(0.25)

        

    def check_all_conditions(self):
        return {p:v.check(self) for p,v in self.conditions.items()}

    def condition_option_list_and_choices(self, condition_name):
        if condition_name not in self.conditions:
            p = self.sensor_ports[0]
            self.conditions[condition_name] = Condition(condition_name, p, self.comparisons[p][0], self.thresholds[p][0])
        c = self.conditions[condition_name]
        multi = [
            [name for name in sorted(self.conditions)], 
            self.sensor_ports, 
            self.comparisons[c.port], 
            self.thresholds[c.port]
        ]
        return multi, c.choice_indices(self)

    def action_choices(self, action_name):
        if action_name not in self.actions:
            p = self.motor_ports[0]
            self.actions[action_name] = Action(action_name, p, '0')
        return self.actions[action_name].choice_indices(self)

    def row_choices(self, row_name):
        if row_name not in self.rows:
            self.rows[row_name] = Row(row_name, 'C1', 'False', 'None', 'None', 'None')
        return self.rows[row_name].choice_indices(self)

    def change_condition_port(self, condition_name, new_port):
        c = self.conditions[condition_name]
        c.port = new_port
        c.op = self.comparisons[new_port][0]
        c.threshold = self.thresholds[new_port][0]

    def change_action_port(self, action_name, new_port):
        a = self.actions[action_name]
        a.port = new_port
        a.velocity = '0'

    def condition_options(self, port):
        return [self.comparisons[port], self.thresholds[port]]

    def action_list(self):
        return ['None'] + sorted(self.actions)

    def live_motors(self):
        return [name for name in self.motors if self.motors[name] is not None]

    def live_sensors(self):
        return [name for name in self.sensors if self.sensors[name] is not None]

    def num_conditions(self):
        return len(self.conditions)

    def num_actions(self):
        return len(self.actions)

    def num_rows(self):
        return len(self.rows)


class Condition:
    def __init__(self, name, port, op, threshold):
        self.name = name
        self.port = port
        self.op = op
        self.threshold = threshold

    def __repr__(self):
        return '[' + ','.join(["'" + s + "'" for s in [self.name, self.port, self.op, self.threshold]]) + ']'

    def choice_indices(self, program):
        name_i = extract_num(self.name)
        port_i = program.sensor_ports.index(self.port)
        ops, ts = program.condition_options(self.port)
        op_i = ops.index(self.op)
        t_i = ts.index(self.threshold)
        return [name_i, port_i, op_i, t_i]

    def check(self, program):
        reading = program.readings[self.port]()
        expr = '"' + reading + '" ' + self.op + ' "' + self.threshold + '"'
        print(expr)
        return self.port, reading, eval(expr)


VELOCITIES = [str(180 * (i - 3)) for i in range(7)]


class Action:
    def __init__(self, name, port, velocity):
        self.name = name
        self.port = port
        self.velocity = velocity

    def __repr__(self):
        return '[' + ','.join(["'" + s + "'" for s in [self.name, self.port, self.velocity]]) + ']'

    def choice_indices(self, program):
        name_i = extract_num(self.name)
        port_i = program.motor_ports.index(self.port)
        v_i = VELOCITIES.index(self.velocity)
        return [name_i, port_i, v_i]

    def act(self, program):
        program.runners[self.port](int(self.velocity))


class Row:
    def __init__(self, name, condition, invert, action1, action2, action3):
        self.name = name
        self.condition = condition
        self.invert = invert
        self.action1 = action1
        self.action2 = action2
        self.action3 = action3

    def __repr__(self):
        return '[' + ','.join(["'" + s + "'" for s in [self.name, self.condition, self.invert, self.action1, self.action2, self.action3]]) + ']'

    def choice_indices(self, program):
        name_i = extract_num(self.name)
        condition_i = extract_num(self.condition)
        invert_i = 0 if self.invert == "False" else 1
        action_1 = program.action_list().index(self.action1)
        action_2 = program.action_list().index(self.action2)
        action_3 = program.action_list().index(self.action3)
        return [name_i, condition_i, invert_i, action_1, action_2, action_3]

    def is_selected(self, readings):
        if self.condition in readings:
            print(readings[self.condition][2])
            print(str(not eval(self.invert)))
        return self.condition in readings and readings[self.condition][2] != eval(self.invert)

    def actions(self, program):
        return [program.actions[action] for action in [self.action1, self.action2, self.action3] if action != 'None']