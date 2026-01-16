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
    # this function is for the main game splash_scene
    # get coin sound ready
    coin_sound = open("coin.wav", "rb")
    # stop any currently playing sound
    ugame.audio.stop()
    # unmute audio
    ugame.audio.mute(False)
    # play coin sound
    ugame.audio.play(coin_sound)
    # image banks for circuit python
    image_bank_background = stage.Bank.from_bmp16("mt_game_studio.bmp")


    background = stage.Grid(
        image_bank_background, constants.SCREEN_GRID_X, constants.SCREEN_GRID_Y
    )
    background = stage.Grid(
        image_bank_background, constants.SCREEN_GRID_X, constants.SCREEN_GRID_Y
    )
    # used this program to split the image into tile:




    background.tile(2, 2, 0)  # blank white


    background.tile(3, 2, 1)


    background.tile(4, 2, 2)


    background.tile(5, 2, 3)


    background.tile(6, 2, 4)


    background.tile(7, 2, 0)  # blank white


    background.tile(2, 3, 0)  # blank white


    background.tile(3, 3, 5)


    background.tile(4, 3, 6)


    background.tile(5, 3, 7)


    background.tile(6, 3, 8)


    background.tile(7, 3, 0)  # blank white


    background.tile(2, 4, 0)  # blank white


    background.tile(3, 4, 9)


    background.tile(4, 4, 10)


    background.tile(5, 4, 11)


    background.tile(6, 4, 12)


    background.tile(7, 4, 0)  # blank white


    background.tile(2, 5, 0)  # blank white


    background.tile(3, 5, 0)


    background.tile(4, 5, 13)


    background.tile(5, 5, 14)


    background.tile(6, 5, 0)


    background.tile(7, 5, 0)  # blank white
    # create a stage for the game
    game = stage.Stage(ugame.display, 60)


    # set the layers of all sprites
    # Because Text is already a list we do not need to place then inside brakests
    game.layers = [background]


    # renders the sprites
    game.render_block()


    # repeats game forever
    # repeat forever (game loop)
    while True:
        # wait for 2 seconds
        time.sleep(2.0)
        # run the menu scene
        menu_scene()

# -------------------------
# MENU SCENE
# -------------------------
def menu_scene():
    image_bank = stage.Bank.from_bmp16("mt_game_studio.bmp")
    background = stage.Grid(
        image_bank,
        constants.SCREEN_GRID_X,
        constants.SCREEN_GRID_Y
    )

    text = []

    title = stage.Text(width=29, height=12, palette=constants.RED_PALETTE)
    title.move(20, 10)
    title.text("MT GAME STUDIOS")
    text.append(title)

    start = stage.Text(width=29, height=12, palette=constants.RED_PALETTE)
    start.move(40, 110)
    start.text("PRESS START")
    text.append(start)

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
    image_bank = stage.Bank.from_bmp16("mt_game_studio.bmp")
    background = stage.Grid(
        image_bank,
        constants.SCREEN_GRID_X,
        constants.SCREEN_GRID_Y
    )

    text = []

    over = stage.Text(width=29, height=12, palette=constants.RED_PALETTE)
    over.move(30, 30)
    over.text("GAME OVER")
    text.append(over)

    score_text = stage.Text(width=29, height=12, palette=constants.RED_PALETTE)
    score_text.move(10, 60)
    score_text.text("FINAL SCORE: {}".format(final_score))
    text.append(score_text)

    restart = stage.Text(width=29, height=12, palette=constants.RED_PALETTE)
    restart.move(10, 100)
    restart.text("PRESS SELECT")
    text.append(restart)

    game = stage.Stage(ugame.display, constants.FPS)
    game.layers = text + [background]
    game.render_block()

    while True:
        keys = ugame.buttons.get_pressed()
        if keys & ugame.K_SELECT:
            supervisor.reload()
        game.tick()


