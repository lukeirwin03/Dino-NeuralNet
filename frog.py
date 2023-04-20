import pygame
import random
from var import *
from nnet import Nnet
import numpy as np


class Frog():

    def __init__(self, window):
        self.window = window
        self.state = ALIVE
        self.img = pygame.image.load(FROG_FILENAME)
        self.img = pygame.transform.scale(self.img, FROG_SIZE)
        self.rect = self.img.get_rect()
        self.speed = 0
        self.fitness = 0
        self.nnet = Nnet(NNET_INPUTS, NNET_HIDDEN, NNET_OUTPUTS)
        self.timeLived = 0
        self.setPos(FROG_START_X, FROG_START_Y)

    def reset(self):
        self.state = ALIVE
        self.speed = 0 
        self.fitness = 0
        self.timeLived = 0
        self.setPos(FROG_START_X, FROG_START_Y)

    def setPos(self, x, y):
        self.rect.centerx = x
        self.rect.centery = y

    def move(self, dt):
        
        dist = 0
        newSpeed = 0

        dist = ( self.speed * dt ) + (  .5 * GRAVITY * dt * dt )
        newSpeed = self.speed + ( GRAVITY * dt )

        self.rect.centery += dist
        self.speed = newSpeed

        if self.rect.top < 0:
            self.rect.top = 0
            self.speed = 0

        if self.rect.bottom > DISPLAY_H:
            self.rect.bottom = DISPLAY_H
            self.speed = 0

    def jump(self, rocks):
        inputs = self.getInputs(rocks)
        val = self.nnet.getMaxValue(inputs)
        if(self.rect.bottom == DISPLAY_H) and (val > JUMP_CHANCE):
            self.speed = FROG_START_SPEED

    def draw(self):
        self.window.blit(self.img, self.rect)

    def checkStatus(self, rocks):
        self.checkCollision(rocks)
        
    def update(self, dt, rocks):
        if self.state == ALIVE:
            self.timeLived += dt
            self.move(dt)
            self.jump(rocks)
            self.draw()
            self.checkStatus(rocks)

    def assignCollisionFitness(self, rock):
        gapY = rock.rect.top
        self.fitness = -(abs(self.rect.centery - gapY))

    def checkCollision(self, rocks):
        for rock in rocks:
            if rock.rect.colliderect(self.rect):
                self.state = DEAD
                self.assignCollisionFitness(rock)
                break

    def getInputs(self, rocks):
        closest = DISPLAY_W * 2
        topY = 0
        for rock in rocks:
            if rock.rect.right < closest and rock.rect.right > self.rect.left:
                closest = rock.rect.right
                topY = rock.rect.top
        
        horizontalDist = closest - self.rect.centerx
        verticalDist = self.rect.centery + (topY)

        inputs = [
            ((horizontalDist / DISPLAY_W) * 0.99) + 0.01,
            (((verticalDist + Y_SHIFT) / NORMALIZER) * 0.99) + 0.01
        ]

        return inputs
    
    def createOffspring(p1, p2, window):
        newFrog = Frog(window)
        newFrog.nnet.createMixedWeights(p1.nnet, p2.nnet)
        return newFrog

class FrogCollection():

    def __init__(self, window):
        self.window = window
        self.frogs = []
        self.createNewGeneration()

    def createNewGeneration(self):
        self.frogs = []
        for i in range(0, GENERATION_SIZE):
            self.frogs.append(Frog(self.window))

    def update(self, dt, rocks):
        numAlive = 0

        for frog in self.frogs:
            frog.update(dt, rocks)
            if frog.state == ALIVE:
                numAlive += 1

        return numAlive

    def evolvePopulation(self):

        for frog in self.frogs:
            frog.fitness += frog.timeLived * SCROLL_SPEED

        self.frogs.sort(key=lambda x: x.fitness, reverse=True)

        cutOff = int(len(self.frogs) * MUTATION_CUT_OFF)
        chadFrogs = self.frogs[0:cutOff]
        badFrogs = self.frogs[cutOff:]
        numBadToTake = int(len(self.frogs) * MUTATION_BAD_TO_KEEP)

        for frog in badFrogs:
            frog.nnet.modifyWeights()

        newPopulation = []
        indexBadToTake = np.random.choice(np.arange(len(badFrogs)), numBadToTake, replace=False)

        for i in indexBadToTake:
            newPopulation.append(badFrogs[i])

        newPopulation.extend(chadFrogs)

        childrenNeeded = len(self.frogs) - len(newPopulation)

        while len(newPopulation) < len(self.frogs):
            indexToBreed = np.random.choice(np.arange(len(chadFrogs)), 2, replace=False)
            if indexToBreed[0] != indexToBreed[1]:
                newFrog = Frog.createOffspring(chadFrogs[indexToBreed[0]], chadFrogs[indexToBreed[1]], self.window)
                if random.random() < MUTATION_MODIFY_CHANCE_LIMIT:
                    newFrog.nnet.modifyWeights()
                newPopulation.append(newFrog)

        for frog in newPopulation:
            frog.reset();

        self.frogs = newPopulation
