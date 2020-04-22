# sim.py
# 8-4-20

import pygame
import random as rd
import math
import pygame.math
import pygame.gfxdraw

from pygame.locals import *

vec = pygame.math.Vector2

rd.seed(69)

WIDTH = 885
HEIGHT = 600

SUSCEPTIBLE = 0
INFECTED = 1
RECOVERED = 2

MAX_SPEED = 0.25

DIRECTION_CHANGE_CHANCE = 0.05

def color(state):
    if state == SUSCEPTIBLE:
        return (134, 205, 242)
    elif state == INFECTED:
        return (246, 150, 121)
    else:
        return (157, 135, 186)

class Agent(pygame.sprite.Sprite):

    def __init__(self, id, state):
        pygame.sprite.Sprite.__init__(self)
        self.id = id
        self.state = state
        self.color = color(state)
        self.x = rd.randint(1, WIDTH - 1)
        self.y = rd.randint(1, HEIGHT - 1)
        self.pos = vec(self.x, self.y)
        #self.speed = 2
        self.size = 15
        self.image = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        
        #pygame.draw.circle(screen, self.color, (self.x, self.y), self.size)

        pygame.gfxdraw.aacircle(self.image, 0, 0, 50, self.color)
        pygame.gfxdraw.filled_circle(self.image, 0, 0, 50, self.color)

        self.original_image = self.image
        self.rect = self.image.get_rect(center=self.pos)

        self.vel = vec(0, 0)
        self.accel = vec(0, -0.2)
        self.angle_speed = 0
        self.angle = 0

    def update(self, all_agents):
        if self.state == INFECTED:
            self.recover_check()

        #if self.state == SUSCEPTIBLE:
            self.infect_check(all_agents)

        if rd.random() > DIRECTION_CHANGE_CHANCE:
            self.change_dir()

        self.vel += self.accel

        if self.vel.length() > MAX_SPEED:
            self.vel.scale_to_length(MAX_SPEED)

        self.pos += self.vel
        self.rect.center = self.pos

        self.wrap_around_screen()


    def change_dir(self):
        if rd.random() > 0.5:
            self.angle_speed = 5
        else:
            self.angle_speed = -5

        self.rotate()

        
    def rotate(self):
        self.accel.rotate_ip(self.angle_speed)

        self.angle += self.angle_speed

        if self.angle > 360:
            self.angle -= 360
        elif self.angle < 0:
            self.angle += 360
            
        self.image = pygame.transform.rotate(self.original_image, -self.angle)

        self.rect = self.image.get_rect(center=self.rect.center)
        

    def wrap_around_screen(self):
        
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH
        if self.pos.y <= 0:
            self.pos.y = HEIGHT
        if self.pos.y > HEIGHT:
            self.pos.y = 0

            
    def infect_check(self, all_agents):
        
        agents = pygame.sprite.spritecollide(self, all_agents, False)

        for agent in agents:
            #print("AA")

            agent = Agent(agent.id, INFECTED)
            
            #self.status = INFECTED
            #self.color = color(agent.state)

            #pygame.gfxdraw.aacircle(agent.image, 0, 0, 50, agent.color)
            #pygame.gfxdraw.filled_circle(agent.image, 0, 0, 50, agent.color)
        
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

ctrl = Controller(WIDTH, HEIGHT, 100, 2)

screen = pygame.display.set_mode([ctrl.x_size, ctrl.y_size])
clock = pygame.time.Clock()

all_agents = pygame.sprite.Group()

for i in range(0, ctrl.agent_count):
    if i < ctrl.starting_infected:
        all_agents.add(Agent(i, INFECTED))
    else:
        all_agents.add(Agent(i, SUSCEPTIBLE))

        
while ctrl.running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            ctrl.running = False

    all_agents.update(all_agents)

    screen.fill((0, 0, 0))

    all_agents.draw(screen)

    pygame.display.update()

pygame.quit()
        
