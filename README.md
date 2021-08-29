# tegen

[![Documentation Status](https://readthedocs.org/projects/tegen/badge/?version=latest)](https://tegen.readthedocs.io/en/latest/?badge=latest)
![PyPI version](https://img.shields.io/pypi/v/tegen)
![Github Version](https://img.shields.io/github/v/release/iiiii7d/tegen?include_prereleases)
![Python Versions](https://img.shields.io/pypi/pyversions/tegen)
![License](https://img.shields.io/github/license/iiiii7d/tegen)

![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/iiiii7d/tegen)
![GitHub repo size](https://img.shields.io/github/repo-size/iiiii7d/tegen)
![GitHub last commit](https://img.shields.io/github/last-commit/iiiii7d/tegen)
![GitHub Release Date](https://img.shields.io/github/release-date-pre/iiiii7d/tegen)
[![CodeFactor](https://www.codefactor.io/repository/github/iiiii7d/tegen/badge)](https://www.codefactor.io/repository/github/iiiii7d/tegen)

Terminal game engine for Python, made by 7d

**Latest release version: v0.0 (29/8/21)**
Changelogs: https://tegen.readthedocs.io/en/latest/changelog.html

**Documentation: https://tegen.readthedocs.io/en/latest/**

![images/tictactoe.gif](images/tictactoe.gif)

## Why 'Tegen'?
<u>**Te**</u>rminal <u>**G**</u>ame <u>**En**</u>gine

## Usage
```python
import tegen
from blessed.keyboard import Keystroke

game = tegen.Game()
scene = tegen.Scene()

class GameObj(tegen.objects.Sprite):
    direction = 1

    def on_keyboard_press(self, g: tegen.Game, key: Keystroke):
        if key == "a":
            self.x += 1

class GameText(tegen.objects.Text):
    def on_keyboard_press(self, g: tegen.Game, key: Keystroke):
        self.text += key
        if key == 'q':
            g.end()

scene.add_object(GameObj(), "obj", 0, 0)
scene.add_object(GameText("", back="ffa500"), "key", 0, 4)

try:
    game.start(info_wait=1)
    game.add_keyboard_listener()
    game.load_scene(scene)
except Exception:
    game.handle_error()
```

[Example tictactoe game](https://github.com/iiiii7d/tegen/blob/main/tegen/examples/tictactoe.py)