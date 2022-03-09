"""
Modified on Feb 20 2020
@author: lbg@dongseo.ac.kr 
"""

background_image_filename = 'image/curve_pattern.png'
sprite_image_filename = 'image/icon_speech.png'

import pygame
from pygame.locals import *
from sys import exit
import numpy as np
    
# Define the colors we will use in RGB format
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE =  (  0,   0, 255)
GREEN = (  0, 255,   0)
RED =   (255,   0,   0)

pygame.init()
screen = pygame.display.set_mode((640, 480), 0, 32)
background = pygame.image.load(background_image_filename).convert()
sprite = pygame.image.load(sprite_image_filename).convert_alpha()
old_pt = np.array([0, 0])
cur_pt = np.array([0, 0])

font= pygame.font.SysFont("consolas",20) 
pygame.display.set_caption("Game Title")
  
#Loop until the user clicks the close button.
done = False
flag = None
button = 0
clock= pygame.time.Clock()
 
# print text function
def printText(msg, color='BLACK', pos=(50,50)):
    textSurface = font.render(msg, True, pygame.Color(color), None)
    textRect = textSurface.get_rect()
    textRect.topleft = pos
    screen.blit(textSurface, textRect)

while not done:   
    # This limits the while loop to a max of 10 times per second.
    # Leave this out and we will use all CPU we can.
    time_passed = clock.tick(10)

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN: # If user release what he pressed.
            pressed= pygame.key.get_pressed()
            buttons= [pygame.key.name(k) for k,v in enumerate(pressed) if v]
            flag= True
        elif event.type == pygame.KEYUP:# If user press any key.
            flag= False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            button = -1            
        elif event.type == pygame.MOUSEBUTTONUP:
            button = 1            
        elif event.type == pygame.QUIT:
            done = True
        else:
            button = 0                    
            
#    screen.blit(background, (0,0))
#    screen.blit(sprite, old_pt)
    time_passed_seconds = time_passed / 1000.0
    
    x, y = pygame.mouse.get_pos()
    cur_pt = np.array([x, y])
    vector_pt = cur_pt - old_pt
    pygame.draw.line(screen, GREEN, old_pt, cur_pt, 3)
    # print("x:"+repr(x)+" y:"+repr(y))
    # print(cur_pt)
    
     
    # All drawing code happens after the for loop and but
    # inside the main while done==False loop.
      
    # Clear the screen and set the screen background
    # screen.fill(WHITE)
    pygame.draw.rect(screen, WHITE, (50, 50, 400, 100))

    # Print red text if user pressed any key.
    if flag== True:
        printText('you just key down!!','RED')
        printText('--> you pressed any key.','RED', (50,70))
        printText('Pressed Key : ' + buttons[0],'RED', (50,90))
 
    # Print blue text if user released any key.
    elif flag== False:
        printText('you just key up!!','BLUE')
        printText('--> released what you pressed.','BLUE', (50,70))
 
    # Print default text if user do nothing.
    else:
        printText('Please press any key.')
        
    printText("x:"+repr(x)+" y:"+repr(y)+" button:"+repr(button), 'GREEN', (50,110))
 
#    vector_to_mouse = vector_to_mouse/np.linalg.norm(vector_to_mouse)
#    destination = Vector2( *pygame.mouse.get_pos() ) - Vector2( *sprite.get_size() )/2
#    vector_to_mouse = Vector2.from_points(position, destination)
#    vector_to_mouse.normalize()

    old_pt = cur_pt   
    # Go ahead and update the screen with what we've drawn.
    # This MUST happen after all the other drawing commands.
    pygame.display.flip()
    pygame.display.update()

pygame.quit()
