import time
import random
import pygame
from pygame import mixer
import turtle
import os
from colours import *

# TODO: MOST IMPORTANT: QOL changes, fix bugs, Figure out why button needs 2 pushes to swap positions
# ----- CONSTANTS
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
SKY_BLUE = (95, 165, 228)
WIDTH = 1200
HEIGHT = 800
TITLE = "Platform Dodge Game"

# SCREEN STUFF LMAO
size = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(size)
pygame.display.set_caption(TITLE)
mixer.init()

# -------- TEXT
def write_text(text, x, y, font_size):
    font = pygame.font.Font(pygame.font.get_default_font(), font_size)
    text_surface = font.render(text, False, BLACK)
    screen.blit(text_surface, (x, y))



class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([80, 110])
        self.image.fill((0, 0, 0))
        self.rect = self.image.get_rect()
        self.image = pygame.image.load("Assets//Player_idle.png")
        self.hp = 4
        self.boost = 1
        self.change_y = 0
        self.change_x = 0
        self.rect.x, self.rect.y = (WIDTH / 2, HEIGHT / 3)

    def update(self):
        # Keeping player in the screen
        # Top and bottom
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        # Left and right
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        # Keep player on the platform
        self.calc_grav()

        self.rect.y += self.change_y #remember to actually use self.change_y instead of just setting it

    def calc_grav(self):
        """ Calculate effect of gravity. """
        if self.change_y == 0:
            #If not moving, set the base change value to this:
            self.change_y = 0.5
        else:
            #If you are moving in the y axis, accelerate by this much
            self.change_y += 0.34

        # See if we are on the ground.
        if self.rect.y >= HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = HEIGHT - self.rect.height

