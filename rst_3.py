#!/usr/bin/env python3
# Created by: Shem
# Created on: 1/10/2025
# This is my game
import stage


def game_scene():
    # this function is for the main game game_scene
    # image banks for circuitpython
    image_bank_background = stage.Bank.from_bmp16("space_aliens_background.bmp")
    # sets the background to image 0 in the bank
    background = stage.Grid(image_bank_background, 10, 8)

    # create a sprite
    ship = stage.Sprite(image_bank_sprites, 5, 75, 66)

    # set the layers of all sprites
    game.layers = [ship] + [background]

    # renders the sprites
    game.render_block()

    # repeats game forever
    while True:
        game.render_sprites([ship])
        game.tick()


if __name__ == "__main__":
    game_scene()
