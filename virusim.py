import os, sys
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import random
import thorpy

from ui_helper import *

num_susceptible = 0
num_infected = 0
num_removed = 0

class Agent():

    def __init__(self, screen, x, y, r, c, disease = None):
        self.screen = screen
        self.x = x + 380
        self.y = y + 15
        self.r = r
        self.c = c
        self.disease = disease
        
    def update(self, grid):
        if self.disease:
            if not self.disease.recovering:
                self.infect_check(grid)

                self.recover_check()
        
        return

    def draw(self):
        global num_susceptible
        global num_infected
        global num_removed
        if self.disease:
            if self.disease.recovering:
                pygame.draw.rect(self.screen, PURPLE, [self.x, self.y, AGENT_SIZE, AGENT_SIZE])
                num_removed += 1
            else:
                pygame.draw.rect(self.screen, RED, [self.x, self.y, AGENT_SIZE, AGENT_SIZE])
                num_infected += 1
        else:
            pygame.draw.rect(self.screen, BLUE, [self.x, self.y, AGENT_SIZE, AGENT_SIZE])
            num_susceptible += 1

        return
            
    def infect_check(self, grid):
        #row = self.r
        #col = self.c
        orig_radius = self.disease.radius
        orig_infect_chance = self.disease.infect_chance
        orig_recovery_chance = self.disease.recovery_chance
        
        radius = self.disease.radius

        while radius > 0:
            row = self.r - radius
            col = self.c - radius

            if random.random() < orig_infect_chance:
                if valid_index(row, col):
                    if grid[row][col]:
                        if not grid[row][col].disease:
                            grid[row][col].disease = Disease(orig_radius, orig_infect_chance, orig_recovery_chance)
                        
            for i in range(1, (radius * 2) + 1):
                col = col + 1

                if random.random() < orig_infect_chance:
                    if valid_index(row, col):
                        if grid[row][col]:
                            if not grid[row][col].disease:
                                grid[row][col].disease = Disease(orig_radius, orig_infect_chance, orig_recovery_chance)

            for i in range(1, (radius * 2) + 1):
                row = row + 1

                if random.random() < orig_infect_chance:
                    if valid_index(row, col):
                        if grid[row][col]:
                            if not grid[row][col].disease:
                                grid[row][col].disease = Disease(orig_radius, orig_infect_chance, orig_recovery_chance)
        
            for i in range(1, (radius * 2) + 1):
                col = col - 1

                if random.random() < orig_infect_chance:
                    if valid_index(row, col):
                        try:
                            if grid[row][col]:
                                if not grid[row][col].disease:
                                    grid[row][col].disease = Disease(orig_radius, orig_infect_chance, orig_recovery_chance)
                        except IndexError:
                            print(str(row) +", "+ str(col))

            for i in range(1, (radius * 2) + 1):
                row = row - 1

                if random.random() < orig_infect_chance:
                    if valid_index(row, col):
                        if grid[row][col]:
                            if not grid[row][col].disease:
                                grid[row][col].disease = Disease(orig_radius, orig_infect_chance, orig_recovery_chance)

            radius = radius - 1

                            
        return

    def recover_check(self):
        if random.random() < RECOVERY_CHANCE:
            self.disease.recovering = True
        
        return

class Disease():

    def __init__(self, radius, infect_chance, recovery_chance):
        self.radius = radius
        self.infect_chance = infect_chance
        self.recovery_chance = recovery_chance
        self.recovering = False


def valid_index(row, col):
    if row < 0 or row >= AGENTS_PER_COL:
        return False
    if col < 0 or col >= AGENTS_PER_ROW:
        return False

    return True

# Simulation Variables
sim_running = False
SEED = 123456789
WIDTH = 885
HEIGHT = 600
AGENT_SIZE = 15 # This should be 5 or 15

AGENTS_PER_ROW = int(WIDTH / AGENT_SIZE)
AGENTS_PER_COL = int(HEIGHT / AGENT_SIZE)
MAX_AGENTS = 0

SUSCEPTIBLE = 0
INFECTED = 1
RECOVERED = 2

