#!/usr/bin/env python3
# Created by: shem
# Created on: January/6/2025
# This constants file is for the Space Alien game
# PyBadge screen size is 160x128 and sprites are 16x16
import ugame
import stage
import constant

def game_scene():
    # This function is the game scene
    # Image banks for CircuitPython
    image_bank_background = stage.Bank.from_bmp16("space_aliens_background.bmp")
    image_bank_sprites = stage.Bank.from_bmp16("space_aliens.bmp")
    # Set the background (10x8 tiles of 16x16)
    background = stage.Grid(
        image_bank_background,
        constant.SCREEN_GRID_X,
        constant.SCREEN_GRID_Y,
    )
    # Create the ship sprite
    ship = stage.Sprite(
        image_bank_sprites, 5, 75, constant.SCREEN_Y - (2 * constant.SPRITE_SIZE)
    )
    # Create the stage and set FPS
    game = stage.Stage(ugame.display, constant.FPS)
    # Set layers (sprites in front of background)
    game.layers = [ship, background]
    # Render background and initial sprite position
    game.render_block()
    # Game loop
    while True:
        # Get user input
        keys = ugame.buttons.get_pressed()
        if keys & ugame.K_X:
            pass
        if keys & ugame.K_O:
            pass
        if keys & ugame.K_START:
            pass
        if keys & ugame.K_SELECT:
            pass
        if keys & ugame.K_RIGHT:
            if ship.x <= constant.SCREEN_X - constant.SPRITE_SIZE:
                ship.move(ship.x + 1, ship.y)
            else:
                ship.move(
                    constant.SCREEN_X - constant.SPRITE_SIZE,
                    ship.y,
                )
        if keys & ugame.K_LEFT:
            if ship.x >= 0:
                ship.move(ship.x - 1, ship.y)
            else:
                ship.move(0, ship.y)
        if keys & ugame.K_UP:
            pass
        if keys & ugame.K_DOWN:
            pass
        # Redraw sprite
        game.render_sprites([ship])
        game.tick()

if __name__ == "__main__":
        game_scene()