# -*- coding: utf-8 -*-
"""
Created on Fri Oct 10 14:38:51 2014

@author: cyprien
"""

import pygame
from pygame.locals import *
import time

UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3

class SnakeModel:
    """ Encodes the game state """
    def __init__(self):
        self.snake = Snake()
        self.score = 0

class SnakeBlock:
    def __init__(self,color,height,width,x,y,direction):
        self.color = color
        self.height = height
        self.width = width
        self.x = x
        self.y = y
        self.direction = direction
        
        self.delay = 0
        self.lastDir = 0

    def move(self):
        self.delay -= 1

        if self.delay > 0:
            direction = self.lastDir
        else:
            direction = self.direction
        
        if direction == 0:
            self.y -= 20
        if direction == 1:
            self.y += 20
        if direction == 2:
            self.x -= 20
        if direction == 3:
            self.x += 20

class Snake:
    def __init__(self):
        self.blocks = []

        for i in range(4):
            self.addBlock((0,0,0), 20, 20, 1)

    def addBlock(self, color,height,width,direction):
        x = y = 200

        if len(self.blocks) > 0:
            block = self.blocks[-1]
            if block.direction == 0:
                x = block.x
                y = block.y + 20            
            if block.direction == 1:
                x = block.x
                y = block.y - 20 
            if block.direction == 2:
                x = block.x + 20
                y = block.y 
            if block.direction == 3:
                x = block.x - 20
                y = block.y
        self.blocks.append(SnakeBlock(color, height, width, x, y, direction))

    def move(self):
        for block in self.blocks:
            block.move()

class PyGameWindowView:
    def __init__(self,model,screen):
        self.model = model
        self.screen = screen
        self.background = pygame.image.load("background.jpg").convert()

    def draw(self):
        screen.blit(self.background, (0,0))
        for blocks in self.model.snake.blocks:
            pygame.draw.rect(self.screen, pygame.Color(blocks.color[0],blocks.color[1],blocks.color[2]),pygame.Rect(blocks.x,blocks.y,blocks.width,blocks.height))

        pygame.draw.rect(screen, (0,0,0), (0,0,640,50), 0)


        myfont = pygame.font.SysFont("monospace", 40)
        label = myfont.render("Score:"+str(self.model.score), 1, (255,255,0))
        screen.blit(label, (200, 5))
        
        pygame.display.update()

class PyGameKeyboardController:
    def __init__(self,model):
        self.model = model

    def handle_key_event(self,event):
        direction = 0
        if event.key == K_LEFT:
            direction = LEFT
        if event.key == K_UP:
            direction = UP
        if event.key == K_RIGHT:
            direction = RIGHT
        if event.key == K_DOWN:
            direction = DOWN

        delay = 1
        for block in self.model.snake.blocks:
            block.delay = delay
            block.lastDir = block.direction
            block.direction = direction
            delay += 1

if __name__ == '__main__':
    pygame.init()

    size = (640,480)
    screen = pygame.display.set_mode(size)

    model = SnakeModel()
    view = PyGameWindowView(model,screen)
    controller = PyGameKeyboardController(model)

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            if event.type == KEYDOWN:
                controller.handle_key_event(event)
        model.snake.move()
        view.draw()
        time.sleep(.1)

    pygame.quit()
