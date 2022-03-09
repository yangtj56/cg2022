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

background = pygame.image.load(background_image_filename).convert()
width, height = background.get_size()
screen = pygame.display.set_mode((width, height), 0, 32)
pygame.display.set_caption("ImagePolyline")
  
# Define the colors we will use in RGB format
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE =  (  0,   0, 255)
GREEN = (  0, 255,   0)
RED =   (255,   0,   0)

old_pt = np.array([0, 0])
cur_pt = np.array([0, 0])
 
screen.blit(background, (0,0))
# https://kite.com/python/docs/pygame.Surface.blit
clock= pygame.time.Clock()

#Loop until the user clicks the close button.
done = False
while not done:   
    # This limits the while loop to a max of 10 times per second.
    # Leave this out and we will use all CPU we can.
    time_passed = clock.tick(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
            
    x, y = pygame.mouse.get_pos()
    cur_pt = np.array([x, y])
    if old_pt[0] != 0 and old_pt[1] != 0: 
        pygame.draw.line(screen, GREEN, old_pt, cur_pt, 5)
    print("mouse x:"+repr(x)+" y:"+repr(y)+" tick:"+repr(time_passed)+" time:")
    old_pt = cur_pt   

    # Go ahead and update the screen with what we've drawn.
    # This MUST happen after all the other drawing commands.
    pygame.display.update()
pygame.quit()
