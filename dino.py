import pygame
from var import *
from rock import RockCollection
from frog import FrogCollection

def updateLabel(data, title, font, x, y, window):
    label = font.render('{} {}'.format(title, data), 1, DATA_FONT_COLOR)
    window.blit(label, (x, y))
    return y

def updateDataLabels(window, dt, gameTime, iterations, numAlive, font):
    y_pos = 10
    gap = 20
    x_pos = 10
    y_pos = updateLabel( round(1000/dt, 2), 'FPS', font, x_pos, y_pos + gap, window )
    y_pos = updateLabel( round(gameTime/1000, 2), 'Game Time', font, x_pos, y_pos + gap, window )
    y_pos = updateLabel( iterations, 'Iteration', font, x_pos, y_pos + gap, window )
    y_pos = updateLabel( numAlive, 'Alive', font, x_pos, y_pos + gap, window )

    y_pos = updateLabel( round((gameTime*.2)), 'Score', font, x_pos, y_pos + gap, window )
    


def runGame():
    pygame.init()
    window = pygame.display.set_mode( ( DISPLAY_W, DISPLAY_H ) )
    pygame.display.set_caption('Dino')

    running = True
    bg = pygame.image.load(BG_FILENAME)
    font = pygame.font.SysFont("monospace", DATA_FONT_SIZE)

    clock = pygame.time.Clock()
    dt = 0
    gameTime = 0
    iterations = 0

    rocks = RockCollection(window)
    rocks.createNewRocks()

    frogs = FrogCollection(window)


    while running:

        dt = clock.tick(FPS)
        gameTime += dt

        window.blit( bg, (0,0) )
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                running == False
        
        rocks.update(dt + gameTime * 0.0005)
        numAlive = frogs.update(dt + gameTime * 0.0005, rocks.rocks)

        if numAlive == 0:
            rocks.createNewRocks()
            gameTime = 0
            frogs.evolvePopulation()
            iterations += 1

        updateDataLabels(window, dt, gameTime, iterations, numAlive, font)
        pygame.display.update()




if __name__ == '__main__':
    runGame()