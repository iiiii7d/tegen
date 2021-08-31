import tegen
import blessed
from blessed.keyboard import Keystroke

game = tegen.Game()
scene = tegen.Scene()
term = blessed.Terminal()

class GameObj(tegen.objects.Sprite):
    direction = 1

    def update(self, g: tegen.Game):
        if self.x == 0: self.direction = 1
        elif self.x == term.width-2: self.direction = -1
        self.x += self.direction

class FpsText(tegen.objects.Text):
    def update(self, g: tegen.Game):
        self.text = "fps: "+str(g.fps())
class KeyText(tegen.objects.Text):
    def on_keyboard_press(self, g: tegen.Game, key: Keystroke):
        if key == 'q':
            g.end()
        elif key == 'a':
            g.objects['input'].trigger(g)

scene.add_object(GameObj(), "obj", 0, 1)
scene.add_object(FpsText("fps:"), "fps", 0, 0)
scene.add_object(KeyText(" ", back="00ff00"), "key", 0, 4)
scene.add_object(tegen.objects.TextInput(""), "input", 0, 6)

try:
    game.start(info_wait=1)
    game.add_keyboard_listener()
    game.load_scene(scene)
    #import time
    #time.sleep(15)
    #game.end()
except Exception:
    game.handle_error()
print("end")