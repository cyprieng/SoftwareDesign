# -*- coding: utf-8 -*-
"""
Game of snake

@author: Cyprien, Leo, Harsh
"""

#Import
import pygame
from pygame.locals import *
import time
from random import randrange

#DIRECTION OF THE SNAKE
UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3

class SnakeModel:
    """ Encodes the game state """
    def __init__(self):
        """ Init the game """
        self.snake = Snake()
        self.score = 0
        self.eatBlocks = []
        self.eatBlocks.append(EatBlock())

    def move(self):
      """ Move the snake and handle event like collision """
      #Move Snake
      self.snake.move()

      #Detect eating
      for block in self.snake.blocks:
        for eatblock in self.eatBlocks:
          if block.x == eatblock.x and block.y == eatblock.y:
            #Add block to snake, remove eat block, add a new eat block and update score
            self.eatBlocks.remove(eatblock)
            self.snake.addBlock()
            self.eatBlocks.append(EatBlock())
            self.score += 10

        #Detect snake collision
        collision = 0
        for block2 in self.snake.blocks:
          if block.x == block2.x and block.y == block2.y:
            collision += 1

            #The snake is eating itself => Game Over
            if collision == 2:
              self.snake.stop = True
              break

    def restart(self):
      """ Restart a game """
      self.score = 0
      self.snake.blocks = []
      self.snake.direction = UP
      self.snake.stop = False

      for i in range(4):
          self.snake.addBlock()

class Block(object):
    """ Represent a block of the Snake """
    def __init__(self,x,y):
        self.x = x
        self.y = y

class EatBlock(Block):
    """ Represent a block that the snake need to eat """
    def __init__(self):
        Block.__init__(self,randrange(32)*20,randrange(3,24)*20)

class Snake:
    """ Represent the snake """
    def __init__(self):
        """ Init snake state """
        self.blocks = []
        self.direction = UP
        self.stop = False

        #Add some blocks
        for i in range(4):
            self.addBlock()

    def addBlock(self):
        """ Add a block to the snake """
        x = y = 200 #Default position

        #If it is not the first block
        if len(self.blocks) > 0:
            #Set the position relatively to the last block
            direction = self.direction
            block = self.blocks[-1]

            if direction == UP:
                x = block.x
                y = block.y - 20
            if direction == DOWN:
                x = block.x
                y = block.y + 20
            if direction == LEFT:
                x = block.x - 20
                y = block.y
            if direction == RIGHT:
                x = block.x + 20
                y = block.y

            #Screen Overflow
            if x < 0:
              x = 620
            if x > 620:
              x = 0
            if y < 60:
              y = 460
            if y > 460:
              y = 60

        #Add block
        self.blocks.append(Block(x, y))

    def move(self):
        """ Move the snake """
        if self.stop == False:
          self.addBlock() #Add block at the head
          self.blocks.pop(0)  #Remove block at the tail


class PyGameWindowView:
    """ View of the game: print everything on the screen """
    def __init__(self,model,screen):
        """ Init the view """
        self.model = model
        self.screen = screen

        """ Load image of the snake """
        self.background = pygame.image.load("background.jpg").convert()
        self.block = pygame.image.load("block.png").convert_alpha()
        self.head = pygame.image.load("head.png").convert_alpha()

    def draw(self):
        """ Draw everything on screen """
        #Print the background
        screen.blit(self.background, (0,0))

        #Print the snake
        i=len(self.model.snake.blocks) -1
        for block in self.model.snake.blocks:
            if i == 0: #It is the head
              screen.blit(self.head, (block.x,block.y))
            else:
              screen.blit(self.block, (block.x,block.y))

            i -= 1

        #Print eat block
        for eatblock in self.model.eatBlocks:
            screen.blit(self.block, (eatblock.x,eatblock.y))

        #Draw score panel
        pygame.draw.rect(screen, (0,0,0), (0,0,640,60), 0)
        if self.model.snake.stop == True: #Game over
          myfont = pygame.font.SysFont("monospace", 20)
          label = myfont.render("Game over, press enter to restart. (Score:"+str(self.model.score)+")", 1, (255,255,255))
          screen.blit(label, (10, 15))
        else:
          myfont = pygame.font.SysFont("monospace", 40)
          label = myfont.render("Score:"+str(self.model.score), 1, (255,255,255))
          screen.blit(label, (200, 5))

        pygame.display.update()

class PyGameKeyboardController:
    """ Handle keyboard input """
    def __init__(self,model):
        """ Init controller """
        self.model = model

    def handle_key_event(self,event):
        """ Handle keyboard event

        Keyword arguments:
        event -- event to handle
        """
        #Get arrow key
        lastDir = self.model.snake.direction
        if event.key == K_LEFT and lastDir != RIGHT:
            self.model.snake.direction = LEFT
        if event.key == K_UP and lastDir != DOWN:
            self.model.snake.direction = UP
        if event.key == K_RIGHT and lastDir != LEFT:
            self.model.snake.direction = RIGHT
        if event.key == K_DOWN and lastDir != UP:
            self.model.snake.direction = DOWN

        #Enter to restart if the game is over
        if event.key == K_RETURN and self.model.snake.stop == True:
            self.model.restart()

if __name__ == '__main__':
    #Init pygame
    pygame.init()
    size = (640,480)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Snake")
    pygame.display.set_icon(pygame.image.load("head.png").convert_alpha())

    #Init MVC
    model = SnakeModel()
    view = PyGameWindowView(model,screen)
    controller = PyGameKeyboardController(model)

    #RUN
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
