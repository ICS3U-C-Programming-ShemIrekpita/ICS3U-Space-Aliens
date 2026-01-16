#!/usr/bin/env python3
# Created by: Shem

import stage
import ugame
import time
import random
import constants
import supervisor

# -------------------------
# SPLASH SCENE
# -------------------------
def splash_scene():
    """Display splash screen for 2 seconds then go to menu."""
    coin_sound = open("coin.wav", "rb")
    ugame.audio.stop()
    ugame.audio.mute(False)
    ugame.audio.play(coin_sound)

    image_bank_background = stage.Bank.from_bmp16("mt_game_studio.bmp")
    background = stage.Grid(image_bank_background, constants.SCREEN_GRID_X, constants.SCREEN_GRID_Y)

    # Draw logo tiles
    tiles = [
        (3, 2, 1), (4, 2, 2), (5, 2, 3), (6, 2, 4),
        (3, 3, 5), (4, 3, 6), (5, 3, 7), (6, 3, 8),
        (3, 4, 9), (4, 4, 10), (5, 4, 11), (6, 4, 12),
        (4, 5, 13), (5, 5, 14)
    ]
    for tile in tiles:
        background.tile(tile[0], tile[1], tile[2])

    game = stage.Stage(ugame.display, constants.FPS)
    game.layers = [background]
    game.render_block()

    time.sleep(2)
    menu_scene()


# -------------------------
# MENU SCENE
# -------------------------
def menu_scene():
    """Display the main menu and wait for START button."""
    image_bank_background = stage.Bank.from_bmp16("mt_game_studio.bmp")
    background = stage.Grid(image_bank_background, constants.SCREEN_GRID_X, constants.SCREEN_GRID_Y)

    text = []

    title_text = stage.Text(29, 12, palette=constants.RED_PALETTE)
    title_text.move(20, 10)
    title_text.text("MT Game Studios")
    text.append(title_text)

    start_text = stage.Text(29, 12, palette=constants.RED_PALETTE)
    start_text.move(40, 110)
    start_text.text("PRESS START")
    text.append(start_text)

    game = stage.Stage(ugame.display, constants.FPS)
    game.layers = text + [background]
    game.render_block()

    while True:
        keys = ugame.buttons.get_pressed()
        if keys & ugame.K_START:
            game_scene()
        game.tick()


# -------------------------
# GAME OVER SCENE
# -------------------------
def game_over_scene(final_score):
    """Display the game over screen and wait for SELECT to restart."""
    image_bank = stage.Bank.from_bmp16("mt_game_studio.bmp")
    background = stage.Grid(image_bank, constants.SCREEN_GRID_X, constants.SCREEN_GRID_Y)

    text = []

    score_text = stage.Text(29, 14, palette=constants.BLUE_PALETTE)
    score_text.move(22, 20)
    score_text.text(f"Final Score: {final_score}")
    text.append(score_text)

    game_over = stage.Text(29, 14, palette=constants.BLUE_PALETTE)
    game_over.move(43, 60)
    game_over.text("GAME OVER")
    text.append(game_over)

    restart = stage.Text(29, 14, palette=constants.BLUE_PALETTE)
    restart.move(32, 110)
    restart.text("PRESS SELECT")
    text.append(restart)

    game = stage.Stage(ugame.display, constants.FPS)
    game.layers = text + [background]
    game.render_block()

    while True:
        if ugame.buttons.get_pressed() & ugame.K_SELECT:
            supervisor.reload()
        game.tick()


