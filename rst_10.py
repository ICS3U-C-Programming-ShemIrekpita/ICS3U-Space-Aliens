import stage
import ugame
import time
import random
import constants


def splash_scene():
    # play coin sound
    coin_sound = open("coin.wav", "rb")
    ugame.audio.stop()
    ugame.audio.mute(False)
    ugame.audio.play(coin_sound)

    image_bank_background = stage.Bank.from_bmp16("mt_game_studio.bmp")

    background = stage.Grid(
        image_bank_background,
        constants.SCREEN_GRID_X,
        constants.SCREEN_GRID_Y
    )

    # logo tiles
    background.tile(2, 2, 0)
    background.tile(3, 2, 1)
    background.tile(4, 2, 2)
    background.tile(5, 2, 3)
    background.tile(6, 2, 4)

    background.tile(3, 3, 5)
    background.tile(4, 3, 6)
    background.tile(5, 3, 7)
    background.tile(6, 3, 8)

    background.tile(3, 4, 9)
    background.tile(4, 4, 10)
    background.tile(5, 4, 11)
    background.tile(6, 4, 12)

    background.tile(4, 5, 13)
    background.tile(5, 5, 14)

    game = stage.Stage(ugame.display, 60)
    game.layers = [background]
    game.render_block()

    time.sleep(2)
    menu_scene()


def menu_scene():
    image_bank_background = stage.Bank.from_bmp16("mt_game_studio.bmp")

    background = stage.Grid(
        image_bank_background,
        constants.SCREEN_GRID_X,
        constants.SCREEN_GRID_Y
    )

    text = []

    title = stage.Text(
        width=29,
        height=12,
        font=None,
        palette=constants.RED_PALETTE
    )
    title.move(20, 10)
    title.text("MT Game Studios")
    text.append(title)

    prompt = stage.Text(
        width=29,
        height=12,
        font=None,
        palette=constants.RED_PALETTE
    )
    prompt.move(40, 110)
    prompt.text("PRESS START")
    text.append(prompt)

    game = stage.Stage(ugame.display, 60)
    game.layers = text + [background]
    game.render_block()

    while True:
        keys = ugame.buttons.get_pressed()
        if keys & ugame.K_START:
            game_scene()
        game.tick()


def game_scene():
    def show_alien():
        for alien in aliens:
            if alien.x < 0:
                alien.move(
                    random.randint(
                        constants.SPRITE_SIZE,
                        constants.SCREEN_X - constants.SPRITE_SIZE
                    ),
                    constants.OFF_TOP_SCREEN
                )
                break

    image_bank_background = stage.Bank.from_bmp16("space_aliens_background.bmp")
    image_bank_sprites = stage.Bank.from_bmp16("space_aliens.bmp")

    pew_sound = open("pew.wav", "rb")
    ugame.audio.stop()
    ugame.audio.mute(False)

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

    game = stage.Stage(ugame.display, 60)
    game.layers = lasers + [ship] + aliens + [background]
    game.render_block()

    a_button = constants.button_state["button_up"]

    while True:
        keys = ugame.buttons.get_pressed()

        if keys & ugame.K_O:
            if a_button == constants.button_state["button_up"]:
                a_button = constants.button_state["button_just_pressed"]
        else:
            a_button = constants.button_state["button_up"]

        if keys & ugame.K_LEFT and ship.x > 0:
            ship.move(ship.x - 2, ship.y)

        if keys & ugame.K_RIGHT and ship.x < constants.SCREEN_X - constants.SPRITE_SIZE:
            ship.move(ship.x + 2, ship.y)

        if a_button == constants.button_state["button_just_pressed"]:
            ugame.audio.play(pew_sound)
            for laser in lasers:
                if laser.x < 0:
                    laser.move(ship.x, ship.y)
                    break

        for laser in lasers:
            if laser.x > 0:
                laser.move(laser.x, laser.y - constants.LASER_SPEED)
                if laser.y < constants.OFF_TOP_SCREEN:
                    laser.move(constants.OFF_SCREEN_X, constants.OFF_SCREEN_Y)

        for alien in aliens:
            if alien.x > 0:
                alien.move(alien.x, alien.y + constants.ALIEN_SPEED)
                if alien.y > constants.SCREEN_Y:
                    alien.move(constants.OFF_SCREEN_X, constants.OFF_SCREEN_Y)
                    show_alien()

        game.render_sprites(lasers + [ship] + aliens)
        game.tick()


if __name__ == "__main__":
    splash_scene()
