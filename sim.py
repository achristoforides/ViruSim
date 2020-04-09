# sim.py
# 8-4-20

import pygame
import random as rd
import math
import pygame.math

rd.seed(69)

SUSCEPTIBLE = 0
INFECTED = 1
RECOVERED = 2


def color(state):
    if state == SUSCEPTIBLE:
        return (134, 205, 242)
    elif state == INFECTED:
        return (246, 150, 121)
    else:
        return (157, 135, 186)

class Agent():

    def __init__(self, id, state, ctrl):
        self.id = id
        self.state = state
        self.color = color(state)
        self.pos = [rd.randint(1, ctrl.x_size - 1), rd.randint(1, ctrl.y_size - 1)]
        self.speed = 2
        self.size = 10
        self.dir = 0

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.pos, self.size)

    def move(self, ctrl):
        self.dir = rd.randint(1, 4)

        if self.dir == 1:
            self.pos[0] += self.speed
        elif self.dir == 2:
            self.pos[0] -= self.speed
        elif self.dir == 3:
            self.pos[1] += self.speed
        else:
            self.pos[1] -= self.speed
        
    def infect(self):
        return
        
    def recover_check(self):
        return
        
    def death_check(self):
        return
        
        
class Disease():

    def __init__(self, infect_radius, infect_chance, recovery_time):
        self.infect_radius = infect_radius
        self.infect_chance = infect_chance
        self.recovery_time = recovery_time
        

        
class Controller():

    def __init__(self, x_size, y_size, agent_count, starting_infected):
        self.x_size = x_size
        self.y_size = y_size
        self.agent_count = agent_count
        self.starting_infected = starting_infected
        self.running = True


pygame.init()

ctrl = Controller(885, 600, 250, 10)

screen = pygame.display.set_mode([ctrl.x_size, ctrl.y_size])

agents = list()

for i in range(0, ctrl.agent_count):
    if i < ctrl.starting_infected:
        agents.append(Agent(i, INFECTED, ctrl))
    else:
        agents.append(Agent(i, SUSCEPTIBLE, ctrl))

while ctrl.running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            ctrl.running = False

    screen.fill((0, 0, 0))

    for agent in agents:
        agent.move(ctrl)
        agent.draw(screen)

    pygame.display.flip()

pygame.quit()
        
