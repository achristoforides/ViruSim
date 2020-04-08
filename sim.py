# sim.py
# 8-4-20

import pygame
import random as rd

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
        self.x_pos = rd.randint(1, ctrl.x_size - 1)
        self.y_pos = rd.randint(1, ctrl.y_size - 1)
        self.speed = 10
        self.size = 7

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, [self.x_pos, self.y_pos], self.size)

        
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

    screen.fill((255, 255, 255))

    for agent in agents:
        agent.draw(screen)

    pygame.display.flip()

pygame.quit()
        