class Floor(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([WIDTH, 75])
        self.image.fill((0, 0, 0))
        self.rect = self.image.get_rect()
        self.image = pygame.image.load("Hellfire_Animation//Floorfire.png")
        self.change_y = 0
        self.change_x = 0
        self.rect.x, self.rect.y = (WIDTH/ 2, HEIGHT)

    def update(self):#, player):
        # Keeping floor in the screen
        # Top and bottom
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        # Left and right
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

class Platform(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([200, 70])
        self.image.fill((0, 0, 0))
        self.rect = self.image.get_rect()
        self.image = pygame.image.load("Assets/Platform_sando.jpg")
        self.change_y = 0
        self.change_x = 0
        self.rect.x, self.rect.y = (WIDTH - 300, HEIGHT - 500)
        #self.blit(self.image, (0, 0))

    def update(self):
        #print ("Platform update")
        # Keeping floor in the screen
        # Top and bottom
        #if self.rect.top < 0:
        #     self.kill()
        if self.rect.bottom > HEIGHT:
             self.kill()
        # # Left and right
        # if self.rect.left < 0:
        #     self.rect.left = 0
        # if self.rect.right > WIDTH:
        #     self.rect.right = WIDTH

class Mcguffin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([75, 75])
        self.image.fill((0, 0, 0))
        self.rect = self.image.get_rect()
        self.image = pygame.image.load("Assets/Mcguffin.jpg")
        self.change_y = 0
        self.change_x = 0
        self.life_timer = 0
        self.rect.x, self.rect.y = (WIDTH - random.randrange (1, 1200), HEIGHT - random.randrange (1, 1000))

    def update(self):  # , player):
        # Keeping floor in the screen
        # Top and bottom
        self.life_timer += 1
        if self.rect.top < 0:
            pass
        if self.rect.bottom > HEIGHT:
            self.kill()
        # Left and right
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.life_timer >= 500:
            self.kill()
            self.life_timer = 0

class Projectile (pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([75, 75])
        self.image.fill((0, 0, 0))
        self.rect = self.image.get_rect()
        self.image = pygame.image.load("Assets/Projectile1.png")
        self.change_y = 0
        self.change_x = 0
        self.life_timer = 0
        self.rect.x, self.rect.y = (WIDTH - 1000, HEIGHT - 1200)

    def update(self):
        #print ("Platform update")
        # Keeping floor in the screen
        # Top and bottom
        #if self.rect.top < 0:
        #     self.kill()
        if self.rect.bottom > HEIGHT:
             self.kill()


class Hot_Explosion (pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([HEIGHT, 50])
        self.image.fill((0, 0, 0))
        self.image = pygame.image.load("Assets/Hot_explode.png")
        self.rect = self.image.get_rect()
        self.change_y = 0
        self.change_x = 0
        self.life_timer = 0
        self.rect.x, self.rect.y = (WIDTH - 1000, HEIGHT - 1200)

    def update(self):
        self.life_timer += 1
        #print ("Platform update")
        # Keeping floor in the screen
        # Top and bottom
        #if self.rect.top < 0:
        #     self.kill()
        if self.life_timer == 5:
             self.kill()

class Hot_Sauce_Bomb (pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([100, 100])
        self.image.fill((0, 0, 0))
        self.rect = self.image.get_rect()
        self.image = pygame.image.load("Assets/Hot_Bomb.png")
        self.change_y = 0
        self.change_x = 0
        self.life_timer = 0
        self.rect.x, self.rect.y = (WIDTH - 1000, HEIGHT - 1200)

    def update(self):
        #print ("Platform update")
        # Keeping floor in the screen
        # Top and bottom
        #if self.rect.top < 0:
        #     self.kill()
        pass


def draw_health_bar(player, x, y, ):
    health_bar_width = 40
    health_bar_length = 300
    health_bar_border = pygame.Rect(x, y, health_bar_length, health_bar_width)
    pygame.draw.rect(screen, BLACK, health_bar_border)
    health_bar_inside = pygame.Rect(x + 5, y + 5, health_bar_length - 10, health_bar_width - 10)
    pygame.draw.rect(screen, WHITE, health_bar_inside)
    proportion = player.hp / 4
    the_length_of_the_health_bar_coloured_in = (health_bar_length - 10) * proportion
    health_bar_the_actual_health_bar = pygame.Rect(x + 5, y + 5, the_length_of_the_health_bar_coloured_in,
                                                   health_bar_width - 10)
    pygame.draw.rect(screen, RED, health_bar_the_actual_health_bar)

def draw_boost_bar(player, x, y, ):
    boost_bar_width = 30
    boost_bar_length = 220
    boost_bar_border = pygame.Rect(x, y, boost_bar_length, boost_bar_width)
    pygame.draw.rect(screen, BLACK, boost_bar_border)
    boost_bar_inside = pygame.Rect(x + 5, y + 5, boost_bar_length - 10, boost_bar_width - 10)
    pygame.draw.rect(screen, WHITE, boost_bar_inside)
    proportion = player.boost / 1
    the_length_of_the_boost_bar_coloured_in = (boost_bar_length - 10) * proportion
    boost_bar_the_actual_boost_bar = pygame.Rect(x + 5, y + 5, the_length_of_the_boost_bar_coloured_in,
                                                   boost_bar_width - 10)
    pygame.draw.rect(screen, CYAN, boost_bar_the_actual_boost_bar)

class Button (pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([100, 100])
        self.image.fill((0, 0, 0))
        self.rect = self.image.get_rect()
        self.image = pygame.image.load("Assets/Retry_button.jpg")
        self.rect.x, self.rect.y = (WIDTH - 1000, HEIGHT - 250)

class Quit_Button (pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([100, 100])
        self.image.fill((0, 0, 0))
        self.rect = self.image.get_rect()
        self.image = pygame.image.load("Assets/Quitbutton.jpg")
        self.rect.x, self.rect.y = (WIDTH - 500, HEIGHT - 250)

class GameOver_Select_Arrow (pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([100, 100])
        self.image.fill((0, 0, 0))
        self.rect = self.image.get_rect()
        self.image = pygame.image.load("Assets/Button_select_arrow.png")
        self.change_x = 0
        #self.rect.y = HEIGHT - 350
        #self.rect.x = WIDTH - 1000
    def update(self):
        pass
def main():
    pygame.init()

    # ----- SCREEN PROPERTIES
    size = (WIDTH, HEIGHT)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption(TITLE)
    bg = pygame.image.load("Assets//Background.jpg")
    gobg = pygame.image.load("Assets//Game_Over_Screen.jpg")


    # TODO: Hookup all references to the below, to the game instead
    #  Sprite groups

    all_sprites_group = pygame.sprite.Group()
    platform_sprites_group = pygame.sprite.Group()
    floor_sprites_group = pygame.sprite.Group()
    powerup_sprites_group = pygame.sprite.Group()
    projectile_sprites_group = pygame.sprite.Group()
    hot_bomb_sprites_group = pygame.sprite.Group()
    hot_explosion_sprites_group = pygame.sprite.Group()
    button_sprites_group = pygame.sprite.Group()
    quit_button_sprites_group = pygame.sprite.Group()
    GMOVER_arrow_sprites_group = pygame.sprite.Group()

    player = Player()
    floor = Floor()
    mcguffin = Mcguffin()
    projectile = Projectile()
    hot_bomb = Hot_Sauce_Bomb()
    #game_over_buttons = Buttons()
    hot_explosion = Hot_Explosion()
    all_sprites_group.add(player)
    #all_sprites_group.add(mcguffin)
    all_sprites_group.add(floor)
    #all_sprites_group.add(projectile)
    #all_sprites_group.add(hot_bomb)
    #all_sprites_group.add(hot_explosion)
    #all_sprites_group.add(game_over_buttons)
    floor_sprites_group.add(floor)
    platformright = Platform()
    platformleft = Platform()
    platformleft.rect.x, platformleft.rect.y = (WIDTH - 1200, HEIGHT - 500)
    all_sprites_group.add(platformright)
    all_sprites_group.add(platformleft)
    platform_sprites_group.add(platformright)
    platform_sprites_group.add(platformleft)
    #projectile_sprites_group.add(projectile)
    #hot_bomb_sprites_group.add(hot_bomb)
    #hot_explosion_sprites_group.add(hot_explosion)
    #button_sprites_group.add(game_over_buttons)

    # Buttons for game over screen
    button_sprites_group.add(Button())
    quit_button_sprites_group.add(Quit_Button())
    GMOVER_arrow_sprites_group.add(GameOver_Select_Arrow())




    # ----- LOCAL VARIABLES
    Main_menu = False
    Guy_dodge_game_done = False
    Guy_dodge_game_running = True
    direction = 0
    crouch = False
    jump = 0
    score = 0
    mcguffin_timer = 0
    invuln = 10
    time_since_last_jump = 0
    clock = pygame.time.Clock()

    last_time_spawned = pygame.time.get_ticks()
    last_time_spawned_mcguffin = pygame.time.get_ticks()
    last_time_spawned_projectile = pygame.time.get_ticks()
    last_time_spawned_hot_bomb = pygame.time.get_ticks()
    PLATFORM_COOLDOWN = random.randrange(2500, 4000)
    Mcguffin_cooldown = random.randrange(5000, 10000)
    Projectile_cooldown = random.randrange (2000, 5000)
    Hot_bomb_cooldown = random.randrange (3000, 6000)

    floor_fire = pygame.image.load('./Hellfire_Animation/Floorfire.png')
    floor_fire_rev = pygame.image.load('./Hellfire_Animation/Floorfire-reverse.png')

    # ----- MAIN LOOP
    while not Guy_dodge_game_done:
        # -- Event Handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Guy_dodge_game_done = True

        # Spawn Platforms
        score += 1
        #game.Platform_creator()
        if pygame.time.get_ticks() - last_time_spawned >= PLATFORM_COOLDOWN:
            platformright = Platform()
            platformleft = Platform()
            platformleft.rect.x, platformleft.rect.y = (WIDTH - random.randrange(300, 400), HEIGHT - random.randrange(1000, 1300))
            platformright.rect.x, platformright.rect.y = (WIDTH - random.randrange(1000, 1200), HEIGHT - random.randrange(1000, 1300))
            all_sprites_group.add(platformright)
            all_sprites_group.add(platformleft)
            platform_sprites_group.add(platformright)
            platform_sprites_group.add(platformleft)
            # PLATFORM_COOLDOWN += random.randrange(2500, 10000)
            last_time_spawned = pygame.time.get_ticks()
            # Create Platforms
        if player.hp > 4:
            player.hp = 4
        if player.boost > 1:
            player.boost = 1

        if pygame.time.get_ticks() - last_time_spawned_mcguffin >= Mcguffin_cooldown:
            mcguffin = Mcguffin()
            mcguffin.rect.x, mcguffin.rect.y = (WIDTH - random.randrange (1, 1200), HEIGHT - 1200)
            powerup_sprites_group.add(mcguffin)
            all_sprites_group.add(mcguffin)
            last_time_spawned_mcguffin = pygame.time.get_ticks()

        if pygame.time.get_ticks() - last_time_spawned_projectile >= Projectile_cooldown:
            projectile = Projectile()
            projectile_sprites_group.add(projectile)
            all_sprites_group.add(projectile)
            projectile.rect.x, projectile.rect.y = (WIDTH - random.randrange (100, 1200), HEIGHT - 1200)
            last_time_spawned_projectile = pygame.time.get_ticks()
            print ("spawn projectile")

        if pygame.time.get_ticks() - last_time_spawned_hot_bomb >= Hot_bomb_cooldown:
            hot_bomb = Hot_Sauce_Bomb()
            all_sprites_group.add(hot_bomb)
            hot_bomb_sprites_group.add(hot_bomb)
            hot_bomb.rect.x, hot_bomb.rect.y = (WIDTH - random.randrange (100, 1200), HEIGHT - 1200)
            last_time_spawned_hot_bomb = pygame.time.get_ticks()
            print ("spawn Hot Sauce")





        pressed = pygame.key.get_pressed()
        # ----- LOGIC
        #Touching the bottom of the screen code
        #if player.rect.y >= HEIGHT - player.rect.height and player.change_y >= 0:
            #player.change_y = 0
            #player.rect.y = HEIGHT - player.rect.height

        #Touching a platform, or in this case the "Floor"
        touching_floor = pygame.sprite.spritecollide(player, floor_sprites_group, False)
        for the_floor in touching_floor:
            if not invuln > 0:
                player.hp -= 1
                print ("DAMAGE! FLOOR!")
                invuln += 200
            if floor.rect.top > player.rect.y:
                player.change_y = 0
            if player.rect.bottom >= floor.rect.top:
                player.rect.bottom = floor.rect.top
                player.change_y = -20
            jump = 0
        touching_platforms = pygame.sprite.spritecollide(player, platform_sprites_group, False)

        for platform in touching_platforms:
            # The player is on top of the platform
            if player.rect.right <= platform.rect.left:
                player.rect.right = platform.rect.left
            elif player.rect.bottom >= platform.rect.top:
                player.rect.bottom = platform.rect.top
                player.change_y = 0
                jump = 0
            # The player is below the platform
            elif player.rect.top <= platform.rect.bottom:
                #player.rect.y = platform.rect.bottom
                player.change_y = 0
            # The player is to the left of the platform
            jump = 0

        powerup_contact = pygame.sprite.spritecollide(player, powerup_sprites_group, True)

        for powerups in powerup_contact:
            powers = ["blank", "health", "boost",]
            powerup_select = random.choice(powers)
            if powerup_select == "blank":
                print ("Activated blank effect!")
                for projectile in projectile_sprites_group:
                    projectile.kill()
            if powerup_select == "health":
                print ("HP UP")
                player.hp += 1
            if powerup_select == "boost":
                print ("Boost acquired")
                player.boost += 1
            score += 100

        projectile_contact = pygame.sprite.spritecollide(player, projectile_sprites_group, True)

        hot_explosion_contact = pygame.sprite.spritecollide(player, hot_explosion_sprites_group, False)

        if not invuln > 0:
            for projectiles in projectile_contact:
                print("DAMAGE! PROJECTILE!")
                player.hp -= 1
                invuln += 200

            for explosions in hot_explosion_contact:
                print ("DAMAGE! EXPLOSION!")
                player.hp -= 1
                invuln += 200

        #if boost > 1:
            #boost == 1

        for platform in platform_sprites_group:
            platform.change_y = 3
            platform.rect.y += platformright.change_y

        for projectile in projectile_sprites_group:
            projectile.change_y = 5
            projectile.rect.y += projectile.change_y

        for hot_bomb in hot_bomb_sprites_group:
            hot_bomb.change_y = 5
            hot_bomb.rect.y += hot_bomb.change_y

        for mcguffin in powerup_sprites_group:
            mcguffin.change_y = 6
            mcguffin.rect.y += mcguffin.change_y





        # The player is to the right of the platform

        # if platforms.rect.top > player.rect.y:
        #     print("in")
        #     player.change_y = -0
        # if platforms.rect.bottom > player.rect.y:
        #     print ("w")
        #     player.change_y = 1
        # if platforms.rect.left < player.rect.x:
        #     print ("x")
        #     player.change_x = 0
        if pressed[pygame.K_w] or pressed[pygame.K_UP]:
            direction = 1
            player.rect.width, player.rect.height = (80, 110)
            if time_since_last_jump >= 0.5*60:
                if jump < 2:
                    player.change_y = -10
                    #player.rect.y -= player.change_y  # moves the player upward
                    jump += 1
                    time_since_last_jump = 0
                    # print('jump')
        if pressed[pygame.K_s] or pressed[pygame.K_DOWN]:
            direction = 2
            crouch = True
            player.image = pygame.image.load("Assets//Player_crouch.png")
            # player.rect.width, player.rect.height = player.image.get_rect()[2], player.image.get_rect()[3]
            player.rect.width, player.rect.height = (80, 96)
            # player.rect.width = 80
            # Repeat code to undo
            #  0        1       2      3
            # [x-coord, ycoord, width, height]
            if not touching_floor or touching_platforms:
                player.change_y = 10
                player.rect.y += player.change_y
            if touching_floor or touching_platforms:
                player.change_y = 0
                player.rect.y += player.change_y
            else: crouch = False
        if pressed[pygame.K_a] or pressed[pygame.K_LEFT]:
            player.image = pygame.image.load("Assets//Player_left.png")
            player.rect.width, player.rect.height = (80, 110)
            player.change_x = 5
            player.rect.x -= player.change_x
            direction = 3
        if pressed[pygame.K_d] or pressed[pygame.K_RIGHT]:
            player.image = pygame.image.load("Assets//Player_idle.png")
            player.rect.width, player.rect.height = (80, 110)
            player.change_x = 5
            player.rect.x += player.change_x
            direction = 4
        if pressed[pygame.K_LSHIFT] and pressed[pygame.K_d] or pressed[pygame.K_LSHIFT] and pressed[pygame.K_RIGHT]:
            player.change_x = 10
            player.rect.x += player.change_x
        if pressed[pygame.K_LSHIFT] and pressed[pygame.K_a] or pressed[pygame.K_LSHIFT] and pressed[pygame.K_LEFT]:
            player.change_x = 10
            player.rect.x -= player.change_x
        if pressed[pygame.K_SPACE] and player.boost >= 1:
            if direction == 1:
                player.change_y -= 20
                player.boost -= 1
                print("boost up")
            if direction == 2:
                player.change_y -= 20
                player.boost -= 1
                print("boost up")
            if direction == 3:
                player.change_y -= 20
                player.boost -= 1
                print("boost up")
            if direction == 4:
                player.change_y -= 20
                player.boost -= 1
                print("boost up")
        if pressed[pygame.K_ESCAPE]:
            hp = 0
            Guy_dodge_game_done = True
            Guy_dodge_game_running = False


        all_sprites_group.update()
        platform_sprites_group.update()

        if player.hp <= 0:
            print("YOU GOT FLAVOURED")
            Guy_dodge_game_done = True
            Guy_dodge_game_running = False

        for hot_sauces in hot_bomb_sprites_group:
            if hot_bomb.rect.bottom > HEIGHT:
                hot_explosion = Hot_Explosion()
                all_sprites_group.add(hot_explosion)
                hot_explosion_sprites_group.add(hot_explosion)
                hot_explosion.rect.x, hot_explosion.rect.y = (hot_bomb.rect.x, HEIGHT - 1200)
                print("Boom!")
                hot_bomb.kill()

        # ----- RENDER
        screen.fill(WHITE)
        screen.blit(bg, (0,0))
        #screen.blit(platform.image, (0,0))
        all_sprites_group.draw(screen)
        draw_boost_bar(player, 50, 60)
        draw_health_bar(player, 50, 25)
        if int(pygame.time.get_ticks()) % 2 == 0:
            screen.blit(floor_fire, (0, HEIGHT - floor_fire.get_height()))
        else:
            screen.blit(floor_fire_rev, (0, HEIGHT - floor_fire_rev.get_height()))

        mixer.music.load("./Songs/BGM/Game_over_music.mp3")
        mixer.music.play()
        post_game_option_select = 0
        while Guy_dodge_game_done and not Guy_dodge_game_running: #a long way of writing: while the game over screen runs, check for these commands
            screen.fill(BLACK)
            screen.blit(gobg, (0, 0))
            # Make one button
            button_sprites_group.draw(screen)
            quit_button_sprites_group.draw(screen)
            GMOVER_arrow_sprites_group.draw(screen)
            game_over_arrow = GameOver_Select_Arrow()
            # mixer.music.load("./Songs/BGM/Game_over_music.mp3")
            # mixer.music.play()
            pressed = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    Guy_dodge_game_done = True
                if pressed[pygame.K_LEFT]:
                    post_game_option_select = 1
                if pressed[pygame.K_RIGHT]:
                    post_game_option_select = 2
                if pressed[pygame.K_RETURN] and post_game_option_select == 1:
                    Guy_dodge_game_done = False
                    #Rerun the game unrecursively (closes main and reopens main)
                    return True
                if pressed[pygame.K_RETURN] and post_game_option_select == 2:
                    # Returns False, which ends the game over loop, starting the main menu loop
                    return False
                #I am not quite sure why THIS works of all things, but it does.
                for game_over_arrow in GMOVER_arrow_sprites_group:
                    if post_game_option_select == 1:
                        game_over_arrow.rect.x = WIDTH - 1200
                    if post_game_option_select == 2:
                        game_over_arrow.rect.x = WIDTH - 600
                pygame.display.flip()
                print (post_game_option_select)

                #Fills the screen with black, blits the gameover screen, checks for either enter or backspace


        #all_sprites_group.draw(platform)



        # ----- UPDATE DISPLAY
        pygame.display.flip()
        clock.tick(60)
        time_since_last_jump += 1
        invuln -= 1



def main_menu():
    mixer.music.stop()
    mixer.music.load("./Songs/BGM/Start_screen_muzak.mp3")
    mixer.music.play()
    screen.fill(BLACK)
    mm0 = pygame.image.load("./menu/all_off.png")
    mm1 = pygame.image.load("./menu/all_play_on.png")
    mm2 = pygame.image.load("./menu/all_options_on.png")
    mm3 = pygame.image.load("./menu/all_quit_on.png")
    screen.blit(mm0, (0,0))
    mainmenu_select = 0
    pygame.display.flip()


    while True: #while the main menu runs, these commands are active
        pressed = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if mainmenu_select > 3 or mainmenu_select <= -1:
                mainmenu_select = 0
            if pressed[pygame.K_DOWN]:
                mainmenu_select += 1
            if pressed[pygame.K_UP]:
                mainmenu_select -= 1
            if mainmenu_select == 0:
                screen.blit(mm0, (0, 0))
            elif mainmenu_select == 1:
                screen.blit(mm1, (0, 0))
            elif mainmenu_select == 2:
                screen.blit(mm2, (0, 0))
            elif mainmenu_select == 3:
                screen.blit(mm3, (0, 0))
            if pressed[pygame.K_RETURN] and mainmenu_select == 1:
                return True
            if pressed[pygame.K_RETURN] and mainmenu_select == 3:
                return False
            if pressed[pygame.K_ESCAPE]:
                return False

            pygame.display.flip()

while True: #Runs for the whole program. Universal truth. While the game runs, when you aren't in the main menu it runs the rerun loop, which will proceed to loop until you break out of it, but since it is the end of your while loop and the outermost loop is always true, it loops into the menu
    if not main_menu():
        break
    # print ("main menu was here")
    while True: #repeat infinitely until.... blank (check the break statement)
        rerun = main()
        if rerun:
            continue
        else:
            break


# the cutout of the cow. DO NOT REMOVE. IT BREAKS THE SHIT OUT OF THE GAME AND IDFK WHY.
