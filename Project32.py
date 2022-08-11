import arcade, random, os, time, math

# Global Variables
SPRITE_SCALING = 0.5
ENEMY_COUNT = 50
ENEMYBOMBER_COUNT = 25
SPRITE_NATIVE_SIZE = 128
SPRITE_SIZE = int(SPRITE_NATIVE_SIZE * SPRITE_SCALING)
MOVEMENT_SPEED = 2
SPRITE_SCALING_BULLET = 0.8
BULLET_SPEED = 5
EXPLOSION_TEXTURE_COUNT = 60
SPRITE_SCALING_COIN = 0.5
COIN_COUNT = 100

# Screen Setup
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 700
IMAGE_WIDTH = 800
SCROLL_SPEED = 2.5
SCREEN_TITLE = "PROJECT 32"


class MenuView(arcade.View):
    def on_show(self):
        self.background_list = arcade.SpriteList()
        self.background_sprite = arcade.Sprite("images\menu_template.png")
        self.background_sprite.center_x = IMAGE_WIDTH // 2
        self.background_sprite.center_y = SCREEN_HEIGHT // 2
        self.background_list.append(self.background_sprite)

    def on_draw(self):
        arcade.start_render()
        self.background_list.draw()
        arcade.draw_text("Menu", 550, 260, arcade.color.YELLOW, font_size=20)
        arcade.draw_text("Click anyhwere to continue", 590, 230,
                         arcade.color.YELLOW, font_size=20, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        game_view = InstructionView()
        self.window.show_view(game_view)


class InstructionView(arcade.View):
    def on_show(self):
        self.background_list = arcade.SpriteList()
        self.background_sprite = arcade.Sprite("images\menu_template.png")
        self.background_sprite.center_x = IMAGE_WIDTH // 2
        self.background_sprite.center_y = SCREEN_HEIGHT // 2
        self.background_list.append(self.background_sprite)

    def on_draw(self):
        arcade.start_render()
        self.background_list.draw()
        arcade.draw_text("Instructions", 550, 260, arcade.color.YELLOW, font_size=20)
        arcade.draw_text("""Use the WASD keys to control the plane
        Space to fire weapons
        Click anywhere to continue""", 590, 200,
                         arcade.color.YELLOW, font_size=20, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        game_view = GameView()
        self.window.show_view(game_view)


class Explosion(arcade.Sprite):  # Creates the explosion

    def __init__(self, texture_list):
        super().__init__("images/explosion/explosion0000.png")

        # Start at the firs frame
        self.current_texture = 0
        self.textures = texture_list

    def update(self):
        self.current_texture += 1
        if self.current_texture < len(self.textures):
            self.set_texture(self.current_texture)
        else:
            self.remove_from_sprite_lists()


class Enemy(arcade.Sprite):
    def update(self):
        # Move the enemy
        self.center_x -= 1


class EnemyBomber(Enemy):
    pass


class GameView(arcade.View):  # Main Aplication Class

    def __init__(self):  # Initliser
        super().__init__()

        self.frame_count = 0

        self.background_list = None
        self.player_list = None
        self.coin_list = None
        self.enemy_list = None
        self.enemy2_list = None
        self.bullet_list = None
        self.bullet2_list = None
        self.explosions_list = None
        self.score = 0

        # Hideing the mouse cursor
        # self.set_mouse_visible(False)

        # Pre-load anamation frames
        self.explosion_texture_list = []

        for i in range(EXPLOSION_TEXTURE_COUNT):
            texture_name = f"images/explosion/explosion{i:04d}.png"

            self.explosion_texture_list.append(arcade.load_texture(texture_name))

        self.setup()

    def setup(self):
        # Setting game background
        backgroundRan = random.randint(1, 4)
        if backgroundRan == 1:
            texture = ("images/tropicMap.png")
        elif backgroundRan == 2:
            texture = ("images/urbanMap.png")
        else:
            texture = ("images/deseartMap.png")

            # first background image
        self.background_list = arcade.SpriteList()
        self.background_sprite = arcade.Sprite(texture)
        self.background_sprite.center_x = IMAGE_WIDTH // 2
        self.background_sprite.center_y = SCREEN_HEIGHT // 2
        self.background_sprite.change_x = -SCROLL_SPEED

        self.background_list.append(self.background_sprite)

        # second background image
        self.background_sprite_2 = arcade.Sprite(texture)
        self.background_sprite_2.center_x = SCREEN_WIDTH + IMAGE_WIDTH // 2
        self.background_sprite_2.center_y = SCREEN_HEIGHT // 2
        self.background_sprite_2.change_x = -SCROLL_SPEED

        self.background_list.append(self.background_sprite_2)

        # Sprite Lists
        self.player_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.enemy2_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.bullet2_list = arcade.SpriteList()
        self.explosions_list = arcade.SpriteList()

        # Setting Up the Player
        self.score = 0
        self.player_sprite = arcade.Sprite("images/spitfire_top.png", SPRITE_SCALING)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 50
        self.player_list.append(self.player_sprite)
        self.player_health = 100

        # Setup Enemies
        for i in range(ENEMY_COUNT):
            enemy = Enemy("images/BF109_TOP.png", SPRITE_SCALING)

            # Enemy Positions
            enemy.center_x = random.randrange(900, 8000)
            enemy.center_y = random.randrange(SCREEN_HEIGHT)

            # Add to enemy list
            self.enemy_list.append(enemy)

            # Enemy Health
            self.enemy_health = 20

        for i in range(ENEMYBOMBER_COUNT):
            enemy2 = EnemyBomber("images/Bomber.png", SPRITE_SCALING)

            # Enemy Positions
            enemy2.center_x = random.randrange(900, 8000)
            enemy2.center_y = random.randrange(SCREEN_HEIGHT)

            # Add to enemy list
            self.enemy2_list.append(enemy2)

            # Enemy Health
            self.enemy2_health = 50

            # Create the coins
        for i in range(COIN_COUNT):
            # Create the coin instance

            coin = Enemy("images/Coin.png", SPRITE_SCALING_COIN)

            # Position the coin
            coin.center_x = random.randrange(900, 8000)
            coin.center_y = random.randrange(120, SCREEN_HEIGHT)

            # Add the coin to the lists
            self.coin_list.append(coin)

    def on_draw(self):

        arcade.start_render()
        # Draw background texture
        self.background_list.draw()

        # Draw Sprites
        self.player_list.draw()

        # Draw Enemies
        self.enemy_list.draw()
        self.enemy2_list.draw()

        # Draw Bullets
        self.bullet_list.draw()
        self.bullet2_list.draw()

        # Draw Explosions
        self.explosions_list.draw()

        # Draw Coins
        self.coin_list.draw()

        # Text Render
        arcade.draw_text(f"Score: {self.score}", 10, 20, arcade.color.WHITE, 14)
        arcade.draw_text(f"Health: {self.player_health}", 100, 20, arcade.color.WHITE, 14)

    def on_key_press(self, key, modifiers):  # Called whenever the user presses a key.
        # Player Movement
        if key == arcade.key.A:
            self.player_sprite.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.D:
            self.player_sprite.change_x = MOVEMENT_SPEED
        elif key == arcade.key.W:
            self.player_sprite.change_y = MOVEMENT_SPEED
        elif key == arcade.key.S:
            self.player_sprite.change_y = -MOVEMENT_SPEED
        elif key == arcade.key.SPACE:
            # Create a Bullet
            bullet = arcade.Sprite("images/bullet.png", SPRITE_SCALING_BULLET)
            # Bullet Speed
            bullet.change_x = BULLET_SPEED
            # Bullet Positiining
            bullet.center_x = (self.player_sprite.center_x + 9)
            bullet.bottom = (self.player_sprite.bottom + 24)
            # Add to list
            self.bullet_list.append(bullet)
            # Create a Bullet
            bullet2 = arcade.Sprite("images/bullet.png", SPRITE_SCALING_BULLET)
            # Bullet Speed
            bullet2.change_x = BULLET_SPEED
            # Bullet Positiining
            bullet2.center_x = (self.player_sprite.center_x + 9)
            bullet2.bottom = (self.player_sprite.bottom + 46)
            # Add to list
            self.bullet_list.append(bullet2)

    def on_key_release(self, key, modifiers):  # Called whenever a user releases a key.

        if key == arcade.key.A or key == arcade.key.D:
            self.player_sprite.change_x = 0
        elif key == arcade.key.W or key == arcade.key.S:
            self.player_sprite.change_y = 0

    def update(self, delta_time):  # All the logic to move, and the game logic goes here.

        self.frame_count += 1

        # Moveing Background
        if self.background_sprite.left == -IMAGE_WIDTH:
            self.background_sprite.center_x = SCREEN_WIDTH + IMAGE_WIDTH // 2

        if self.background_sprite_2.left == -IMAGE_WIDTH:
            self.background_sprite_2.center_x = SCREEN_WIDTH + IMAGE_WIDTH // 2

        self.background_list.update()

        # Player Movement
        self.player_list.update()

        # Moveing Enemies
        self.enemy_list.update()
        self.enemy2_list.update()

        # Bullet Movement
        self.bullet_list.update()
        self.bullet2_list.update()

        # Explosions
        self.explosions_list.update()

        # Coin
        self.coin_list.update()

        # Enemy game over senario

        for enemy in self.enemy_list:
            if enemy.left < 0:
                game_view = GameOverView()
                self.window.show_view(game_view)

        # Enemy2 aiming at player and game over senario
        # Loop through each enemy that we have
        for enemy2 in self.enemy2_list:

            # Position the start at the enemy's current location
            start_x = enemy2.center_x
            start_y = enemy2.center_y

            # Get the destination location for the bullet
            dest_x = self.player_sprite.center_x
            dest_y = self.player_sprite.center_y

            # Do math to calculate how to get the bullet to the destination.
            # Calculation the angle in radians between the start points
            # and end points. This is the angle the bullet will travel.
            x_diff = dest_x - start_x
            y_diff = dest_y - start_y
            angle = math.atan2(y_diff, x_diff)

            if enemy2.left < 0:
                game_view = GameOverView()
                self.window.show_view(game_view)

            # Shoot every 60 frames change of shooting each frame
            if self.frame_count % 60 == 0 and enemy2.center_x < 900:
                bullet2 = arcade.Sprite("images/bullet.png")
                bullet2.center_x = start_x
                bullet2.center_y = start_y

                # Angle the bullet sprite
                bullet2.angle = math.degrees(angle)

                # Taking into account the angle, calculate our change_x
                # and change_y. Velocity is how fast the bullet travels.
                bullet2.change_x = math.cos(angle) * BULLET_SPEED
                bullet2.change_y = math.sin(angle) * BULLET_SPEED

                self.bullet2_list.append(bullet2)

        # Loop through bullets to check for enemy collison
        for bullet in self.bullet_list:
            # Check for collison
            hit_list = arcade.check_for_collision_with_list(bullet, self.enemy_list)

            # If collison = true then remove the bullet
            if len(hit_list) > 0 and self.enemy_health == 0:
                explosion = Explosion(self.explosion_texture_list)
                explosion.center_x = hit_list[0].center_x
                explosion.center_y = hit_list[0].center_y
                self.explosions_list.append(explosion)

                bullet.remove_from_sprite_lists()

                # When a enemy is hit remove it from the game
                for enemy in hit_list:
                    enemy.remove_from_sprite_lists()
                    self.score += 10
                    self.enemy_health = 20

            elif len(hit_list) > 0:
                self.enemy_health -= 10
                bullet.remove_from_sprite_lists()

        for bullet in self.bullet_list:
            # Check for collison
            hit_list = arcade.check_for_collision_with_list(bullet, self.enemy2_list)

            # If collison = true then remove the bullet
            if len(hit_list) > 0 and self.enemy2_health == 0:
                explosion = Explosion(self.explosion_texture_list)
                explosion.center_x = hit_list[0].center_x
                explosion.center_y = hit_list[0].center_y
                self.explosions_list.append(explosion)

                bullet.remove_from_sprite_lists()

                # When a enemy is hit remove it from the game
                for enemy2 in hit_list:
                    enemy2.remove_from_sprite_lists()
                    self.score += 30
                    self.enemy2_health = 50
            elif len(hit_list) > 0:
                self.enemy2_health -= 10
                bullet.remove_from_sprite_lists()

        for bullet2 in self.bullet2_list:
            # Check for collison
            hit_list = arcade.check_for_collision_with_list(bullet2, self.player_list)

            # If collison = true then remove the bullet
            if len(hit_list) > 0 and self.player_health == 0:
                game_view = GameOverView()
                self.window.show_view(game_view)
            elif len(hit_list) > 0:
                self.player_health = self.player_health - 10
                bullet2.remove_from_sprite_lists()

            # Loop through each player for collison with coin
        for player in self.player_list:

            # Check the player to see if it hit a coin
            hit_list = arcade.check_for_collision_with_list(player, self.coin_list)

            # For every coin we hit, add to the score and remove the coin
            for coin in hit_list:
                coin.remove_from_sprite_lists()
                self.score += 5


class GameOverView(arcade.View):
    def __init__(self):
        super().__init__()
        self.time_taken = 0

    def on_show(self):
        self.background_list = arcade.SpriteList()
        self.background_sprite = arcade.Sprite("images\menu_template.png")
        self.background_sprite.center_x = IMAGE_WIDTH // 2
        self.background_sprite.center_y = SCREEN_HEIGHT // 2
        self.background_list.append(self.background_sprite)

    def on_draw(self):
        arcade.start_render()
        self.background_list.draw()
        arcade.draw_text("GAME OVER", 550, 260, arcade.color.YELLOW, font_size=20)
        arcade.draw_text("Click anyhwere to continue", 590, 230,
                         arcade.color.YELLOW, font_size=20, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        game_view = GameView()
        self.window.show_view(game_view)


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, "PROJECT 32")
    window.total_score = 0
    insturction_view = MenuView()
    window.show_view(insturction_view)
    arcade.run()


if __name__ == "__main__":
    main()