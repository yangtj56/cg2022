"""
Modified on Feb 20 2020
@author: lbg@dongseo.ac.kr
"""

import re
import pygame
from sys import exit
import numpy as np
    
width = 800
height = 600
pygame.init()
screen = pygame.display.set_mode((width, height), 0, 32)

pygame.display.set_caption("ImagePolylineMouseButton-Bezier")
  
# Define the colors we will use in RGB format
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE =  (  0,   0, 255)
GREEN = (  0, 255,   0)
RED =   (255,   0,   0)

pts = [] 
knots = []
count = 0
#screen.blit(background, (0,0))
screen.fill(WHITE)

# https://kite.com/python/docs/pygame.Surface.blit
clock= pygame.time.Clock()

def drawPoint(pt, color='GREEN', thick=3):
    # pygame.draw.line(screen, color, pt, pt)
    pygame.draw.circle(screen, color, pt, thick)

def drawLine(pt0, pt1, color='GREEN', thick=3):
    x = pt0[0]
    y = pt0[1]
    x1 = pt0[0]
    y1 = pt0[1]
    x2 = pt1[0]
    y2 = pt1[1]

    dx = abs(x2-x1)
    dy = abs(y2-y1)
    gradient = dy/dx

    if gradient >1:
        dx,dy = dy,dx
        x , y = y , x
        x1, y1 = y1, x1
        x2, y2 = y2, x2

    p = 2 * dy - dx

    for k in range(dx):
        x = x+1 if x < x2 else x-1
        if p>0:
            y = y+1 if y < y2 else y -1
            p = p+2*(dy-dx)
        else:
            p = p+2*dy

        if gradient < 1:
            drawPoint([x, y], color, thick)
        else:
            drawPoint([y, x], color, thick)
    # drawPoint((100,100), color,  thick)
    # drawPoint(pt0, color, thick)
    # drawPoint(pt1, color, thick)

def Fa(i):
    res = 1
    cur = i;
    count = i
    for j in range(count):
        res = res *cur
        cur=cur-1
    return res

def Bezier(t,i,n):
    return ( Fa(n)/(Fa(i)*Fa(n-i)))* pow(t,i) *pow(1-t,n-i)

def drawCurves(color='GREEN', thick=3):
    if(count < 3): return
    for dt in range(width):
        t = dt/width
        x = 0
        y = 0
        for ptIndex in range(count):
            bezier = Bezier(t,ptIndex,count-1)
            # print(repr(ptIndex)+":"+repr(bezier))
            x = x+  pts[ptIndex][0] * bezier
            y = y+  pts[ptIndex][1] * bezier

        drawPoint([x, y], color, thick)

def drawPolylines(color='GREEN', thick=3):
    if(count < 2): return
    for i in range(count-1):
        drawLine(pts[i], pts[i+1], color,thick)

#Loop until the user clicks the close button.
done = False
pressed = 0
margin = 6
old_pressed = 0
old_button1 = 0

while not done:   
    # This limits the while loop to a max of 10 times per second.
    # Leave this out and we will use all CPU we can.
    time_passed = clock.tick(30)

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            pressed = -1            
        elif event.type == pygame.MOUSEBUTTONUP:
            pressed = 1            
        elif event.type == pygame.QUIT:
            done = True
        else:
            pressed = 0

    button1, button2, button3 = pygame.mouse.get_pressed()
    x, y = pygame.mouse.get_pos()
    pt = [x, y]
    pygame.draw.circle(screen, RED, pt, 0)

    if old_pressed == -1 and pressed == 1 and old_button1 == 1 and button1 == 0 :
        pts.append(pt) 
        count += 1
        #print("len:"+repr(len(pts))+" mouse x:"+repr(x)+" y:"+repr(y)+" button:"+repr(button1)+" pressed:"+repr(pressed)+" add pts ...")
    #else:
        #print("len:"+repr(len(pts))+" mouse x:"+repr(x)+" y:"+repr(y)+" button:"+repr(button1)+" pressed:"+repr(pressed))

    for i in range(count):
        pygame.draw.rect(screen, BLUE, (pts[i][0]-margin, pts[i][1]-margin, 2*margin, 2*margin), 5)

    if len(pts)>1:
        drawPolylines(GREEN, 1)
        drawCurves(BLUE, 1)
    
    # Go ahead and update the screen with what we've drawn.
    # This MUST happen after all the other drawing commands.
    pygame.display.flip()
    screen.fill(WHITE)
    old_button1 = button1
    old_pressed = pressed

pygame.quit()