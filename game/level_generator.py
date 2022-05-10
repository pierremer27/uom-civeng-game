import sys
import json
import random
import datetime

from game.constants import BOARD_WIDTH, BOARD_HEIGHT, COLORS

BOARD_EDGES_OFFSET = 20
random.seed(datetime.datetime.now().timestamp())


def get_random_value(max):
    return random.randint(BOARD_EDGES_OFFSET, max - BOARD_EDGES_OFFSET)


def get_random_color():
    return random.choice(list(COLORS.items()))[0]


print('Level name: ', end='')
level_name = input()
locations = []
filename = sys.argv[1]
i = 0

while True:
    i += 1
    print('Location ', i, ': ', sep='', end='')
    line = input()
    if line == 'stop' or line == '':
        break
    locations.append({
        'name': line,
        'x': get_random_value(BOARD_WIDTH),
        'y': get_random_value(BOARD_HEIGHT),
        'color': get_random_color(),
    })

json_string = json.dumps({
    "name": level_name,
    "bridges": [],
    "locations": locations,
}, indent=4)
text_file = open(filename, "w")
n = text_file.write(json_string)
text_file.close()
