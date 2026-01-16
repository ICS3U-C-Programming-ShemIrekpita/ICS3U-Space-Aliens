#!/usr/bin/env python3
# Created by: Shem
# Created on: 1/10/2025
# This is my game

import ugame
import stage

def game_scene():
    # load image banks
    image_bank_background = stage.Bank.from_bmp16("space_aliens_background.bmp")
    image_bank_sprites = stage.Bank.from_bmp16("space_aliens.bmp")

    # create background
    background = stage.Grid(image_bank_background, 10, 8)

    # create player ship
    ship = stage.Sprite(image_bank_sprites, 5, 75, 66)

    # create stage
    game = stage.Stage(ugame.display, 60)
    game.layers = [ship, background]
    game.render_block()

    # game loop
    while True:
        # get user input
        keys = ugame.buttons.get_pressed()
        if keys & ugame.K_X:
            print("A")
        if keys & ugame.K_O:
            print("B")
        if keys & ugame.K_START:
            print("Start")
        if keys & ugame.K_SELECT:
            print("Select")
        if keys & ugame.K_RIGHT:
            ship.move(ship.x + 1, ship.y)
        if keys & ugame.K_LEFT:
            ship.move(ship.x - 1, ship.y)
        if keys & ugame.K_UP:
            ship.move(ship.x, ship.y - 1)
        if keys & ugame.K_DOWN:
            ship.move(ship.x, ship.y + 1)
        # update screen
        game.render_sprites([ship])
        game.tick()

if __name__ == "__main__":
    game_scene()
