#!/usr/bin/env python3
# Created by: Shem
# Created on: 1/10/2025
# This is my game
import ugame
import stage
def game_scene():
    image_bank_background = stage.Bank.from_bmp16("space_aliens_background.bmp")

    image_bank_sprites = stage.Bank.from_bmp16("space_aliens.bmp")

    background = stage.Grid(image_bank_background, 10, 8)

    ship = stage.Sprite(image_bank_sprites, 5, 75, 66)
    game = stage.Stage(ugame.display, 60)
    game.layers = [ship] + [background]
    game.render_block()
    while True:
        game.render_sprites([ship])
        game.tick()
        pass

if __name__ == '__main__':
    game_scene()