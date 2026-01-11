import stage
import ugame
import time
import random
import constants


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
    # image banks for circuitpython
    image_bank_background = stage.Bank.from_bmp16("mt_game_studio.bmp")

    background = stage.Grid(
        image_bank_mt_background, constants.SCREEN_GRID_X, constants.SCREEN_GRID_Y
    )
    background = stage.Grid(
        image_bank_mt_background, constants.SCREEN_GRID_X, constants.SCREEN_GRID_Y
    )
    # used this program to split the image into tile:

    #   https://ezgif.com/sprite-cutter/ezgif-5-818cdbcc3f66.png

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


def menu_scene():
    # this function is for the main game game_scene
    # image banks for circuitpython
    image_bank_background = stage.Bank.from_bmp16("mt_game_studio.bmp")
    # sets the background to image 0 in the bank
    background = stage.Grid(
        image_bank_mt_background, constants.SCREEN_GRID_X, constants.SCREEN_GRID_Y
    )
    background = stage.Grid(
        image_bank_mt_background, constants.SCREEN_GRID_X, constants.SCREEN_GRID_Y
    )
    # Add text objects
    # This section of the code tell is what colour it want the text
    # come out in and the font style and adds it to a list ans gives it is's location.
    text = []

    text1 = stage.Text(
        width=29, height=12, font=None, palette=constants.RED_PALETTE, buffer=None
    )
    text1.move(20, 10)
    text1.text("MT Game Studios")
    text.append(text1)

    text2 = stage.Text(
        width=29, height=12, font=None, palette=constants.RED_PALETTE, buffer=None
    )
    text2.move(40, 110)
    text2.text("PRESS START")
    text.append(text2)

    background = stage.Grid(
        image_bank_background, constants.SCREEN_GRID_X, constants.SCREEN_GRID_Y
    )
    # create a stage for the game
    game = stage.Stage(ugame.display, 60)

    # set the layers of all sprites
    # Because Text is already a list we do not need to place then inside brakests
    game.layers = text + [background]

    # renders the sprites
    game.render_block()

    # repeats game forever
    while True:
        keys = ugame.buttons.get_pressed()
        if keys & ugame.K_START != 0:
            game_scene()
        game.tick()


def game_scene():
    # this function is for the main game game_scene
    # image banks for circuitpython
    image_bank_background = stage.Bank.from_bmp16("space_aliens_background.bmp")
    image_bank_sprites = stage.Bank.from_bmp16("space_aliens.bmp")

    a_button = constants.button_state["button_up"]
    b_button = constants.button_state["button_up"]
    start_button = constants.button_state["button_up"]
    select_button = constants.button_state["button_up"]

    pew_sound = open("pew.wav", "rb")

    sound = ugame.audio
    sound.stop()
    sound.mute(False)

    # sets the background to image 0 in the bank
    background = stage.Grid(
        image_bank_background, constants.SCREEN_GRID_X, constants.SCREEN_GRID_Y
    )
    for x_location in range(constants.SCREEN_GRID_X):
        for y_location in range(constants.SCREEN_GRID_Y):
            tile_picked = random.randint(1, 3)
            background.tile(x_location, y_location, tile_picked)
    # create a sprite
    ship = stage.Sprite(
        image_bank_sprites, 5, 75, constants.SCREEN_Y - (2 * constants.SPRITE_SIZE)
    )
    alien = stage.Sprite(
        image_bank_sprites,
        9,
        int(constants.SCREEN_X / 2 - constants.SPRITE_SIZE / 2),
        16,
    )

    # create a stage for the game
    game = stage.Stage(ugame.display, 60)

    # set the layers of all sprites
    game.layers = [ship] + [alien] + [background]

    # renders the sprites
    game.render_block()

    # repeats game forever
    while True:
        keys = ugame.buttons.get_pressed()

        if keys & ugame.K_O != 0:

            if a_button == constants.button_state["button_up"]:
                a_button = constants.button_state["button_just_pressed"]
            elif a_button == constants.button_state["button_just_pressed"]:
                a_button = constants.button_state["button_still_pressed"]
        else:
            if a_button == constants.button_state["button_still_pressed"]:
                a_button = constants.button_state["button_released"]
            else:
                a_button = constants.button_state["button_up"]
        if keys & ugame.K_RIGHT:
            if ship.x <= constants.SCREEN_X - constants.SPRITE_SIZE:
                ship.move(ship.x + 1, ship.y)
            else:
                ship.move(constants.SCREEN_X - constants.SPRITE_SIZE, ship.y)
        if keys & ugame.K_LEFT:
            if ship.x >= 0:
                ship.move(ship.x - 1, ship.y)
            else:
                ship.move(0, ship.y)
        if keys & ugame.K_UP:
            pass
        if keys & ugame.K_DOWN:
            pass
        if a_button == constants.button_state["button_just_pressed"]:
            sound.play(pew_sound)
        game.render_sprites([ship] + [alien])
        game.tick()


if __name__ == "__main__":
    menu_scene()
