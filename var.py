DISPLAY_W = 1120
DISPLAY_H = 630
FPS = 30

DATA_FONT_SIZE = 18
DATA_FONT_COLOR = (40,40,40)
BG_FILENAME = 'bg.png'

ROCK_FILENAME = 'rock2.png'
ROCK_SIZE = (150, 150)
SCROLL_SPEED = 400/1000
ROCK_DONE = 1
ROCK_MOVING = 0

ROCK_MAX = 500
ROCK_MIN = 550
ROCK_START_X = DISPLAY_W
ROCK_FIRST = 600
ROCK_ADD_GAP = 600

FROG_FILENAME = 'frog.png'
FROG_SIZE = (100,100)
FROG_START_SPEED = -0.7
FROG_START_X = 150
FROG_START_Y = DISPLAY_H - 200
ALIVE = 1
DEAD = 0
GRAVITY = 0.001

GENERATION_SIZE = 30

NNET_INPUTS = 2
NNET_HIDDEN = 5
NNET_OUTPUTS = 1

JUMP_CHANCE = 0.6 # 0.5 

MAX_Y_DIFF = ROCK_MAX
MIN_Y_DIFF = ROCK_MIN
Y_SHIFT = abs(MIN_Y_DIFF)
NORMALIZER = abs(MIN_Y_DIFF) + MAX_Y_DIFF

MUTATION_WEIGHT_MODIFY_CHANCE = 0.2
MUTATION_ARRAY_MIX_PERC = 0.5

MUTATION_CUT_OFF = 0.4
MUTATION_BAD_TO_KEEP = 0.2
MUTATION_MODIFY_CHANCE_LIMIT = 0.4