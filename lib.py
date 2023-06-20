from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color

TEXT_HEIGHT = 16

def waitNonePressed(ev3):
    while True:
        if len(ev3.buttons.pressed()) == 0:
            return


motor_ports = [Port.A, Port.B, Port.C, Port.D]
sensor_ports = [Port.S1, Port.S2, Port.S3, Port.S4]

class Program:
    def __init__(self, motors, sensors):
        self.motors = {}
        self.motor_ports = []
        for i in range(len(motor_ports)):
            m = chr(ord('A') + i)
            if motors[i] == 'Motor':
                self.motors[m] = Motor(motor_ports[i])
                self.motor_ports.append(motor_ports[i])
            else:
                self.motors[m] = None

        self.sensors = {}
        self.sensor_ports = []
        self.comparisons = {}
        self.thresholds = {}
        for i in range(len(sensor_ports)):
            s = 'S' + str(i + 1)
            if sensors[i] == 'Touch':
                self.sensors[s] = TouchSensor(sensor_ports[i])
                self.sensor_ports.append(sensor_ports[i])
                self.comparisons[s] = ['=']
                self.thresholds[s] = ['1', '0']
            elif sensors[i] == 'Sonar':
                self.sensors[s] = UltrasonicSensor(sensor_ports[i])
                self.sensor_ports.append(sensor_ports[i])
                self.comparisons[s] = ['<', '>']
                self.thresholds[s] = [str(i * 10) for i in range(1, 16)]
            else:
                self.sensors[s] = None
                self.comparisons[s] = None
                self.thresholds[s] = None

        self.conditions = {}
        self.actions = {}
        self.tables = {}

    def condition_option_list_and_choices(self, condition_name):
        if condition_name not in self.conditions:
            p = self.sensor_ports[0]
            self.conditions[condition_name] = Condition(condition_name, p, self.comparisons[p], self.thresholds[p])
        c = self.conditions[condition_name]
        multi = [[]] * len(self.conditions)
        for name in sorted(self.conditions):
            multi[0].append(name)
            p = self.conditions[name].port
            multi[1].append(p)
            multi[2].append(self.comparisons[p])
            multi[3].append(self.thresholds[p])
        return multi, c.choice_indices(self)

    def condition_options(self, port):
        return [self.comparisons[port], self.thresholds[port]]

    def live_motors(self):
        return [name for name in self.motors if self.motors[name] is not None]

    def live_sensors(self):
        return [name for name in self.sensors if self.sensors[name] is not None]

    def num_conditions(self):
        return len(self.conditions)

    def num_actions(self):
        return len(self.actions)

    def num_tables(self):
        return len(self.tables)


class Condition:
    def __init__(self, name, port, op, threshold):
        self.name = name
        self.port = port
        self.op = op
        self.threshold = threshold

    def choice_indices(self, program):
        name_i = int(self.name[1:]) - 1
        port_i = program.sensor_ports.index(self.port)
        ops, ts = program.condition_options(self.port)
        op_i = ops.index(self.op)
        t_i = ts.index(self.threshold)
        return [name_i, port_i, op_i, t_i]


