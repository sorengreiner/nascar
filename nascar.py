"""
Move Sprite With Keyboard

Simple program to show moving a sprite with the keyboard.
The sprite_move_keyboard_better.py example is slightly better
in how it works, but also slightly more complex.

Artwork from http://kenney.nl

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.sprite_move_keyboard
"""

import arcade
import os

SPRITE_SCALING = 1
GRAVITY = 0

ROAD_WIDTH = 600
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Move Sprite with Keyboard Example"

PIXEL_LENGTH = 0.025
CAR_SPEED_KPH = 200
CAR_SPEED_MPS = CAR_SPEED_KPH/3.6

MOVEMENT_SPEED = CAR_SPEED_MPS/PIXEL_LENGTH
MOVEMENT_SPEED_SIDE = 8/PIXEL_LENGTH



class Player(arcade.Sprite):

    def update(self):
        bounds_left = (SCREEN_WIDTH - ROAD_WIDTH)/2
        bounds_right = SCREEN_WIDTH - (SCREEN_WIDTH - ROAD_WIDTH)/2

        if self.left < bounds_left:
            self.left = bounds_left
        elif self.right > bounds_right:
            self.right = bounds_right

#        if self.bottom < 0:
#            self.bottom = 0
#        elif self.top > SCREEN_HEIGHT - 1:
#            self.top = SCREEN_HEIGHT - 1


class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self, width, height, title):
        """
        Initializer
        """

        # Call the parent class initializer
        super().__init__(width, height, title)

        # Set the working directory (where we expect to find files) to the same
        # directory this .py file is in. You can leave this out of your own
        # code, but it is needed to easily run the examples using "python -m"
        # as mentioned at the top of this program.
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        self.car_names = ["images/Nascar_Nr_2.png", "images/Nascar_Nr_20.png", "images/Nascar_Nr_9.png", "images/Nascar_Nr_49.png"] 

        self.zoom = 1.2
        self.camera_x = 0
        self.camera_y = 0

        # Variables that will hold sprite lists
        self.player_list = None
        # Set up the player info
        self.player_sprite = None
        # List that holds other cars
        self.car_list = None
        # List that holds road pieces
        self.road_list = None
        # Set the background color
        arcade.set_background_color(arcade.color.GRAY)

    def setup(self):
        """ Set up the game and initialize the variables. """

        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.car_list = arcade.SpriteList()
        self.road_list = arcade.SpriteList()

        # Set up the player
        self.player_sprite = Player("images/Nascar_Nr_20.png", SPRITE_SCALING)
        self.player_sprite.center_x = 350
        self.player_sprite.center_y = 250
        self.player_list.append(self.player_sprite)
          
        # Set up the other cars
        for y in range(4):
            car = arcade.Sprite(self.car_names[y], SPRITE_SCALING)
            car.center_x = SCREEN_WIDTH/2
            car.center_y = y*230 + 100
            self.car_list.append(car)					

        # Set up the road pieces
        for y in range(20):
            road = arcade.Sprite("images/Tileable_Asphalt_Texture.png", SPRITE_SCALING)
            road.center_x = SCREEN_WIDTH/2
            road.center_y = y*400
            self.road_list.append(road)					

    def on_draw(self):
        """
        Render the screen.
        """

        # This command has to happen before we start drawing
        arcade.start_render()

        left = self.zoom*(self.camera_x - SCREEN_WIDTH/2)
        right = self.zoom*(self.camera_x - SCREEN_WIDTH/2 + SCREEN_WIDTH)
        bottom = self.zoom*(self.camera_y - SCREEN_HEIGHT/2)
        top = self.zoom*(self.camera_y - SCREEN_HEIGHT/2 + SCREEN_HEIGHT)

        arcade.set_viewport(left, right, bottom, top)

        # Draw all the sprites.
        self.road_list.draw()
        self.player_list.draw()
        self.car_list.draw()

        arcade.set_viewport(0, SCREEN_WIDTH, 0, SCREEN_HEIGHT)

        arcade.draw_text("{} mph".format(int(CAR_SPEED_KPH*1.6)), 50, 50, arcade.color.WHITE, 32)
        

    def update(self, delta_time):
        """ Movement and game logic """

        self.player_sprite.center_x += self.player_sprite.change_x*delta_time
        self.player_sprite.center_y += self.player_sprite.change_y*delta_time

        # Let the camera follow the car center
        self.camera_x = self.player_sprite.center_x/self.zoom
        self.camera_y = self.player_sprite.center_y/self.zoom

        # Call update on all sprites (The sprites don't do much in this
        # example though.)
        self.player_list.update()

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        if key == arcade.key.UP:
            self.player_sprite.change_y = MOVEMENT_SPEED
        elif key == arcade.key.DOWN:
            self.player_sprite.change_y = -MOVEMENT_SPEED
        elif key == arcade.key.LEFT:
            self.player_sprite.change_x = -MOVEMENT_SPEED_SIDE
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = MOVEMENT_SPEED_SIDE

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0


def main():
    """ Main method """
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
