# Import the stage module for display and sprite handling
import stage

# Import ugame module to handle buttons, audio, and system functions
import ugame

# Import time module to use sleep for pauses
import time

# Import random module to generate random numbers
import random

# Import constants module for game constants like screen size, sprite size, speeds
import constants

# Import supervisor module to reload the program
import supervisor

# ------------------------------
# Functions to handle saving and loading
# ------------------------------


# Save the high score to a text file
def save_high_score(score):
    # Try reading the existing high score from a file
    try:
        with open("high_score.txt", "r") as file:
            high_score = int(file.read())  # convert text to integer
    except OSError:
        # If file does not exist, set high score to 0
        high_score = 0

    # Check if the current score is higher than the saved high score
    if score > high_score:
        # Write the new high score to the file
        with open("high_score.txt", "w") as file:
            file.write(str(score))
        # Return new high score
        return score
    # If not higher, return existing high score
    return high_score


# Save current game progress to a file
def save_progress(score):
    # Open file in write mode and save current score
    with open("save_game.txt", "w") as file:
        file.write(str(score))


# Load saved game progress from a file
def load_progress():
    # Try reading saved score
    try:
        with open("save_game.txt", "r") as file:
            saved_score = int(file.read())  # convert text to integer
        return saved_score
    except OSError:
        # If file does not exist, return None
        return None


# ------------------------------
# Splash Scene
# ------------------------------


# Function to display splash screen
def splash_scene():
    # Open the coin.wav sound file in binary mode
    coin_sound = open("coin.wav", "rb")
    # Stop any audio that is currently playing
    ugame.audio.stop()
    # Unmute audio
    ugame.audio.mute(False)
    # Play the coin sound
    ugame.audio.play(coin_sound)
    # Load image bank for background graphics
    image_bank_background = stage.Bank.from_bmp16("mt_game_studio.bmp")

    # Create a background grid using the image bank
    background = stage.Grid(
        image_bank_mt_background, constants.SCREEN_GRID_X, constants.SCREEN_GRID_Y
    )
    # Redundant grid creation (can be removed, but kept as per original)
    background = stage.Grid(
        image_bank_mt_background, constants.SCREEN_GRID_X, constants.SCREEN_GRID_Y
    )

    # Tile the background with specific tiles to form the splash screen
    background.tile(2, 2, 0)  # blank white tile
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

    # Create a stage object to show the background
    game = stage.Stage(ugame.display, 60)  # 60 frames per second

    # Set the layer order: background only
    game.layers = [background]

    # Render the background and sprites (sprites are none in this scene)
    game.render_block()

    # Main loop for splash scene
    while True:
        # Wait 2 seconds to show splash
        time.sleep(2.0)
        # After splash, move to menu scene
        menu_scene()


# ------------------------------
# Menu Scene
# ------------------------------


# Function to display the menu scene
def menu_scene():
    # Load image bank for menu background
    image_bank_background = stage.Bank.from_bmp16("mt_game_studio.bmp")
    # Create background grid
    background = stage.Grid(
        image_bank_mt_background, constants.SCREEN_GRID_X, constants.SCREEN_GRID_Y
    )
    # Redundant grid creation
    background = stage.Grid(
        image_bank_mt_background, constants.SCREEN_GRID_X, constants.SCREEN_GRID_Y
    )

    # Create text list for menu items
    text = []

    # Create and position the "MT Game Studios" title text
    text1 = stage.Text(
        width=29, height=12, font=None, palette=constants.RED_PALETTE, buffer=None
    )
    text1.move(20, 10)
    text1.text("MT Game Studios")
    text.append(text1)

    # Create and position the "PRESS START" prompt
    text2 = stage.Text(
        width=29, height=12, font=None, palette=constants.RED_PALETTE, buffer=None
    )
    text2.move(40, 110)
    text2.text("PRESS START")
    text.append(text2)

    # Try to display the high score
    high_score = 0
    try:
        with open("high_score.txt", "r") as file:
            high_score = int(file.read())
    except OSError:
        high_score = 0  # no high score yet

    # Create and position high score text
    text3 = stage.Text(
        width=29, height=12, font=None, palette=constants.RED_PALETTE, buffer=None
    )
    text3.move(20, 50)
    text3.text("High Score: {:0>2d}".format(high_score))
    text.append(text3)

    # Re-create background grid
    background = stage.Grid(
        image_bank_background, constants.SCREEN_GRID_X, constants.SCREEN_GRID_Y
    )

    # Create stage object for menu
    game = stage.Stage(ugame.display, 60)
    # Set layers: text on top of background
    game.layers = text + [background]
    # Render everything
    game.render_block()

    # Check if saved game exists
    saved_score = load_progress()
    resume_game = False
    if saved_score:
        # Display "Press START to Resume" if saved progress exists
        text_resume = stage.Text(
            width=29, height=12, font=None, palette=constants.RED_PALETTE, buffer=None
        )
        text_resume.move(20, 70)
        text_resume.text("Press START to Resume")
        text.append(text_resume)
        # Update layers and render again
        game.layers = text + [background]
        game.render_block()
        # Wait for START button press to resume
        while True:
            keys = ugame.buttons.get_pressed()
            if keys & ugame.K_START != 0:
                resume_game = True
                break
            game.tick()

    # Main menu loop
    while True:
        keys = ugame.buttons.get_pressed()
        if keys & ugame.K_START != 0:
            if resume_game:
                game_scene(saved_score)  # resume game with saved score
            else:
                game_scene(0)  # start fresh game
        game.tick()


# ------------------------------
# Game Scene
# ------------------------------


# Function for the main game scene
def game_scene(initial_score=0):
    # Initialize score with initial value or resume score
    score = initial_score

    # Create score text object
    score_text = stage.Text(width=29, height=14)  # create text object
    score_text.clear()  # clear any previous text
    score_text.cursor(0, 0)  # set cursor position
    score_text.move(1, 1)  # position top-left
    score_text.text("Score: {0}".format(score))  # display score

    # Function to spawn a single alien on screen
    def show_alien():
        # Iterate through all aliens
        for alien_number in range(len(aliens)):
            # If alien is off-screen
            if aliens[alien_number].x < 0:
                # Move alien onto screen at random x
                aliens[alien_number].move(
                    random.randint(
                        constants.SPRITE_SIZE,
                        constants.SCREEN_X - constants.SPRITE_SIZE,
                    ),
                    constants.OFF_TOP_SCREEN,
                )
                break  # only spawn one alien

    # ------------------------------
    # Image and Sound Setup
    # ------------------------------

    # Load background and sprite images
    image_bank_background = stage.Bank.from_bmp16("space_aliens_background.bmp")
    image_bank_sprites = stage.Bank.from_bmp16("space_aliens.bmp")

    # Initialize button states
    a_button = constants.button_state["button_up"]
    b_button = constants.button_state["button_up"]
    start_button = constants.button_state["button_up"]
    select_button = constants.button_state["button_up"]

    # Load sound effects
    pew_sound = open("pew.wav", "rb")  # laser
    boom_sound = open("boom.wav", "rb")  # alien explosion
    crash_sound = open("crash.wav", "rb")  # ship collision
    # Stop current audio and unmute
    sound = ugame.audio
    sound.stop()
    sound.mute(False)


# ------------------------------
# Game Over Scene
# ------------------------------
# This scene shows final score, "GAME OVER" text, and waits for SELECT to restart

# ------------------------------
# Start the game
# ------------------------------
if __name__ == "__main__":
    menu_scene()