# -------------------------
# GAME SCENE
# -------------------------
def game_scene():
    score = 0
    score_dirty = True

    score_text = stage.Text(width=29, height=12, palette=constants.RED_PALETTE)
    score_text.move(1, 1)

    def update_score():
        score_text.clear()
        score_text.cursor(0, 0)
        score_text.text("Score: {}".format(score))

    def show_alien():
        for alien in aliens:
            if alien.x < 0:
                alien.move(
                    random.randint(
                        0,
                        constants.SCREEN_X - constants.SPRITE_SIZE
                    ),
                    constants.OFF_TOP_SCREEN
                )
                break

    image_bank_background = stage.Bank.from_bmp16("space_aliens_background.bmp")
    image_bank_sprites = stage.Bank.from_bmp16("space_aliens.bmp")

    background = stage.Grid(
        image_bank_background,
        constants.SCREEN_GRID_X,
        constants.SCREEN_GRID_Y
    )

    for x in range(constants.SCREEN_GRID_X):
        for y in range(constants.SCREEN_GRID_Y):
            background.tile(x, y, random.randint(1, 3))

    ship = stage.Sprite(
        image_bank_sprites,
        5,
        75,
        constants.SCREEN_Y - (2 * constants.SPRITE_SIZE)
    )

    aliens = []
    for _ in range(constants.TOTAL_NUMBER_OF_ALIENS):
        alien = stage.Sprite(
            image_bank_sprites,
            9,
            constants.OFF_SCREEN_X,
            constants.OFF_SCREEN_Y
        )
        aliens.append(alien)
        show_alien()

    lasers = []
    for _ in range(constants.TOTAL_NUMBER_OF_LASERS):
        laser = stage.Sprite(
            image_bank_sprites,
            10,
            constants.OFF_SCREEN_X,
            constants.OFF_SCREEN_Y
        )
        lasers.append(laser)

    pew_sound = open("pew.wav", "rb")
    boom_sound = open("boom.wav", "rb")

    ugame.audio.stop()
    ugame.audio.mute(False)

    game = stage.Stage(ugame.display, constants.FPS)
    game.layers = [score_text] + lasers + [ship] + aliens + [background]
    game.render_block()

    a_button = constants.button_state["button_up"]

    while True:
        keys = ugame.buttons.get_pressed()

        # Fire button
        if keys & ugame.K_O:
            if a_button == constants.button_state["button_up"]:
                a_button = constants.button_state["button_just_pressed"]
        else:
            a_button = constants.button_state["button_up"]

        # Ship movement
        if keys & ugame.K_LEFT and ship.x > 0:
            ship.move(ship.x - 2, ship.y)
        if keys & ugame.K_RIGHT and ship.x < constants.SCREEN_X - constants.SPRITE_SIZE:
            ship.move(ship.x + 2, ship.y)

        # Fire laser
        if a_button == constants.button_state["button_just_pressed"]:
            for laser in lasers:
                if laser.x < 0:
                    laser.move(ship.x, ship.y)
                    ugame.audio.play(pew_sound)
                    break

        # Move lasers
        for laser in lasers:
            if laser.x >= 0:
                laser.move(laser.x, laser.y - constants.LASER_SPEED)
                if laser.y < constants.OFF_TOP_SCREEN:
                    laser.move(constants.OFF_SCREEN_X, constants.OFF_SCREEN_Y)

        # Move aliens
        for alien in aliens:
            if alien.x >= 0:
                alien.move(alien.x, alien.y + constants.ALIEN_SPEED)

                # 🚨 SHIP COLLISION → GAME OVER
                if stage.collide(
                    ship.x, ship.y,
                    ship.x + constants.SPRITE_SIZE,
                    ship.y + constants.SPRITE_SIZE,
                    alien.x, alien.y,
                    alien.x + constants.SPRITE_SIZE,
                    alien.y + constants.SPRITE_SIZE
                ):
                    game_over_scene(score)
                    return

                # Alien escapes → score -1 ONLY
                if alien.y > constants.SCREEN_Y:
                    alien.move(constants.OFF_SCREEN_X, constants.OFF_SCREEN_Y)
                    show_alien()
                    score = max(0, score - 1)
                    score_dirty = True

        # Laser ↔ Alien collision
        for laser in lasers:
            if laser.x < 0:
                continue
            for alien in aliens:
                if alien.x < 0:
                    continue
                if stage.collide(
                    laser.x + 6, laser.y + 2,
                    laser.x + 11, laser.y + 12,
                    alien.x + 1, alien.y,
                    alien.x + 15, alien.y + 15
                ):
                    laser.move(constants.OFF_SCREEN_X, constants.OFF_SCREEN_Y)
                    alien.move(constants.OFF_SCREEN_X, constants.OFF_SCREEN_Y)
                    ugame.audio.play(boom_sound)
                    show_alien()
                    score += 1
                    score_dirty = True
                    break

        if score_dirty:
            update_score()
            score_dirty = False

        game.render_sprites(lasers + [ship] + aliens)
        game.tick()


# -------------------------
# START GAME
# -------------------------
if __name__ == "__main__":
    splash_scene()
