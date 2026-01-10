import ugame
import stage


def game_scene():
    # This function is the game_scene
    # image banks for circut python
    image_bank_background = stage.Bank.from_bmp16("space_aliens_background.bmp")
    image_bank_sprites = stage.Bank.from_bmp16("space_aliens.bmp")
    # set the back ground to image 0 in the bank
    # and size to (10x8 tiles of size 16x16)
    background = stage.Grid(image_bank_background, 10, 8)
    # a sprite that will update every frame.
    ship = stage.Sprite(image_bank_sprites, 5, 75, 66)
    # create a stage for the background to show up
    # and set frame rate to 60fps
    game = stage.Stage(ugame.display, 60)
    # set the layers , items show up in the order
    game.layers = [ship] + [background]
    # Render the back ground and initialis location of sprites
    game.render_block()
    # Repeat forever, game loop
    while True:
        # get user input
        keys = ugame.buttons.get_pressed()
        if keys & ugame.k_k:
            print("A")
        if keys & ugame.k_0:
            print("B")
        if keys & ugame.k_START:
            print("Start")
        if keys & ugame.k_SELECT:
            print("Select")
        if keys & ugame.K_RIGHT:
            ship.move(ship.x + 1, ship.y)
        if keys & ugame.K_LEFT:
            ship.move(ship.x - 1, ship.y)
        if keys & ugame.K_UP:
            ship.move(ship.x, ship.y - 1)
        if keys & ugame.K_DOWN:
            ship.move(ship.x, ship.y + 1)
        # update game logic

        # redraw sprite
        game.render_sprites([ship])
        game.tick()


if __name__ == "__main__":
    game_scene()
