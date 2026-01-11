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
    def show_alien():
        """
        Show an alien that is off-screen by moving it onto the screen.
        Only one alien appears per call.
        """
        for alien_number in range(len(aliens)):
            if aliens[alien_number].x < 0:
                aliens[alien_number].move(
                    random.randint(
                        constants.SPRITE_SIZE,
                        constants.SCREEN_X - constants.SPRITE_SIZE,
                    ),
                    constants.OFF_TOP_SCREEN,
                )
                break

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
    aliens = []
    # Create each laser and place it off-screen initially
    for alien_number in range(constants.TOTAL_NUMBER_OF_alien):
        a_single_alien = stage.Sprite(
            image_bank_sprites,
            10,  # tile number of the laser in the sprite sheet
            constants.OFF_SCREEN_X,  # start off-screen
            constants.OFF_SCREEN_Y,
        )
        alien.append(a_single_alien)
        # place one alien on the screen
        show_alien()
    # Create a list of lasers for shooting
    lasers = []
    # Create each laser and place it off-screen initially
    for laser_number in range(constants.TOTAL_NUMBER_OF_LASERS):
        a_single_laser = stage.Sprite(
            image_bank_sprites,
            10,  # tile number of the laser in the sprite sheet
            constants.OFF_SCREEN_X,  # start off-screen
            constants.OFF_SCREEN_Y,
        )
        lasers.append(a_single_laser)

    # create a stage for the game
    game = stage.Stage(ugame.display, 60)

    # set the layers of all sprites
    game.layers = lasers + [ship] + aliens + [background]

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
        # Update game logic
        # Play sound if A button was just pressed
        if a_button == constants.button_state["button_just_pressed"]:
            sound.play(pew_sound)
            # Fire a laser if there are any available off-screen
            for laser_number in range(len(lasers)):
                if lasers[laser_number].x < 0:  # check if laser is off-screen
                    # Move laser to ship's current position
                    lasers[laser_number].move(ship.x, ship.y)
                    # Play shooting sound
                    ugame.audio.play(pew_sound)
                    # Only fire one laser per button press
                    break
        # Each frame, move the lasers that have been fired
        for laser_number in range(len(lasers)):
            if lasers[laser_number].x > 0:  # check if laser is active (on-screen)
                # Move the laser upward by LASER_SPEED
                lasers[laser_number].move(
                    lasers[laser_number].x,
                    lasers[laser_number].y - constants.LASER_SPEED,
                )
        # Each frame, move the lasers that have been fired
        for laser_number in range(len(lasers)):
            # Only move lasers that are active (on-screen)
            if lasers[laser_number].x > 0:
                # Move the laser upward by LASER_SPEED
                lasers[laser_number].move(
                    lasers[laser_number].x,
                    lasers[laser_number].y - constants.LASER_SPEED,
                )
                # If the laser goes off the top of the screen, hide it off-screen
                if lasers[laser_number].y < constants.OFF_TOP_SCREEN:
                    lasers[laser_number].move(
                        constants.OFF_SCREEN_X, constants.OFF_SCREEN_Y
                    )
        # Each frame, move the aliens down the screen
        for alien_number in range(len(aliens)):
            # Only move aliens that are active (on-screen)
            if aliens[alien_number].x > 0:
                # Move the alien downward by ALIEN_SPEED
                aliens[alien_number].move(
                    aliens[alien_number].x,
                    aliens[alien_number].y + constants.ALIEN_SPEED,
                )
                # If the alien goes off the bottom of the screen, hide it off-screen
                if aliens[alien_number].y > constants.SCREEN_Y:
                    aliens[alien_number].move(
                        constants.OFF_SCREEN_X, constants.OFF_SCREEN_Y
                    )
            # Show a new alien after hiding this one
            show_alien()
        game.render_sprites(lasers + [ship] + alien)
        game.tick()


if __name__ == "__main__":
    menu_scene()
