# Example code for tegen: Tic Tac Toe, by 7d
# Enjoy my shoddy code :)
import os, sys
sys.path.insert(0, os.path.abspath('../..'))
import tegen
import blessed
from blessed.keyboard import Keystroke

game = tegen.Game()
scene = tegen.Scene()
term = blessed.Terminal()

class Lines(tegen.objects.Sprite):
    pixels = tegen.pixel.from_2d_array(char=['     █     █     ',
                                             '     █     █     ',
                                             '     █     █     ',
                                             '█████████████████',
                                             '     █     █     ',
                                             '     █     █     ',
                                             '     █     █     ',
                                             '█████████████████',
                                             '     █     █     ',
                                             '     █     █     ',
                                             '     █     █     '])

class Label(tegen.objects.Text):
    fore = 0xffa500

class XPiece(tegen.objects.Sprite):
    pixels = tegen.pixel.from_2d_array(char=['█   █',
                                             ' ███ ',
                                             '█   █'],
                                       fore=[[0xff3300]*5]*3,
                                       anchor='center')

class OPiece(tegen.objects.Sprite):
    pixels = tegen.pixel.from_2d_array(char=[' ███ ',
                                             '█   █',
                                             ' ███ '],
                                       fore=[[0x00ccff]*5]*3,
                                       anchor='center')


class Notif(tegen.objects.Text):
    turn = 1
    won = False

    def on_keyboard_press(self, g: tegen.Game, key: Keystroke):
        if self.won: g.end()
        if key not in list(range(1, 10)): return
        x = g.objects["label" + str(key)].x
        y = g.objects["label" + str(key)].y
        piece = XPiece if self.turn == 1 else OPiece
        if "piece" + str(key) in g.objects.keys(): return
        game.add_object(piece(), "piece" + str(key), x, y)

        piece_locations = [(obj.x, obj.y) for obj in filter(lambda o: issubclass(o, piece), g.objects.values())]
        if ((1, 2) and (1, 8) and (1, 14)) or \
           ((5, 2) and (5, 8) and (5, 14)) or \
           ((9, 2) and (9, 8) and (9, 14)) or \
           ((1, 2) and (5, 2) and (9, 2)) or \
           ((1, 8) and (5, 8) and (9, 8)) or \
           ((1, 14) and (5, 14) and (9, 14)) or \
           ((1, 2) and (5, 8) and (9, 14)) or \
           ((9, 2) and (5, 8) and (1, 14)) in piece_locations:
            self.won = True
            self.text = "Player " + str(self.turn) + " wins! Press any key to exit"

        self.turn = 2 if self.turn == 1 else 1
        self.fore = 0x00ccff if self.turn == 2 else 0xff3300
        self.text = "Player " + str(self.turn) + "'s turn"


scene.add_object(Lines(), "lines", 0, 0)
scene.add_object(Notif("Player 1's turn", fore=0xff3300), "notif", 0, 12)
count = 1
for y in [1, 5, 9]:
    for x in [2, 8, 14]:
        scene.add_object(Label(term.bold(str(count))), "label"+str(count), x, y)
        count += 1

try:
    game.start(info_wait=1)
    game.add_keyboard_listener()
    game.load_scene(scene)
except Exception:
    game.handle_error()