import tegen
import time

game = tegen.Game()
scene = tegen.Scene()

class GameObj(tegen.objects.Sprite):
    pass

scene.add_object(GameObj(), "obj", 0, 1)

game.start()
game.load_scene(scene)
time.sleep(3)
game.end()
print("end")