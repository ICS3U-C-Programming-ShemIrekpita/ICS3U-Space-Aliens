#!/usr/bin/env python3
# Created by: Shem
# Import stage module to handle sprite graphics and grids
import stage
# Import ugame module to handle buttons, audio, and system functions
import ugame
# Import time module to add delays
import time
# Import random module to generate random positions for aliens
import random
# Import constants (your constants like screen size, sprite size)
import constants
# Import supervisor to allow reloading the program
import supervisor
# -------------------------
# SPLASH SCENE
# -------------------------
def splash_scene():
    # Open the coin sound effect file in read-binary mode
    coin_sound = open("coin.wav", "rb")
    # Stop any currently playing audio
    ugame.audio.stop()
    # Unmute the audio system
    ugame.audio.mute(False)
    # Play the coin sound
    ugame.audio.play(coin_sound)
    # Load the background image bank for the splash screen
    image_bank_background = stage.Bank.from_bmp16("mt_game_studio.bmp")
    # Create a grid for the background using the image bank
    background = stage.Grid(
        image_bank_background, constants.SCREEN_GRID_X, constants.SCREEN_GRID_Y
    )
    # Duplicate assignment (not needed but harmless)
    background = stage.Grid(
        image_bank_background, constants.SCREEN_GRID_X, constants.SCREEN_GRID_Y
    )
    # Manually set tiles in the grid to create the splash screen layout
    background.tile(2, 2, 0)  # Set tile at (2,2) to blank
    background.tile(3, 2, 1)  # Set tile at (3,2) to tile #1
    background.tile(4, 2, 2)  # Set tile at (4,2) to tile #2
    background.tile(5, 2, 3)  # Set tile at (5,2) to tile #3
    background.tile(6, 2, 4)  # Set tile at (6,2) to tile #4
    background.tile(7, 2, 0)  # Set tile at (7,2) to blank
    background.tile(2, 3, 0)  # Blank tile
    background.tile(3, 3, 5)  # Tile #5
    background.tile(4, 3, 6)  # Tile #6
    background.tile(5, 3, 7)  # Tile #7
    background.tile(6, 3, 8)  # Tile #8
    background.tile(7, 3, 0)  # Blank tile
    background.tile(2, 4, 0)  # Blank tile
    background.tile(3, 4, 9)  # Tile #9
    background.tile(4, 4, 10) # Tile #10
    background.tile(5, 4, 11) # Tile #11
    background.tile(6, 4, 12) # Tile #12
    background.tile(7, 4, 0)  # Blank tile
    background.tile(2, 5, 0)  # Blank tile
    background.tile(3, 5, 0)  # Blank tile
    background.tile(4, 5, 13) # Tile #13
    background.tile(5, 5, 14) # Tile #14
    background.tile(6, 5, 0)  # Blank tile
    background.tile(7, 5, 0)  # Blank tile
    # Create the Stage object for display with 60 FPS
    game = stage.Stage(ugame.display, 60)
    # Set the layers for rendering; only background for splash
    game.layers = [background]
    # Render everything once
    game.render_block()
    # Wait for 2 seconds then move to menu
    while True:
        time.sleep(2.0)
        menu_scene()  # Call the menu scene function
# -------------------------
# MENU SCENE
# -------------------------
def menu_scene():
    # Load the menu background image bank
    image_bank = stage.Bank.from_bmp16("mt_game_studio.bmp")
    # Create a grid for the background
    background = stage.Grid(
        image_bank,
        constants.SCREEN_GRID_X,
        constants.SCREEN_GRID_Y
    )
    # List to hold text objects
    text = []
    # Create title text object
    title = stage.Text(width=29, height=12, palette=constants.RED_PALETTE)
    title.move(20, 10)          # Move it to x=20, y=10
    title.text("MT GAME STUDIOS")  # Set the text
    text.append(title)          # Add to text list
    # Create start instruction text
    start = stage.Text(width=29, height=12, palette=constants.RED_PALETTE)
    start.move(40, 110)         # Position text
    start.text("PRESS START")   # Set text
    text.append(start)          # Add to text list
    # Create the Stage object for menu
    game = stage.Stage(ugame.display, constants.FPS)
    # Set layers: text objects first, then background
    game.layers = text + [background]
    game.render_block()         # Render once
    # Wait for user input
    while True:
        keys = ugame.buttons.get_pressed()  # Read pressed buttons
        if keys & ugame.K_START:           # If START button pressed
            game_scene()                   # Start main game
        game.tick()                         # Wait for next frame
