"""
Modified on Feb 20 2020
@author: lbg@dongseo.ac.kr
"""

import pygame
from sys import exit
import numpy as np
    
width = 800
height = 600
pygame.init()
screen = pygame.display.set_mode((width, height), 0, 32)

background_image_filename = 'image/curve_pattern.png'
symbol_image_filename = 'image/icon_speech.png'

background = pygame.image.load(background_image_filename).convert()
width, height = background.get_size()
screen = pygame.display.set_mode((width, height), 0, 32)

symbol = pygame.image.load(symbol_image_filename).convert_alpha()
symbol_width, symbol_height = symbol.get_size()

#screen = pygame.display.set_mode((width, height), 0, 32)
pygame.display.set_caption("ImageMouseMOve")
loop = 0
 
screen.blit(background, (0,0))
# https://kite.com/python/docs/pygame.Surface.blit
clock= pygame.time.Clock()

#Loop until the user clicks the close button.
done = False
while not done:   
    # This limits the while loop to a max of 10 times per second.
    # Leave this out and we will use all CPU we can.
    time_passed = clock.tick(30)
    current_time = clock.get_time()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
            
    x, y = pygame.mouse.get_pos()
    print("mouse x:"+repr(x)+" y:"+repr(y)+" tick:"+repr(time_passed)+" time:"+repr(current_time)+" loop:"+repr(loop))
    screen.blit(background, (0,0))
    screen.blit(symbol, (x-symbol_width/2, y-symbol_height/2))    

    # Go ahead and update the screen with what we've drawn.
    # This MUST happen after all the other drawing commands.
    pygame.display.update()
    loop += 1

pygame.quit()
