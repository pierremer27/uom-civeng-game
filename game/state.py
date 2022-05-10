import pygame
from game.assets import Assets
from game.constants import *
from game.utils import Location, LocationGraph, Connection
from router import connect_locations
import math
import statistics


class State():
    def __init__(self, config: dict):
        # Game configuration
        self.config = config
        # Temporary list of connections (used to animate connections)
        self.connections_buffer = []
        # Is the game running
        self.active = True
        # The game assets
        self.assets = Assets(config["background_path"])
        # The cost of the network
        self.cost = 0
        # The congestion rating
        self.traffic_congestion = 0
        # The total number of itineraries that have been tested.
        self.num_travels = 0
        # The total travel time of all the itineraries that have been tested.
        self.total_travel_time_mins = 0
        # The timer used to animate stuff
        self.timer = 0
        # The game step (0, 1 or 2)
        self.step = 0
        # Used to display errors
        self.network_error = ''
        # The function to call at each step of the game. (cf self.step)
        self.steps = [
            self.wait_step,
            self.load_connections_step,
            self.test_network_step,
        ]
        # The list of connections being highlighted in green.
        self.test_network_highlight = []
        # The itineraries the system has already evaluated.
        self.itineraries_to_test = []

        # The font used to display regular text.
        self.font = None
        # The font used to display big text.
        self.big_font = None
        # The pygame window
        self.window = None

        self.init_window()
        self.load_config()
        self.init_itineraries()

        # The graph representing our railway network
        self.graph = LocationGraph(self.locations)

        self.connect_locations()

    def init_window(self):
        """
        This function is reponsible for creating a pygame window and setting up the fonts to render text later.
        """
        pygame.init()
        pygame.display.set_caption('Railway Planner - ' + self.config['name'])
        self.font = pygame.font.Font(pygame.font.get_default_font(), 14)
        self.big_font = pygame.font.Font(pygame.font.get_default_font(), 18)
        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.window.fill(pygame.color.Color(255, 255, 255))

    def init_itineraries(self):
        """
        Initializes a list of all the intineraries we're going to test (aka all of them)
        """
        for loc1 in self.locations:
            for loc2 in self.locations:
                if loc1 != loc2 and Connection(loc1, loc2) not in self.itineraries_to_test:
                    self.itineraries_to_test.append(Connection(loc1, loc2))

    def load_config(self):
        """
        Load the locations from the config file into an array to manipulate them easier.
        """
        self.locations = []
        for loc in self.config['locations']:
            self.locations.append(
                Location(loc['x'], loc['y'] + HEADER_HEIGHT, loc['name'], loc['color']))

    def connect_locations(self):
        """
        Invoke the student's algorithm. Store all the connections it created in a buffer.
        """
        connect_locations(self.locations, self.connect_handler)

    def connect_handler(self, a, b):
        """
        This function is called by the student's algorithm.
        """
        # We don't want want to connect a location to itself
        if a == b:
            return
        # We don't want to connect stuff twice
        for con in self.connections_buffer:
            if con[0] == a and con[1] == b:
                return
            if con[1] == a and con[0] == b:
                return
        # We append each student-made connection to a buffer to display connections
        # one by one afterwards.
        self.connections_buffer.append((a, b))

    def update(self):
        """
        Called each frame, updates the game state.
        """
        self.handle_events()
        self.update_animations()
        self.draw()
        # Update the window
        pygame.display.update()

    def handle_events(self):
        """
        Handle pygame events. Closes the program when the window is closed
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.active = False

    def update_animations(self):
        """
        Depending on the current step of the game, call the right function.
        """
        if self.step < len(self.steps):
            self.steps[self.step]()

    def wait_step(self):
        """
        Ensures the game waits a bit after being launched before animating connections.
        """
        # Wait a 100 frames and do nothing
        # Increment the timer each step
        self.timer += 1
        if self.timer > 100:
            # When we reach 100, go to the next step
            self.timer = 0
            self.step += 1

    def load_connections_step(self):
        """
        Slowly animate each connection.
        """
        self.timer += 1
        if len(self.connections_buffer):
            # Every 20 frames, add a connection to the screen
            if self.timer % 20 == 0:
                self.graph.add_connection(
                    self.connections_buffer[0][0], self.connections_buffer[0][1])
                self.connections_buffer.pop(0)
                #### COST ###############################################
                self.cost += self.graph.connections[-1].distance() * \
                    RAILWAY_UNIT_COST
                self.cost += CONNECTION_COST
                #########################################################
        else:
            # Once we've animated everything, we go to the next step.
            self.timer = 0
            self.step += 1

    def test_network_step(self):
        """
        Every 25 frames, test a new itinerary and evaluate it.
        """
        self.timer += 1
        # Every 25 frames.
        if self.timer % SHOW_CONNECTION_DELAY == 0:
            # We un-highlight every green-highlighted connection.
            self.test_network_highlight.clear()

            # If we have tested every itinerary. We end the testing step.
            if len(self.itineraries_to_test) == 0:
                self.step += 1
                return

            # We test an itinerary and remove it from the list of itineraries to test.
            itinerary = self.itineraries_to_test[-1]
            self.test_one_itinerary(itinerary)
            self.itineraries_to_test.pop()

    def test_one_itinerary(self, itinerary):
        """
        Test the commute from point A to point B.
        """
        # We get the shortest path from point A to point B.
        directions = self.graph.pathfind(itinerary.a, itinerary.b)

        # Maybe there's no path from A to B.
        if directions == None:
            self.network_error = "Some locations aren't connected"
            return

        ###### Traffic Congestion #############################
        # For each connection we check how often it's been used and
        # We calculate the variance of this data.
        loads = []
        for con in self.graph.connections:
            loads.append(con.times_used)
        if len(loads) > 1:
            self.traffic_congestion = statistics.variance(
                loads)
        else:
            self.traffic_congestion = 0
        #######################################################

        ###### Average Travel Time ############################
        # Each stop takes CHANGE_TRAIN_TIME mins.
        # Travelling a pixel on screen costs RAILWAY_UNIT_TRAVEL_TIME.
        self.num_travels += 1
        self.total_travel_time_mins += len(
            directions) * CHANGE_TRAIN_TIME
        for i in range(len(directions)):
            self.total_travel_time_mins += directions[i].distance() * \
                RAILWAY_UNIT_TRAVEL_TIME
        #######################################################

        # We highligh the connections we crossed during this commute in green.
        for i in range(len(directions)):
            self.test_network_highlight.append(directions[i])


####################################################
#### DRAW FUNCTION #################################
####################################################

    def draw(self):
        # Draw everything on screen every frame.

        # Draw a white background
        self.window.fill((255, 255, 255))
        tmp = self.assets.background_image.convert()
        tmp.set_alpha(128)
        self.window.blit(tmp, (0, HEADER_HEIGHT))
        # Draw the game header
        self.draw_header()
        # Draw each connection
        self.draw_connections()
        # Draw each connection
        self.draw_locations()

    def draw_header(self):
        # Pygame code to display the whole header
        warning_text_sf = self.font.render(self.network_error, True, RED)
        text_rect = warning_text_sf.get_rect(
            center=(self.window.get_rect().center[0], HEADER_HEIGHT + 10))
        self.window.blit(warning_text_sf, text_rect)
        self.window.blit(self.assets.uom_logo, (0, 0))
        self.draw_header_value('Average Travel Time',
                               str(math.floor(self.total_travel_time_mins / self.num_travels)) + 'min' if self.num_travels else '0min', 500, GREY)
        self.draw_header_value('Cost', str(
            math.floor(self.cost)) + 'mi$', 670, GREY)
        self.draw_header_value('Traffic congestion',
                               f'{self.traffic_congestion:.2f}', 820, GREY)
        pygame.draw.line(self.window, UOM_MAIN_COLOR, (0, HEADER_HEIGHT -
                         HEADER_LINE_WIDTH), (WINDOW_WIDTH, HEADER_HEIGHT - HEADER_LINE_WIDTH), HEADER_LINE_WIDTH)

    def draw_header_value(self, title: str, value: str, x_offset: int, color: tuple):
        # Pygame code to display one KPI
        text_surface = self.font.render(title, True, color)
        text_rect = text_surface.get_rect(
            center=(x_offset, HEADER_HEIGHT / 2 - 10))
        self.window.blit(text_surface, text_rect)

        text_surface = self.big_font.render(value, True, color)
        text_rect = text_surface.get_rect(
            center=(x_offset, HEADER_HEIGHT / 2 + 10))
        self.window.blit(text_surface, text_rect)

    def draw_locations(self):
        # Draw each location with a circle and the name.
        for loc in self.locations:
            pygame.draw.circle(
                self.window, COLORS[loc.color], (loc.x, loc.y), 10)
            text_surface = self.font.render(
                loc.name, True, (0, 0, 0), EXTREME_LIGHT_GREY)
            text_rect = text_surface.get_rect(
                center=(loc.x, loc.y + 20))
            self.window.blit(text_surface, text_rect)

    def draw_connections(self):
        # For each connection draw a grey line.
        for con in self.graph.connections:
            pygame.draw.line(self.window, GREEN if con in self.test_network_highlight else GREY,
                             (con.a.x, con.a.y), (con.b.x, con.b.y), 6 if con in self.test_network_highlight else 4)
