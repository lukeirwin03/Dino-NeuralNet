import pygame
import random
from var import *

class Rock():

    def __init__(self, window, x, y):
        self.window = window
        self.state = ROCK_MOVING
        self.img = pygame.image.load(ROCK_FILENAME)
        self.img = pygame.transform.scale(self.img, ROCK_SIZE)
        self.rect = self.img.get_rect()
        self.setPos(x, y)
        # print('ROCK_MOVING')

    def setPos(self, x, y):
        self.rect.left = x
        self.rect.top = y

    def move(self, dx, dy):
        self.rect.centerx += dx
        self.rect.centery += dy

    def draw(self):
        self.window.blit(self.img, self.rect)

    def checkStatus(self):
        if self.rect.right < 0:
            self.state = ROCK_DONE

    def update(self, dt):
        if self.state == ROCK_MOVING:
            self.move( -(SCROLL_SPEED * dt), 0 )
            self.draw()
            self.checkStatus()

class RockCollection():

    def __init__(self, window):
        self.window = window
        self.rocks = []

    def addNewRock(self, x):
        y = random.randint(ROCK_MAX, ROCK_MIN)
        rock = Rock(self.window, x, y)
        self.rocks.append(rock)

    def createNewRocks(self):
        self.rocks = []
        placed = ROCK_FIRST

        while placed < DISPLAY_W:
            self.addNewRock(placed)
            placed += ROCK_ADD_GAP

    def update(self, dt):
        rightmost = 0
        for rock in self.rocks:
            rock.update(dt)
            if rock.rect.left > rightmost:
                rightmost = rock.rect.left

        if rightmost < ( DISPLAY_W - ROCK_ADD_GAP * ( 1 + random.choice([.1, .5, .7, .9])) ):
            self.addNewRock(DISPLAY_W)
        
        self.rocks = [rock for rock in self.rocks if rock.state == ROCK_MOVING]


