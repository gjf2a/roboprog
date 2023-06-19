class Condition:
    def __init__(self, sensor, checker, op, threshold):
        self.sensor = sensor
        self.checker = checker
        self.op = op
        self.threshold = threshold

    def met(self):
        return op(checker(sensor), threshold)


class Action:
    def __init__(self, motors, powers):
        self.motors = motors
        self.powers = powers

    def act(self):
        for i in range(len(self.motors)):
            self.motors[i].on(self.powers[i])


class Table:
    def __init__(self):
        self.pairs = []

    def add_pair(self, condition, action):
        self.pairs.append((condition, action))

    def choose(self):
        for (c, a) in self.pairs:
            if c.met():
                a.act()
                break


def menu(items):
    