BLACK = (0, 0, 0)
BLUE = (134, 205, 242)
RED = (246, 150, 121)
PURPLE = (157, 135, 186)

POPULATION_DENSITY = 0.2
RADIUS = 1
INFECT_CHANCE = 0.001
RECOVERY_CHANCE = 0.0005
STARTING_INFECTED = 5

current_graph_x = 15

# UI max values
max_infection_chance = 1.0
infection_chance_default_value = 0.5
max_infection_radius = 10
infection_radius_default_value = 1
max_population_density = 1.0
population_density_default_value = 0.5
max_recovery_chance = 1.0
recovery_chance_default_value = 0.01

# Setup simulation parameter UI elements
infection_chance_slider = None
infection_radius_slider = None
population_density_slider = None
recovery_chance_slider = None
starting_infected_textbox = None
seed_textbox = None
run_sim_button = None

grid = []

surface = None
prior_graph_lines = []

def start_simulation():
    global sim_running
    global POPULATION_DENSITY
    global RADIUS
    global INFECT_CHANCE
    global RECOVERY_CHANCE
    global STARTING_INFECTED
    global MAX_AGENTS

    global infection_chance_slider
    global infection_radius_slider
    global population_density_slider
    global recovery_chance_slider
    global starting_infected_textbox
    global seed_textbox

    global num_susceptible
    global num_infected
    global num_removed

    global current_graph_x
    global grid
    global prior_graph_lines

    if sim_running == True:
        return
    
    num_susceptible = 0
    num_infected = 0
    num_removed = 0
    current_graph_x = 15

    MAX_AGENTS = 0

    grid = []
    prior_graph_lines = []

    SEED = int(seed_textbox.get_value())
    random.seed(SEED)

    POPULATION_DENSITY = float(population_density_slider.get_value())
    RADIUS = int(infection_radius_slider.get_value())
    INFECT_CHANCE = float(infection_chance_slider.get_value())
    RECOVERY_CHANCE = float(recovery_chance_slider.get_value())
    STARTING_INFECTED = int(starting_infected_textbox.get_value())
    
    initial_infected = random.choices(range(0, AGENTS_PER_ROW * AGENTS_PER_COL), k=STARTING_INFECTED)

    for r in range(AGENTS_PER_COL):
        row = []
        for c in range(AGENTS_PER_ROW):
            x = c * AGENT_SIZE
            y = r * AGENT_SIZE
        
            if r * AGENTS_PER_COL + c in initial_infected:
                disease = Disease(RADIUS, INFECT_CHANCE, RECOVERY_CHANCE)
                
                row.append(Agent(surface, x, y, r, c, disease))
                MAX_AGENTS += 1
            elif random.random() < POPULATION_DENSITY:
                row.append(Agent(surface, x, y, r, c))
                MAX_AGENTS += 1
            else:
                row.append(None)

        grid.append(row)

    sim_running = True

def restart_simulation():
    global sim_running
    global POPULATION_DENSITY
    global RADIUS
    global INFECT_CHANCE
    global RECOVERY_CHANCE
    global STARTING_INFECTED
    global MAX_AGENTS

    global infection_chance_slider
    global infection_radius_slider
    global population_density_slider
    global recovery_chance_slider
    global starting_infected_textbox
    global seed_textbox

    global num_susceptible
    global num_infected
    global num_removed

    global current_graph_x
    global grid
    global prior_graph_lines

    num_susceptible = 0
    num_infected = 0
    num_removed = 0
    current_graph_x = 15

    MAX_AGENTS = 0

    grid = []
    prior_graph_lines = []

    SEED = int(seed_textbox.get_value())
    random.seed(SEED)

    POPULATION_DENSITY = float(population_density_slider.get_value())
    RADIUS = int(infection_radius_slider.get_value())
    INFECT_CHANCE = float(infection_chance_slider.get_value())
    RECOVERY_CHANCE = float(recovery_chance_slider.get_value())
    STARTING_INFECTED = int(starting_infected_textbox.get_value())
    
    initial_infected = random.choices(range(0, AGENTS_PER_ROW * AGENTS_PER_COL), k=STARTING_INFECTED)

    for r in range(AGENTS_PER_COL):
        row = []
        for c in range(AGENTS_PER_ROW):
            x = c * AGENT_SIZE
            y = r * AGENT_SIZE
        
            if r * AGENTS_PER_COL + c in initial_infected:
                disease = Disease(RADIUS, INFECT_CHANCE, RECOVERY_CHANCE)
                
                row.append(Agent(surface, x, y, r, c, disease))
                MAX_AGENTS += 1
            elif random.random() < POPULATION_DENSITY:
                row.append(Agent(surface, x, y, r, c))
                MAX_AGENTS += 1
            else:
                row.append(None)

        grid.append(row)

    sim_running = True

