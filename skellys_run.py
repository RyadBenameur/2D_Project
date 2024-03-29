""" Little Platformer Game Based on Adventure Time! """
""" Asset for finn credited to @LazyHamsters on Twitter! Check them out!"""

# All imports
import pygame
from pygame.locals import *

tilesize = 64

# Initalise Pygame
pygame.init()

# Declare display infomation
screen_width = 1920
screen_height = 1280
screen = pygame.display.set_mode([screen_width,screen_height])
s_img = pygame.image.load("img/m_assets/background.png")
s_img = pygame.transform.scale(s_img, (1920,1280))
pygame.display.set_caption("Skelly's Run!")

# Declare clock (Will lock framerate later)
clock = pygame.time.Clock()

# Player Class Declaration
class Player():
    def __init__(self,x,y):

        #Index for character sprites
        self.idle_index = 0
        self.run_index = 0

        # Counter for cooldowns
        self.counter = 0

        # Storing frames for animation
        self.idle_r_frames = []
        self.idle_l_frames = []
        self.run_r_frame_list = []
        self.run_l_frame_list = []

        # Idle Frames
        for num in range(1,10):
            img_r_idle = pygame.image.load(f"img/player/idle{num}.png")
            img_r_idle = pygame.transform.scale(img_r_idle, (56,80))
            img_l_idle = pygame.transform.flip(img_r_idle, True, False)
            self.idle_l_frames.append(img_l_idle)
            self.idle_r_frames.append(img_r_idle)
        
        #Running Frames
        for num in range(1,7):
            img_r_run = pygame.image.load(f"img/player/run{num}.png")
            img_r_run = pygame.transform.scale(img_r_run, (60,80))
            img_l_run = pygame.transform.flip(img_r_run, True, False)
            self.run_l_frame_list.append(img_l_run)
            self.run_r_frame_list.append(img_r_run)


        self.frame_idle_right = self.idle_r_frames[self.idle_index]
        self.frame_idle_left = self.idle_l_frames[self.idle_index]
        self.image_run_right = self.run_r_frame_list[self.run_index]
        self.image_run_left = self.run_l_frame_list[self.run_index]
        self.rect = self.frame_idle_right.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocity_y = 0
        self.jump = False
        self.looking = True # True is Right, False is Left


    def update(self):
        # This will be used to calculate changes in position - to calculate collisions.
        dx = 0
        dy = 0
        self.counter += 1

        # Takes input of keys by user.
        # X Axis Changes
        press = pygame.key.get_pressed()
        # X Axis Changes
        if press[pygame.K_a]:
            dx -= 8
            self.looking = False
        if press[pygame.K_d]:
            dx += 8
            self.looking = True

        # Y axis Changes
        if press[pygame.K_w] and self.jump == False:
            self.velocity_y -= 40
            self.jump = True

        # Process jump mechanics / gravity

        self.velocity_y += 1.5
        if self.velocity_y > 15:
            self.velocity_y = 15
        dy += self.velocity_y


        # Collisions
        # if pygame.Rect.colliderect(world.rect):
        #     pygame.quit()






        # Animations for Character

        # Idle Animations for looking right
        if dx == 0 and self.looking is True:
            if self.counter > 20:
                self.idle_index += 1
                if self.idle_index >= len(self.idle_r_frames):
                    self.idle_index = 0
                self.frame_idle_right = self.idle_r_frames[self.idle_index]
                self.counter = 0

        # Idle Animations for looking left
        elif dx == 0 and self.looking is False:
            if self.counter > 20:
                self.idle_index += 1
                if self.idle_index >= len(self.idle_l_frames):
                    self.idle_index = 0
                self.frame_idle_left = self.idle_l_frames[self.idle_index]
                self.counter = 0

        # Running animations
        elif dx > 0:
            self.idle_index = 0
            if self.counter > 6:
                self.run_index+= 1
                if self.run_index >= len(self.run_r_frame_list):
                    self.run_index = 0
                self.image_run_right = self.run_r_frame_list[self.run_index]
                self.counter = 0
        elif dx < 0:
            self.idle_index = 0
            if self.counter > 6:
                self.run_index+= 1
                if self.run_index >= len(self.run_l_frame_list):
                    self.run_index = 0
                self.image_run_left = self.run_l_frame_list[self.run_index]
                self.counter = 0           


        #Update coords of player on screen
        self.rect.x += dx
        self.rect.y += dy

        #Ensures they do not fall off the square
        if self.rect.bottom > screen_height:
            self.rect.bottom = screen_height
            dy = 0

        
        # Draws player on the screen
        if dx == 0:
            if self.looking is True:
                self.rect = self.frame_idle_right.get_rect(topleft = (self.rect.x,self.rect.y))
                screen.blit(self.frame_idle_right, self.rect)
            else:
                self.rect = self.frame_idle_left.get_rect(topleft = (self.rect.x,self.rect.y))
                screen.blit(self.frame_idle_left, self.rect)

        elif dx > 0:
            self.rect = self.image_run_right.get_rect(topleft = (self.rect.x,self.rect.y))
            screen.blit(self.image_run_right,self.rect)
        elif dx < 0:
            self.rect = self.image_run_left.get_rect(topleft = (self.rect.x,self.rect.y))
            screen.blit(self.image_run_left,self.rect)
        
        pygame.draw.rect(screen, (255,255,255), self.rect, 2)

class World():
    def __init__(self,array):
        self.world_tiles = []
        # Generates a list of tuples to contain details regarding world tile images, as well as 
        y_level = 0
        for row in array:
            x_level = 0
            for tile in row:
                if tile != 0:
                    asset = pygame.image.load(f"img/t_assets/tile_{tile}.png")
                    image = pygame.transform.scale(asset, (tilesize, tilesize))
                    self.rect = image.get_rect()
                    self.rect.x = x_level * tilesize
                    self.rect.y = y_level * tilesize
                    tile_data = (image, self.rect)
                    self.world_tiles.append(tile_data)
                x_level += 1
            y_level += 1

    def update(self):
        for tile in self.world_tiles:
            screen.blit(tile[0], tile[1])


# Game Variables
player = Player(0,0)
world = World(
[[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,4,5,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,4,5,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,3,4,5,0,0,0,0,0,0,0,0,0,3,4,5,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],
[2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],
[2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2]]
)



def linedraw():
    """ Function to draw grid on screen. Optional"""
    tilesize = 64
    for x in range(0,30):
        pygame.draw.line(screen,(0,0,0),(x*tilesize,0),(x*tilesize,screen_height))
    for y in range(0,20):
        pygame.draw.line(screen,(0,0,0),(0,y*tilesize),(screen_width,y*tilesize))
        

# Game Loop
running = True
while running:

    # Exit button function
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    #
    # Logic
    #
    

    # Screen Updates 
    screen.fill([255,255,255])
    screen.blit(s_img, (0,0))

    # World Animations
    linedraw()
    world.update()

    # Animations / Characters    
    player.update()

    
    pygame.display.update()
    # Locked Framerate
    clock.tick(60)
pygame.quit()
