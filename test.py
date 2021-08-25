import tegen
import time

game = tegen.Game()
scene = tegen.Scene()

class GameObj(tegen.Sprite):
    pass

scene.add_objects(GameObj())

game.start()
game.load_scene(scene)
time.sleep(3)
game.end()
print("end")