# -------------------------
# GAME SCENE
# -------------------------
def game_scene():
    """Main game loop: move ship, fire lasers, spawn aliens, and check collisions."""
    image_bank_background = stage.Bank.from_bmp16("space_aliens_background.bmp")
    image_bank_sprites = stage.Bank.from_bmp16("space_aliens.bmp")

    # Buttons
    a_button = constants.button_state["button_up"]

    # Sounds
    pew_sound = open("pew.wav", "rb")
    boom_sound = open("boom.wav", "rb")
    crash_sound = open("crash.wav", "rb")
    ugame.audio.stop()
    ugame.audio.mute(False)

    # Background
    background = stage.Grid(image_bank_background, constants.SCREEN_GRID_X, constants.SCREEN_GRID_Y)
    for x in range(constants.SCREEN_GRID_X):
        for y in range(constants.SCREEN_GRID_Y):
            background.tile(x, y, random.randint(1, 3))

    # Player ship
    ship = stage.Sprite(image_bank_sprites, 5, 75, constants.SCREEN_Y - (2 * constants.SPRITE_SIZE))

    # Score
    score = 0
    score_text = stage.Text(29, 14)
    score_text.move(1, 1)
    score_text.text(f"Score: {score}")

    # Aliens
    aliens = []
    for _ in range(constants.TOTAL_NUMBER_OF_ALIENS):
        alien = stage.Sprite(image_bank_sprites, 9, constants.OFF_SCREEN_X, constants.OFF_SCREEN_Y)
        aliens.append(alien)

    # Show one alien initially
    def show_alien():
        for alien in aliens:
            if alien.x < 0:
                alien.move(
                    random.randint(0, constants.SCREEN_X - constants.SPRITE_SIZE),
                    constants.OFF_TOP_SCREEN
                )
                break

    show_alien()

    # Lasers
    lasers = []
    for _ in range(constants.TOTAL_NUMBER_OF_LASERS):
        laser = stage.Sprite(image_bank_sprites, 10, constants.OFF_SCREEN_X, constants.OFF_SCREEN_Y)
        lasers.append(laser)

    # Stage
    game = stage.Stage(ugame.display, constants.FPS)
    game.layers = [score_text] + lasers + [ship] + aliens + [background]
    game.render_block()

    # -------------------------
    # MAIN GAME LOOP
    # -------------------------
    while True:
        keys = ugame.buttons.get_pressed()

        # -------------------------
        # Button states
        # -------------------------
        if keys & ugame.K_O:
            if a_button == constants.button_state["button_up"]:
                a_button = constants.button_state["button_just_pressed"]
        else:
            a_button = constants.button_state["button_up"]

        # -------------------------
        # Fire lasers
        # -------------------------
        if a_button == constants.button_state["button_just_pressed"]:
            ugame.audio.play(pew_sound)
            for laser in lasers:
                if laser.x < 0:
                    laser.move(ship.x, ship.y)
                    break

        # -------------------------
        # Move ship
        # -------------------------
        if keys & ugame.K_LEFT and ship.x > 0:
            ship.move(ship.x - constants.SPRITE_MOVEMENT_SPEED, ship.y)
        if keys & ugame.K_RIGHT and ship.x < constants.SCREEN_X - constants.SPRITE_SIZE:
            ship.move(ship.x + constants.SPRITE_MOVEMENT_SPEED, ship.y)

        # -------------------------
        # Move lasers
        # -------------------------
        for laser in lasers:
            if laser.x > 0:
                laser.move(laser.x, laser.y - constants.LASER_SPEED)
                if laser.y < constants.OFF_TOP_SCREEN:
                    laser.move(constants.OFF_SCREEN_X, constants.OFF_SCREEN_Y)

        # -------------------------
        # Move aliens
        # -------------------------
        for alien in aliens:
            if alien.x > 0:
                alien.move(alien.x, alien.y + constants.ALIEN_SPEED)
                if alien.y > constants.SCREEN_Y:
                    alien.move(constants.OFF_SCREEN_X, constants.OFF_SCREEN_Y)
                    show_alien()

        # -------------------------
        # Laser-alien collisions
        # -------------------------
        for laser in lasers:
            for alien in aliens:
                if laser.x > 0 and alien.x > 0:
                    if stage.collide(
                        laser.x, laser.y, laser.x + 15, laser.y + 15,
                        alien.x, alien.y, alien.x + 15, alien.y + 15
                    ):
                        laser.move(constants.OFF_SCREEN_X, constants.OFF_SCREEN_Y)
                        alien.move(constants.OFF_SCREEN_X, constants.OFF_SCREEN_Y)
                        ugame.audio.play(boom_sound)
                        score += 1
                        score_text.text(f"Score: {score}")
                        show_alien()

        # -------------------------
        # Alien-ship collisions
        # -------------------------
        for alien in aliens:
            if alien.x > 0:
                if stage.collide(
                    alien.x, alien.y, alien.x + 15, alien.y + 15,
                    ship.x, ship.y, ship.x + 15, ship.y + 15
                ):
                    ugame.audio.play(crash_sound)
                    time.sleep(1)
                    game_over_scene(score)

        game.render_sprites(lasers + [ship] + aliens)
        game.tick()


# -------------------------
# START GAME
# -------------------------
if __name__ == "__main__":
    splash_scene()
