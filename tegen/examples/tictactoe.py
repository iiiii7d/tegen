# Example code for tegen: Tic Tac Toe, by 7d
# Enjoy my shoddy code :)
import os
import sys
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
                                       fore=[[0xff3300]*5]*3)

class OPiece(tegen.objects.Sprite):
    pixels = tegen.pixel.from_2d_array(char=[' ███ ',
                                             '█   █',
                                             ' ███ '],
                                       fore=[[0x00ccff]*5]*3)


class Notif(tegen.objects.Text):
    turn = 1
    won = False
    x_locations = []
    o_locations = []

    def on_keyboard_press(self, g: tegen.Game, key: Keystroke):
        if self.won or key == "q":
            g.end()
            return
        if key not in [str(k) for k in range(1, 10)]: return
        piece_x = g.objects["label" + str(key)].x-2
        piece_y = g.objects["label" + str(key)].y-1
        piece = XPiece if self.turn == 1 else OPiece
        if "piece" + str(key) in g.objects.keys(): return
        game.add_object(piece(), "piece" + str(key), piece_x, piece_y)

        locations = self.x_locations if piece == XPiece else self.o_locations
        locations.append(int(key))
        if all(c in locations for c in [1, 2, 3]) or \
           all(c in locations for c in [4, 5, 6]) or \
           all(c in locations for c in [7, 8, 9]) or \
           all(c in locations for c in [1, 4, 7]) or \
           all(c in locations for c in [2, 5, 8]) or \
           all(c in locations for c in [3, 6, 9]) or \
           all(c in locations for c in [1, 5, 9]) or \
           all(c in locations for c in [3, 5, 7]):
            self.won = True
            self.text = "Player " + str(self.turn) + " wins! Press any key to exit"
        elif sorted(self.x_locations+self.o_locations) == list(range(1, 10)):
            self.fore = 0xffcc00
            self.won = True
            self.text = "Drawed. Press any key to exit"
        else:
            self.turn = 2 if self.turn == 1 else 1
            self.fore = 0x00ccff if self.turn == 2 else 0xff3300
            self.text = "Player " + str(self.turn) + "'s turn"
        with term.cbreak():
            while term.inkey(timeout=0.1) != "":
                pass


scene.add_object(Lines(), "lines", 0, 0)
scene.add_object(Notif("Player 1's turn", fore=0xff3300), "notif", 0, 12)
count = 1
for y in [1, 5, 9]:
    for x in [2, 8, 14]:
        scene.add_object(Label(str(count)), "label"+str(count), x, y)
        count += 1

try:
    game.start(info_wait=1)
    game.add_keyboard_listener()
    game.load_scene(scene)
except Exception:
    game.handle_error()