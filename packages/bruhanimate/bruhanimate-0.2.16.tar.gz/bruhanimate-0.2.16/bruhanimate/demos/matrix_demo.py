from bruhanimate.bruhscreen import Screen
from bruhanimate.bruhrenderer import EffectRenderer

import os
import sys

os.system(" ")


def matrix(screen):
    renderer = EffectRenderer(
        screen=screen,
        frames=float("inf"),
        time=0.05,
        effect_type="matrix",
        background=" ",
        transparent=False,
    )

    renderer.run()


def run():
    Screen.show(matrix)


if __name__ == "__main__":
    run()
