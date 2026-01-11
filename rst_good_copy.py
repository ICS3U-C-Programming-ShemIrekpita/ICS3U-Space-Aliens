import stage
import ugame
import time
import random
import constants
import supervisor


# ------------------------
# Splash Scene
# ------------------------
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

    # create background grid
    background = stage.Grid(
        image_bank_background, constants.SCREEN_GRID_X, constants.SCREEN_GRID_Y
    )

    # used this program to split the image into tile:
    # https://ezgif.com/sprite-cutter/ezgif-5-818cdbcc3f66.png

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


# ------------------------
# Menu Scene
# ------------------------
def menu_scene():
    # this function is for the main game game_scene
    # image banks for circuitpython
    image_bank_background = stage.Bank.from_bmp16("mt_game_studio.bmp")

    # sets the background to image 0 in the bank
    background = stage.Grid(
        image_bank_background, constants.SCREEN_GRID_X, constants.SCREEN_GRID_Y
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

    # create a stage for the game
    game = stage.Stage(ugame.display, 60)

    # set the layers of all sprites
    # Because Text is already a list we do not need to place then inside brakests
    game.layers = text + [background]

    # renders the sprites
    game.render_block()

    # repeats game forever
    while True:
        # get user input
        keys = ugame.buttons.get_pressed()
        if keys & ugame.K_START != 0:
            game_scene()
        # wait until refresh rate finishes
        game.tick()


# ------------------------
# Game Over Scene
# ------------------------
def game_over_scene(final_score):
    # This function displays the game over scene with the final score.
    # Image bank for CircuitPython
    image_bank_2 = stage.Bank.from_bmp16("mt_game_studio.bmp")

    # Set the background grid
    background = stage.Grid(
        image_bank_2, constants.SCREEN_GRID_X, constants.SCREEN_GRID_Y
    )

    # Add text objects
    text = []

    # Display final score
    text1 = stage.Text(
        width=29, height=14, font=None, palette=constants.BLUE_PALETTE, buffer=None
    )
    text1.move(22, 20)
    text1.text("Final Score: {:0>2d}".format(final_score))
    text.append(text1)

    # Display GAME OVER message
    text2 = stage.Text(
        width=29, height=14, font=None, palette=constants.BLUE_PALETTE, buffer=None
    )
    text2.move(43, 60)
    text2.text("GAME OVER")
    text.append(text2)

    # Display instruction to restart or exit
    text3 = stage.Text(
        width=29, height=14, font=None, palette=constants.BLUE_PALETTE, buffer=None
    )
    text3.move(32, 110)
    text3.text("PRESS SELECT")
    text.append(text3)

    # Create a stage for the background to show up on
    # and set the frame rate to 60 FPS
    game = stage.Stage(ugame.display, constants.FPS)

    # Set the layers; items show up in order (text on top of background)
    game.layers = text + [background]

    # Render the background and initial location of sprites
    game.render_block()

    # Repeat forever, game loop
    while True:
        # Get user input
        keys = ugame.buttons.get_pressed()
        # Start button selected
        if keys & ugame.K_SELECT != 0:
            supervisor.reload()  # restart the program
        # Wait until refresh rate finishes
        game.tick()


# ------------------------
# Main Game Scene
# ------------------------
def game_scene():
    # this function is for the main game game_scene
    score = 0

    # Create and update the score text
    score_text = stage.Text(width=29, height=14)  # create text object
    score_text.clear()  # clear any previous text
    score_text.cursor(0, 0)  # set cursor position
    score_text.move(1, 1)  # move text to top-left of screen
    score_text.text("Score: {0}".format(score))  # display current score

    # image banks for circuitpython
    image_bank_background = stage.Bank.from_bmp16("space_aliens_background.bmp")
    image_bank_sprites = stage.Bank.from_bmp16("space_aliens.bmp")

    # button states
    a_button = constants.button_state["button_up"]
    b_button = constants.button_state["button_up"]
    start_button = constants.button_state["button_up"]
    select_button = constants.button_state["button_up"]

    # Get sound ready
    pew_sound = open("pew.wav", "rb")  # laser shooting sound
    boom_sound = open("boom.wav", "rb")  # alien explosion sound
    crash_sound = open("crash.wav", "rb")  # ship collision sound

    # Set up audio
    sound = ugame.audio
    sound.stop()  # stop any currently playing sounds
    sound.mute(False)  # unmute audio

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

    # Aliens
    aliens = []
    for alien_number in range(constants.TOTAL_NUMBER_OF_alien):
        a_single_alien = stage.Sprite(
            image_bank_sprites,
            10,  # tile number of the alien in the sprite sheet
            constants.OFF_SCREEN_X,  # start off-screen
            constants.OFF_SCREEN_Y,
        )
        aliens.append(a_single_alien)

    # Lasers
    lasers = []
    for laser_number in range(constants.TOTAL_NUMBER_OF_LASERS):
        a_single_laser = stage.Sprite(
            image_bank_sprites,
            10,  # tile number of the laser in the sprite sheet
            constants.OFF_SCREEN_X,  # start off-screen
            constants.OFF_SCREEN_Y,
        )
        lasers.append(a_single_laser)

    # Show a new alien
    def show_alien():
        """
        Show an alien that is off-screen by moving it onto the screen.
        Only one alien appears per call.
        """
        for alien in aliens:
            if alien.x < 0:
                alien.move(
                    random.randint(
                        constants.SPRITE_SIZE,
                        constants.SCREEN_X - constants.SPRITE_SIZE,
                    ),
                    constants.OFF_TOP_SCREEN,
                )
                break

    show_alien()

    # create a stage for the game
    game = stage.Stage(ugame.display, 60)

    # set the layers of all sprites
    game.layers = [score_text] + lasers + [ship] + aliens + [background]

    # renders the sprites
    game.render_block()

    while True:
        keys = ugame.buttons.get_pressed()

        # A button handling
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

        # Move ship
        if keys & ugame.K_RIGHT != 0:
            ship.move(
                min(ship.x + 1, constants.SCREEN_X - constants.SPRITE_SIZE), ship.y
            )
        if keys & ugame.K_LEFT != 0:
            ship.move(max(ship.x - 1, 0), ship.y)

        # Fire laser
        if a_button == constants.button_state["button_just_pressed"]:
            for laser in lasers:
                if laser.x < 0:  # check if laser is off-screen
                    # Move laser to ship's current position
                    laser.move(ship.x, ship.y)
                    # Play shooting sound
                    sound.play(pew_sound)
                    break

        # Move lasers
        for laser in lasers:
            if laser.x > 0:
                laser.move(laser.x, laser.y - constants.LASER_SPEED)
                # If the laser goes off the top of the screen, hide it off-screen
                if laser.y < constants.OFF_TOP_SCREEN:
                    laser.move(constants.OFF_SCREEN_X, constants.OFF_SCREEN_Y)

        # Move aliens
        for alien in aliens:
            if alien.x > 0:
                alien.move(alien.x, alien.y + constants.ALIEN_SPEED)
                if alien.y > constants.SCREEN_Y:
                    alien.move(constants.OFF_SCREEN_X, constants.OFF_SCREEN_Y)
                    show_alien()

        # Check laser collisions with aliens
        for laser in lasers:
            if laser.x > 0:
                for alien in aliens:
                    if alien.x > 0 and stage.collide(
                        laser.x + 6,
                        laser.y + 2,
                        laser.x + 11,
                        laser.y + 12,
                        alien.x + 1,
                        alien.y,
                        alien.x + 15,
                        alien.y + 15,
                    ):
                        # Hide alien and laser
                        alien.move(constants.OFF_SCREEN_X, constants.OFF_SCREEN_Y)
                        laser.move(constants.OFF_SCREEN_X, constants.OFF_SCREEN_Y)
                        # Play explosion sound
                        sound.stop()
                        sound.play(boom_sound)
                        # Spawn new aliens
                        show_alien()
                        show_alien()
                        # Update score
                        score += 1
                        score_text.text("Score: {0}".format(score))

        # Check alien collisions with ship
        for alien in aliens:
            if alien.x > 0 and stage.collide(
                alien.x + 1,
                alien.y,
                alien.x + 15,
                alien.y + 15,
                ship.x,
                ship.y,
                ship.x + 15,
                ship.y + 15,
            ):
                # Alien hit the ship
                sound.stop()
                sound.play(crash_sound)
                time.sleep(3.0)
                game_over_scene(score)

        # Render all sprites
        game.render_sprites([score_text] + lasers + [ship] + aliens)
        game.tick()


# ------------------------
# Start Program
# ------------------------
if __name__ == "__main__":
    splash_scene()