def pause_simulation():
    global sim_running
    sim_running = not sim_running

if __name__ == "__main__":
    running = True
    
    app_title = "ViruSim"
    app_dimensions = (1280, 720)

    pygame.font.init()
    UI_TITLE_FONT = pygame.font.SysFont('Consolas', 32)
    STATS_FONT = pygame.font.SysFont('Consolas', 18)
    BYLINE_FONT = pygame.font.SysFont('Consolas', 14)

    # Create the window
    surface = pygame.display.set_mode(size=app_dimensions, flags=pygame.DOUBLEBUF)
    pygame.display.flip()

    # Set window title
    pygame.display.set_caption(app_title)

    clock = pygame.time.Clock()

    background = (100, 100, 100)
    
    # Setup UI panels
    graph_panel = UIPanel(15, 15, 350, 350, (70, 70, 70), 'Graph', UI_TITLE_FONT, (0, 0, 0))
    param_panel = UIPanel(15, 380, 350, 295, (70, 70, 70), 'Parameters', UI_TITLE_FONT, (0, 0, 0))
    simul_panel = UIPanel(380, 15, 885, 600, (0, 0, 0), 'Simulation Area', UI_TITLE_FONT, (0, 0, 0))
    stats_panel = UIPanel(410, 630, 825, 75, (70, 70, 70), 'Statistics', UI_TITLE_FONT, (0, 0, 0))

    STATS_PADDING = 30
    sus_def_text = 'Susceptible: '
    inf_def_text = 'Infected: '
    rem_def_text = 'Removed: '
    susceptible_text = STATS_FONT.render(sus_def_text, True, (0, 0, 0))
    infected_text = STATS_FONT.render(inf_def_text, True, (0, 0, 0))
    removed_text = STATS_FONT.render(rem_def_text, True, (0, 0, 0))

    author_line = BYLINE_FONT.render('ViruSim, Alex Christoforides and Chris Dicovskiy', True, (0,0,0))
    
    # Setup simulation parameter UI elements
    infection_chance_slider = thorpy.SliderX(100, (0.0, max_infection_chance), 'Infection Chance', initial_value=infection_chance_default_value)
    infection_radius_slider = thorpy.SliderX(100, (0, max_infection_radius), 'Infection Radius', type_=int, initial_value=infection_radius_default_value)
    population_density_slider = thorpy.SliderX(100, (0.0, max_population_density), 'Population Density %', initial_value=population_density_default_value)
    recovery_chance_slider = thorpy.SliderX(100, (0.0, max_recovery_chance), 'Recovery Chance %', initial_value=recovery_chance_default_value)
    starting_infected_textbox = thorpy.Inserter(name="Initial Agents Infected: ", value=str(5))
    seed_textbox = thorpy.Inserter(name="Random Seed: ", value=str(SEED))
    run_sim_button = thorpy.make_button('Run Simulation', func=start_simulation)
    pause_sim_button = thorpy.make_button('Pause/Resume Simulation', func=pause_simulation)
    restart_sim_button = thorpy.make_button('Restart Simulation', func=restart_simulation)

    param_box = thorpy.Box(elements=[infection_chance_slider,infection_radius_slider,population_density_slider, recovery_chance_slider, starting_infected_textbox, seed_textbox, run_sim_button, pause_sim_button, restart_sim_button])
    
    simulation_parameters_menu = thorpy.Menu(param_box, fps=60)
    for element in simulation_parameters_menu.get_population():
        element.surface = surface

    param_box.set_topleft((48, 380 + param_panel.get_title_height()))
    param_box.set_main_color((70, 70, 70))
    param_box.blit()
    param_box.update()

    counter = 0
    
    starting_graph_y = 55
    ending_graph_y = starting_graph_y + 310
    diff_y = ending_graph_y - starting_graph_y
    while running:
        num_susceptible = 0
        num_infected = 0
        num_removed = 0
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            simulation_parameters_menu.react(event)

        surface.fill(background)
        
        # Sketch out locations of UI elements
        graph_panel.draw(surface)
        graph_panel.render_panel_title_text(surface)
        param_panel.draw(surface)
        param_panel.render_panel_title_text(surface)
        simul_panel.draw(surface)
        stats_panel.draw(surface)
        stats_panel.render_panel_title_text(surface)
        
        # Draw UI Elements
        param_box.blit()

        if sim_running and counter % 10 == 0:
            for row in grid:
                for agent in row:
                    if agent:
                        agent.update(grid)

        for row in grid:
            for agent in row:
                if agent:
                    agent.draw()

        # Draw stats text
        susceptible_text = STATS_FONT.render(sus_def_text + str(num_susceptible), True, BLUE)
        infected_text = STATS_FONT.render(inf_def_text + str(num_infected), True, RED)
        removed_text = STATS_FONT.render(rem_def_text + str(num_removed), True, PURPLE)
        surface.blit(susceptible_text, (600, 630 + stats_panel.get_title_height() + 5))
        surface.blit(infected_text, (STATS_PADDING + 600 + susceptible_text.get_width(), 630 + stats_panel.get_title_height() + 5))
        surface.blit(removed_text, (STATS_PADDING * 2 + 600 + susceptible_text.get_width() + infected_text.get_width(), 630 + stats_panel.get_title_height() + 5))

        surface.blit(author_line, (15, 687))

        pygame.draw.line(surface, (0, 0, 0), (7, 7), (1273, 7))
        pygame.draw.line(surface, (0, 0, 0), (7, 7), (7, 713))
        pygame.draw.line(surface, (0, 0, 0), (7, 713), (1273, 713))
        pygame.draw.line(surface, (0, 0, 0), (1273, 7), (1273, 713))

        for partial in prior_graph_lines:
            for segment in partial:
                point1 = segment[0]
                point2 = segment[1]
                color = segment[2]
                pygame.draw.line(surface, color, point1, point2)

        if counter % 10 == 0 and sim_running and current_graph_x <= 365:
            skip_second_to_last = False
            skip_last = False
            tList = []
            tempY = starting_graph_y
            #rem -> sus -> inf
            t = tempY + int((num_removed / MAX_AGENTS) * diff_y)
            if num_susceptible == 0:
                t = 365
                skip_second_to_last = True
            tList.append([(current_graph_x, tempY), (current_graph_x, t), PURPLE])
            pygame.draw.line(surface, PURPLE, (current_graph_x, tempY), (current_graph_x, t))
            tempY = t
            t = tempY + int((num_susceptible / MAX_AGENTS) * diff_y)
            if num_infected == 0:
                t = 365
                skip_last = True
            if not skip_second_to_last:
                tList.append([(current_graph_x, tempY), (current_graph_x, t), BLUE])                        
                pygame.draw.line(surface, BLUE, (current_graph_x, tempY), (current_graph_x, t))
                tempY = t
            t = 365
            if not skip_last:
                tList.append([(current_graph_x, tempY), (current_graph_x, t), RED])
                pygame.draw.line(surface, RED, (current_graph_x, tempY), (current_graph_x, t))
            prior_graph_lines.append(tList)
            current_graph_x += 1
            if current_graph_x == 365:
                sim_running = False
        
        # Update the window
        pygame.display.update()

        clock.tick(60)
        counter += 1

# Pause sim button
# Reset sim button