# -------------------------
# GAME OVER SCENE
# -------------------------
def game_over_scene(final_score):
    # Load game over background image bank
    image_bank = stage.Bank.from_bmp16("mt_game_studio.bmp")
    # Create grid for background
    background = stage.Grid(
        image_bank,
        constants.SCREEN_GRID_X,
        constants.SCREEN_GRID_Y
    )
    # List to hold text objects
    text = []
    # Create "GAME OVER" text
    over = stage.Text(width=29, height=12, palette=constants.RED_PALETTE)
    over.move(30, 30)
    over.text("GAME OVER")
    text.append(over)
    # Create score text
    score_text = stage.Text(width=29, height=12, palette=constants.RED_PALETTE)
    score_text.move(10, 60)
    score_text.text("FINAL SCORE: {}".format(final_score))
    text.append(score_text)
    # Create instruction to restart
    restart = stage.Text(width=29, height=12, palette=constants.RED_PALETTE)
    restart.move(10, 100)
    restart.text("PRESS SELECT")
    text.append(restart)
    # Create Stage object for game over
    game = stage.Stage(ugame.display, constants.FPS)
    # Set layers: text first, then background
    game.layers = text + [background]
    game.render_block()         # Render once
    # Wait for restart input
    while True:
        keys = ugame.buttons.get_pressed()   # Get button presses
        if keys & ugame.K_SELECT:           # If SELECT pressed
            supervisor.reload()             # Reload the program
        game.tick()                          # Wait for next frame
