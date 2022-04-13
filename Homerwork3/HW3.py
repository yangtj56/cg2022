"""
Modified on Feb 20 2020
@author: lbg@dongseo.ac.kr
"""

import itertools

import numpy as np
import pygame

width = 800
height = 600

pygame.init()
screen = pygame.display.set_mode((width, height), 0, 32)
font = pygame.font.SysFont("consolas", 20)

pygame.display.set_caption(" Barycentric coordinates")

# Define the colors we will use in RGB format
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)


class MOUSE_BUTTON:
    LEFT = 0
    MIDDLE = 1
    RIGHT = 2


# screen.blit(background, (0,0))
screen.fill(WHITE)

# https://kite.com/python/docs/pygame.Surface.blit
clock = pygame.time.Clock()


def drawPoint(pt, color=GREEN, thick=3):
    pygame.draw.circle(screen, color, pt, thick)


def drawLine(pt0, pt1, k=0, color=GREEN, thick=3):
    # Numpy Implementation
    A = np.array([pt0, pt1]).T
    # Generate a0 and a1, with constraint a0 + a1 = 1 and a0, a1 >= 0
    dist = np.max(A)  # np.linalg.norm(A[:, 0] - A[:, 1])
    a0 = np.arange(0 - k, 1 + k, 1 / (dist * (k * 2)))
    a1 = 1 - a0
    a = np.array([a0, a1])

    XY = (A @ a).T  # Coords for points on the line between pt0 and pt1

    for x, y in XY:
        drawPoint((x, y), color, thick)


def drawPolylines(points, color=GREEN, thick=3):
    if len(points) < 2:
        return
    for i in range(len(points) - 1):
        drawLine(points[i], points[i + 1], color, thick=1)


def drawPolyLines2(points, color=GREEN, thick=3):
    if len(points) < 2:
        return
    drawLine(points[-2], points[-1], color, thick)


def draw_guidance(points):
    for pt1, pt2 in itertools.combinations(points, 2):
        drawLine(pt1, pt2, k=1, color=BLUE, thick=1)


def draw_text(msg, color=BLACK, pos=(50, 50)):
    text_surface = font.render(msg, True, pygame.Color(color), None)
    text_rect = text_surface.get_rect()
    text_rect.topleft = pos

    pygame.draw.rect(screen, WHITE, (0, text_rect.y, width, text_rect.h))

    screen.blit(text_surface, text_rect)


def cartesian_to_barycentric(pt1, pt2, pt3, pt):
    basis = np.array([pt1, pt2, pt3]).T
    basis_square = np.pad(basis, ((1, 0), (0, 0)), 'constant', constant_values=1)

    cartesian = np.array([1, *pt])

    barycentric_coords = np.linalg.inv(basis_square) @ cartesian
    return barycentric_coords


# Loop until the user clicks the close button.
done = False
margin = 6
pts = []
button = prev_button = (False, False, False)


def is_clicked(btn_idx: int):
    return button[btn_idx] and not prev_button[btn_idx]


while not done:
    # This limits the while loop to a max of 10 times per second.
    # Leave this out and we will use all CPU we can.
    time_passed = clock.tick(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    button = pygame.mouse.get_pressed()
    x, y = pygame.mouse.get_pos()
    pt = (x, y)
    pygame.draw.circle(screen, RED, pt, 0)

    # print("len:" + repr(len(pts)) + " mouse x:" + repr(x) + " y:" + repr(y) +
    #       " button:" + repr(button[0]) + " pressed:" + repr(button))

    if is_clicked(MOUSE_BUTTON.LEFT):
        if len(pts) >= 3:
            continue

        pts.append(pt)
        pygame.draw.rect(
            screen, RED, (pt[0] - margin, pt[1] - margin, 2 * margin, 2 * margin), 5)
        # drawPolyLines2(pts, GREEN, 1)
        draw_guidance(pts)

    elif is_clicked(MOUSE_BUTTON.RIGHT):
        pts.clear()
        screen.fill(WHITE)

    # 鼠标位置显示信息等
    # if len(pts) == 3:   
    #     bc_u, bc_v, bc_w = cartesian_to_barycentric(*pts, pt)
    #     draw_text(f'pt0 {pts[0]}', color=GREEN, pos=(10, 10))
    #     draw_text(f'pt1 {pts[1]}', color=GREEN, pos=(10, 30))
    #     draw_text(f'pt2 {pts[2]}', color=GREEN, pos=(10, 50))
    #     draw_text(f'pt  {pt}--({bc_u:.2f},{bc_v:.2f},{bc_w:.2f})', color=GREEN, pos=(10, 70))

    prev_button = button

    # Go ahead and update the screen with what we've drawn.
    # This MUST happen after all the other drawing commands.
    pygame.display.update()

pygame.quit()