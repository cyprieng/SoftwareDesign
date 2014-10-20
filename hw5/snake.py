# -*- coding: utf-8 -*-
"""
Created on Fri Oct 10 14:38:51 2014

@author: cyprien
"""

import pygame
from pygame.locals import *
import time
from random import randrange

UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3

class SnakeModel:
    """ Encodes the game state """
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.snake = Snake()
        self.score = 0
        self.eatBlocks = []

        self.eatBlocks.append(EatBlock((255,0,0), 20, 20))

    def move(self):
      self.snake.move()

      #Eating
      for block in self.snake.blocks:
        for eatblock in self.eatBlocks:
          if block.x == eatblock.x and block.y == eatblock.y:
            self.eatBlocks.remove(eatblock)
            self.snake.addBlock((0,0,0), 20, 20)
            self.eatBlocks.append(EatBlock((255,0,0), 20, 20))
            self.score += 10

        collision = 0
        for block2 in self.snake.blocks:
          if block.x == block2.x and block.y == block2.y:
            collision += 1

            if collision == 2:
              self.snake.stop = True
              break

    def restart(self):
      self.score = 0

      self.snake.blocks = []
      self.snake.direction = 0
      self.snake.stop = False

      for i in range(4):
          self.snake.addBlock((0,0,0), 20, 20)


class EatBlock:
    def __init__(self,color,height,width):
        self.color = color
        self.height = height
        self.width = width
        self.x = randrange(32)*20
        self.y = randrange(3,24)*20

class SnakeBlock:
    def __init__(self,color,height,width,x,y):
        self.color = color
        self.height = height
        self.width = width
        self.x = x
        self.y = y
        self.moveList = [0]
        self.indexMove = 0

class Snake:
    def __init__(self):
        self.blocks = []
        self.direction = 0
        self.stop = False

        for i in range(4):
            self.addBlock((0,0,0), 20, 20)

    def addBlock(self, color,height,width):
        x = y = 200

        if len(self.blocks) > 0:
            direction = self.direction
            block = self.blocks[-1]

            if direction == 0:
                x = block.x
                y = block.y - 20
            if direction == 1:
                x = block.x
                y = block.y + 20
            if direction == 2:
                x = block.x - 20
                y = block.y
            if direction == 3:
                x = block.x + 20
                y = block.y

            #Overflow
            if x < 0:
              x = 640
            if x > 640:
              x = 0
            if y < 60:
              y = 480
            if y > 480:
              y = 60

        self.blocks.append(SnakeBlock(color, height, width, x, y))

    def move(self):
        if self.stop == False:
          self.addBlock((0,0,0), 20, 20)
          self.blocks.pop(0)


class PyGameWindowView:
    def __init__(self,model,screen):
        self.model = model
        self.screen = screen
        self.background = pygame.image.load("background.jpg").convert()

    def draw(self):
        screen.blit(self.background, (0,0))
        for blocks in self.model.snake.blocks:
                pygame.draw.rect(self.screen, pygame.Color(blocks.color[0],blocks.color[1],blocks.color[2]),pygame.Rect(blocks.x,blocks.y,blocks.width,blocks.height))

        for eatblocks in self.model.eatBlocks:
            pygame.draw.rect(self.screen, pygame.Color(eatblocks.color[0],eatblocks.color[1],eatblocks.color[2]),pygame.Rect(eatblocks.x,eatblocks.y,eatblocks.width,eatblocks.height))

        pygame.draw.rect(screen, (0,0,0), (0,0,640,60), 0)


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
        if event.key == K_RETURN and self.model.snake.stop == True:
          self.model.restart()

        self.model.snake.direction = direction

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
                break

        model.move()
        view.draw()
        time.sleep(.1)

    pygame.quit()
