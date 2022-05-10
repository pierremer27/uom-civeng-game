import json
import sys
from game.start import start

if __name__ == '__main__':

    # Load the configuration file
    config_path = 'levels/paris.json'
    if len(sys.argv) > 1:
        config_path = sys.argv[1]
    with open(config_path, 'r') as stream:
        config = json.load(stream)

    # Start the game with the config
    start(config)
