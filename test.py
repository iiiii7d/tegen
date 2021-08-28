import tegen
import time

game = tegen.Game()
scene = tegen.Scene()

class GameObj(tegen.objects.Sprite):
    count = 0
    keys = ""

    def update(self, g: tegen.Game):
        if self.count % 2 == 0:
            self.x += 1
        else:
            self.x -= 1
        self.count += 1

    def on_keyboard_press(self, g: tegen.Game, key: str):
        self.keys += key
        if key == 'q':
            game.end()

class GameText(tegen.objects.Text):
    pass

scene.add_object(GameObj(), "obj", 0, 1)
scene.add_object(GameText("abc"), "text", 0, 5)
time.sleep(2)
game.start(info_wait=1)
try:
    game.add_keyboard_listener()
    game.load_scene(scene)
except Exception:
    game.handle_error()
print("end")