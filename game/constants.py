import pygame

WINDOW_WIDTH = 1080
WINDOW_HEIGHT = 620

UOM_LOGO_PATH = 'game/assets/uom_logo.png'
UOM_MAIN_COLOR = (80, 0, 127)

TICKS_STARTUP = 100
TICKS_CONNECTIONS = 300
SHOW_CONNECTION_DELAY = 25

#### KPI CONSTANTS #################################
# The cost of a connection
CONNECTION_COST = 0.1
# The cost of a pixel worth of railway
RAILWAY_UNIT_COST = 0.01

# Travelling one pixel takes x minutes.
RAILWAY_UNIT_TRAVEL_TIME = 0.02
# Stopping at a location takes x minutes.
CHANGE_TRAIN_TIME = 2
####################################################

HEADER_HEIGHT = 80
HEADER_WIDTH = WINDOW_HEIGHT
HEADER_LINE_WIDTH = 2

# 1000 x 620
BOARD_HEIGHT = WINDOW_HEIGHT - HEADER_HEIGHT
BOARD_WIDTH = WINDOW_WIDTH

ORANGE = pygame.Color(255, 144, 51)
BLACK = pygame.Color(0, 0, 0)
BLUE = pygame.Color(51, 131, 255)
DEEP_BLUE = pygame.Color(51, 66, 255)
PURPLE = pygame.Color(162, 51, 255)
VIOLET = pygame.Color(119, 51, 255)
PINK = pygame.Color(215, 51, 255)
PINKEYE = pygame.Color(255, 51, 141)
RED = pygame.Color(255, 51, 94)
GREEN = pygame.Color(46, 176, 14)
GREY = pygame.Color(100, 100, 100)
LIGHT_GREY = pygame.Color(150, 150, 150)
EXTREME_LIGHT_GREY = pygame.Color(230, 230, 230)

COLORS = {
    'orange': ORANGE,
    'black': BLACK,
    'blue': BLUE,
    'deep_blue': DEEP_BLUE,
    'purple': PURPLE,
    'violet': VIOLET,
    'pink': PINK,
    'pinkeye': PINKEYE,
    'red': RED,
    'green': GREEN,
    'grey': GREY,
}
