from pybricks.parameters import Port, Stop, Direction, Button, Color
import lib

line_space = 3

def wait_until_clear(ev3):
    while len(ev3.buttons.pressed()) > 0:
        pass


def mod_inc(n: int, m: int) -> int:
    return (n + 1) % m


def mod_dec(n: int, m: int) -> int:
    return (n - 1) % m


def menuShowAll(ev3, items: List[str]) -> int:
    wait_until_clear(ev3)
    current = 0
    down = False
    refresh(ev3, items, current)
    while True:
        pressed = ev3.buttons.pressed()
        if len(pressed) > 0:
            if not down:
                ev3.speaker.beep()
                down = True
                if Button.CENTER in pressed:
                    return current
                elif Button.UP in pressed:
                    current = mod_dec(current, len(items))
                    refresh(ev3, items, current)
                elif Button.DOWN in pressed:
                    current = mod_inc(current, len(items))
                    refresh(ev3, items, current)
        else:
            down = False


def refresh(ev3, items: List[str], current: int):
    ev3.screen.clear()
    for i, item in enumerate(items):
        fore, back = (Color.BLACK, Color.WHITE) if i != current else (Color.WHITE, Color.BLACK)
        ev3.screen.draw_text(0, i * (lib.TEXT_HEIGHT + line_space), item, text_color=fore, background_color=back)

         
def menuManyOptions(ev3, list_labels: List[str], multi_option_list: List[List[str]], choices=None) -> List[int]:
    wait_until_clear(ev3)
    choices = [0] * len(multi_option_list) if choices is None else choices
    row = 0
    down = False
    refreshMany(ev3, list_labels, multi_option_list, row, choices)
    while True:
        pressed = ev3.buttons.pressed()
        if len(pressed) > 0:
            if not down:
                ev3.speaker.beep()
                down = True
                if Button.CENTER in pressed:
                    break
                elif Button.UP in pressed:
                    row = mod_dec(row, len(multi_option_list))
                elif Button.DOWN in pressed:
                    row = mod_inc(row, len(multi_option_list))
                elif Button.LEFT in pressed:
                    choices[row] = mod_dec(choices[row], len(multi_option_list[row]))
                elif Button.RIGHT in pressed:
                    choices[row] = mod_inc(choices[row], len(multi_option_list[row]))
                refreshMany(ev3, list_labels, multi_option_list, row, choices)
        else:
            down = False

    lib.waitNonePressed(ev3)
    return [multi_option_list[i][choices[i]] for i in range(len(choices))]


def refreshMany(ev3, list_labels: List[str], multi_option_list: List[List[str]], row: int, options: List[int]):
    ev3.screen.clear()
    for i, opt_list in enumerate(multi_option_list):
        fore, back = (Color.BLACK, Color.WHITE) if i != row else (Color.WHITE, Color.BLACK)
        text = list_labels[i] + ":" + str(multi_option_list[i][options[i % len(options)]])
        ev3.screen.draw_text(0, i * (lib.TEXT_HEIGHT + line_space), text, text_color=fore, background_color=back)