# -------------------------
# GAME SCENE
# -------------------------
def game_scene():
    # Initialize score variable
    score = 0
    # Initialize lives (2 extra lives)
    lives = 2
    # Flag to know when to update the score display
    score_dirty = True
    # Create text object to display score and lives
    score_text = stage.Text(width=29, height=12, palette=constants.RED_PALETTE)
    score_text.move(1, 1)  # Position at top-left
    # Function to update score and lives display
    def update_score_lives():
        score_text.clear()  # Clear previous text
        score_text.cursor(0, 0)
        # Display score and lives
        score_text.text("Score: {}  Lives: {}".format(score, lives))
    # Function to randomly place a new alien on the top of the screen
    def show_alien():
        for alien in aliens:
            if alien.x < 0:  # Only move aliens that are off-screen
                alien.move(
                    random.randint(
                        0,
                        constants.SCREEN_X - constants.SPRITE_SIZE  # Random X within screen
                    ),
                    constants.OFF_TOP_SCREEN  # Y position just above screen
                )
                break  # Only move one alien at a time
    # Load game background and sprite image banks
    image_bank_background = stage.Bank.from_bmp16("space_aliens_background.bmp")
    image_bank_sprites = stage.Bank.from_bmp16("space_aliens.bmp")
    # Create background grid for game
    background = stage.Grid(
        image_bank_background,
        constants.SCREEN_GRID_X,
        constants.SCREEN_GRID_Y
    )
    # Fill grid with random tiles
    for x in range(constants.SCREEN_GRID_X):
        for y in range(constants.SCREEN_GRID_Y):
            background.tile(x, y, random.randint(1, 3))
    # Create player's ship sprite
    ship = stage.Sprite(
        image_bank_sprites,
        5,  # Sprite index for ship
        75, # X position
        constants.SCREEN_Y - (2 * constants.SPRITE_SIZE)  # Y near bottom
    )
    # List to hold alien sprites
    aliens = []
    for _ in range(constants.TOTAL_NUMBER_OF_ALIENS):
        alien = stage.Sprite(
            image_bank_sprites,
            9,  # Alien sprite index
            constants.OFF_SCREEN_X,  # Start off-screen
            constants.OFF_SCREEN_Y
        )
        aliens.append(alien)  # Add alien to list
        show_alien()          # Place alien randomly
    # List to hold laser sprites
    lasers = []
    for _ in range(constants.TOTAL_NUMBER_OF_LASERS):
        laser = stage.Sprite(
            image_bank_sprites,
            10,  # Laser sprite index
            constants.OFF_SCREEN_X,
            constants.OFF_SCREEN_Y
        )
        lasers.append(laser)
    # Load sound effects
    pew_sound = open("pew.wav", "rb")  # Laser fire sound
    boom_sound = open("boom.wav", "rb")  # Alien explosion sound
    # Stop audio and unmute
    ugame.audio.stop()
    ugame.audio.mute(False)
    # Create Stage object for game with all sprites
    game = stage.Stage(ugame.display, constants.FPS)
    # Layers: score, lasers, ship, aliens, background
    game.layers = [score_text] + lasers + [ship] + aliens + [background]
    game.render_block()  # Render everything
    # Track fire button state
    a_button = constants.button_state["button_up"]
    # Main game loop
    while True:
        # Read pressed buttons
        keys = ugame.buttons.get_pressed()
        # Fire button logic
        if keys & ugame.K_O:
            if a_button == constants.button_state["button_up"]:
                a_button = constants.button_state["button_just_pressed"]
        else:
            a_button = constants.button_state["button_up"]
        # Ship movement with screen wrap
        if keys & ugame.K_LEFT:
            ship.move(ship.x - 2, ship.y)  # Move left
        if keys & ugame.K_RIGHT:
            ship.move(ship.x + 2, ship.y)  # Move right
        if ship.x < -constants.SPRITE_SIZE:  # Wrap left
            ship.move(constants.SCREEN_X, ship.y)
        elif ship.x > constants.SCREEN_X:   # Wrap right
            ship.move(-constants.SPRITE_SIZE, ship.y)
        # Fire laser if button pressed
        if a_button == constants.button_state["button_just_pressed"]:
            for laser in lasers:
                if laser.x < 0:  # Only fire lasers that are off-screen
                    laser.move(ship.x, ship.y)  # Set laser position to ship
                    ugame.audio.play(pew_sound) # Play laser sound
                    break
        # Move lasers upward
        for laser in lasers:
            if laser.x >= 0:  # Only move active lasers
                laser.move(laser.x, laser.y - constants.LASER_SPEED)
                if laser.y < constants.OFF_TOP_SCREEN:
                    # Remove laser if it goes off-screen
                    laser.move(constants.OFF_SCREEN_X, constants.OFF_SCREEN_Y)
        # Move aliens downward
        for alien in aliens:
            if alien.x >= 0:  # Only move active aliens
                alien.move(alien.x, alien.y + constants.ALIEN_SPEED)
                # Ship collision → lose a life
                if stage.collide(
                    ship.x, ship.y,
                    ship.x + constants.SPRITE_SIZE,
                    ship.y + constants.SPRITE_SIZE,
                    alien.x, alien.y,
                    alien.x + constants.SPRITE_SIZE,
                    alien.y + constants.SPRITE_SIZE
                ):
                    lives -= 1                  # Decrease life
                    alien.move(constants.OFF_SCREEN_X, constants.OFF_SCREEN_Y)  # Remove alien
                    show_alien()                # Spawn new alien
                    score_dirty = True
                    if lives < 0:               # If no lives left
                        game_over_scene(score)  # Game over
                        return
                # Alien escapes → deduct score
                if alien.y > constants.SCREEN_Y:
                    alien.move(constants.OFF_SCREEN_X, constants.OFF_SCREEN_Y)
                    show_alien()
                    score = max(0, score - 1)   # Prevent negative score
                    score_dirty = True
        # Check laser collisions with aliens
        for laser in lasers:
            if laser.x < 0:  # Skip inactive lasers
                continue
            for alien in aliens:
                if alien.x < 0:  # Skip inactive aliens
                    continue
                if stage.collide(
                    laser.x + 6, laser.y + 2,
                    laser.x + 11, laser.y + 12,
                    alien.x + 1, alien.y,
                    alien.x + 15, alien.y + 15
                ):
                    # Collision detected → remove laser and alien
                    laser.move(constants.OFF_SCREEN_X, constants.OFF_SCREEN_Y)
                    alien.move(constants.OFF_SCREEN_X, constants.OFF_SCREEN_Y)
                    ugame.audio.play(boom_sound)  # Play explosion sound
                    show_alien()                  # Spawn new alien
                    score += 1                     # Increase score
                    score_dirty = True
                    break
        # Update score display if needed
        if score_dirty:
            update_score_lives()
            score_dirty = False

        # Render all sprites
        game.render_sprites(lasers + [ship] + aliens)
        # Wait until next frame
        game.tick()

# -------------------------
# START GAME
# -------------------------
if __name__ == "__main__":
    splash_scene()  # Start with splash screen
