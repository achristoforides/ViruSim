# sim2.py

import pygame
import random

SEED = 69

WIDTH = 885
HEIGHT = 600

AGENT_SIZE = 5

AGENTS_PER_ROW = int(WIDTH / AGENT_SIZE)
AGENTS_PER_COL = int(HEIGHT / AGENT_SIZE)
MAX_AGENTS = AGENTS_PER_ROW * AGENTS_PER_COL

SUSCEPTIBLE = 0
INFECTED = 1
RECOVERED = 2

BLACK = (0, 0, 0)
BLUE = (134, 205, 242)
RED = (246, 150, 121)
PURPLE = (157, 135, 186)

POPULATION_DENSITY = 0.5
RADIUS = 1
INFECT_CHANCE = 0.01
RECOVERY_CHANCE = 0.0005
STARTING_INFECTED = 5

class Agent():

    def __init__(self, screen, x, y, r, c, disease = None):
        self.screen = screen
        self.x = x
        self.y = y
        self.r = r
        self.c = c
        #print(str(x) + ", " + str(y))
        #self.pos = pos
        self.disease = disease
        
    def update(self, grid):
        if self.disease:
            if not self.disease.recovering:
                self.infect_check(grid)

                self.recover_check()
        
        return

    def draw(self):
        if self.disease:
            if self.disease.recovering:
                pygame.draw.rect(self.screen, PURPLE, [self.x, self.y, AGENT_SIZE, AGENT_SIZE])
            else:
                pygame.draw.rect(self.screen, RED, [self.x, self.y, AGENT_SIZE, AGENT_SIZE])
        else:
            pygame.draw.rect(self.screen, BLUE, [self.x, self.y, AGENT_SIZE, AGENT_SIZE])

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
                col = col + i

                if random.random() < orig_infect_chance:
                    if valid_index(row, col):
                        if grid[row][col]:
                            if not grid[row][col].disease:
                                grid[row][col].disease = Disease(orig_radius, orig_infect_chance, orig_recovery_chance)

            for i in range(1, (radius * 2) + 1):
                row = row + i

                if random.random() < orig_infect_chance:
                    if valid_index(row, col):
                        if grid[row][col]:
                            if not grid[row][col].disease:
                                grid[row][col].disease = Disease(orig_radius, orig_infect_chance, orig_recovery_chance)
        
            for i in range(1, (radius * 2) + 1):
                col = col - i

                if random.random() < orig_infect_chance:
                    if valid_index(row, col):
                        try:
                            if grid[row][col]:
                                if not grid[row][col].disease:
                                    grid[row][col].disease = Disease(orig_radius, orig_infect_chance, orig_recovery_chance)
                        except IndexError:
                            print(str(row) +", "+ str(col))

            for i in range(1, (radius * 2) + 1):
                row = row - i

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
        

def main():
    random.seed(SEED)

    pygame.init()
    
    screen = pygame.display.set_mode([WIDTH, HEIGHT])

    grid = []

    initial_infected = random.choices(range(0, MAX_AGENTS), k=STARTING_INFECTED)

    for r in range(AGENTS_PER_COL):
        row = []
        for c in range(AGENTS_PER_ROW):
            x = c * AGENT_SIZE
            y = r * AGENT_SIZE
        
            if r * AGENTS_PER_COL + c in initial_infected:
                disease = Disease(RADIUS, INFECT_CHANCE, RECOVERY_CHANCE)
                
                row.append(Agent(screen, x, y, r, c, disease))
            elif random.random() < POPULATION_DENSITY:
                row.append(Agent(screen, x, y, r, c))
            else:
                row.append(None)

        grid.append(row)
                
    running = True

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(BLACK)

        for row in grid:
            for agent in row:
                if agent:
                    agent.update(grid)

        for row in grid:
            for agent in row:
                if agent:
                    agent.draw()
                    
        pygame.display.flip()

    return


if __name__ == "__main__":
    main()

