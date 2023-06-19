from ev3dev2.display import Display

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


class Menu:
    def __init__(self, items):
        self.items = items
        self.current = 0

    def show(self):
        screen = Display()
        screen.clear()
        for i in range(len(self.items)):
            text = self.items[i]
            if i == self.current:
                text += '*'
            screen.draw.text((0, i), text)
        screen.update()

