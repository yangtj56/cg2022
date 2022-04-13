"""
Modified on Feb 20 2020
@author: lbg@dongseo.ac.kr
"""

import itertools
from typing import List, Tuple

import numpy as np
import pygame

width = 800
height = 600

pygame.init()
screen = pygame.display.set_mode((width, height), 0, 32)
font = pygame.font.SysFont("consolas", 20)

pygame.display.set_caption("ImagePolylineMouseButton-Lagrange Interpolation")

# Define the colors we will use in RGB format
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)


class MOUSE_BUTTON:
    LEFT = 1
    MIDDLE = 2
    RIGHT = 3


class RectManager:
    rectangles: List[pygame.rect.Rect]
    rect_dragging: int
    drag_offset: Tuple[int, int]
    indexing: int

    def __init__(self):
        self.rectangles = []
        self.rect_dragging = -1
        self.drag_offset = (0, 0)
        self.indexing = -1


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
    screen.blit(text_surface, text_rect)


def draw_lagrange_polylines(points, color=BLUE, steps=10, thick=3):
    ox, oy = points[0]

    for k in range((len(points) - 1) * steps + 1):
        t = k / steps
        x = y = 0
        for i in range(len(points)):
            x += lagrange_polylines(points, i, t) * points[i][0]
            y += lagrange_polylines(points, i, t) * points[i][1]
        pygame.draw.line(screen, color, (ox, oy), (x, y), thick)
        ox, oy = x, y


def lagrange_polylines(points, i, t):
    l = 1
    li = [x for x in range(len(points)) if x != i]
    for j in li:
        l *= (t - j) / (i - j)
    return l


def cartesian_to_barycentric(pt1, pt2, pt3, pt):
    basis = np.array([pt1, pt2, pt3]).T
    basis_square = np.pad(basis, ((1, 0), (0, 0)), 'constant', constant_values=1)

    cartesian = np.array([1, *pt])

    barycentric_coords = np.linalg.inv(basis_square) @ cartesian
    return barycentric_coords


# Loop until the user clicks the close button.
margin = 6

rm = RectManager()


def is_clicked(curr_btn, prev_btn, btn_idx: int):
    return curr_btn[btn_idx] and not prev_btn[btn_idx]


def main():
    done = False

    def handle_left_mouse_down(event):
        for idx, rect in enumerate(rm.rectangles):
            if rect.collidepoint(event.pos):
                rm.rect_dragging = idx
                rm.drag_offset = (rect.x - event.pos[0], rect.y - event.pos[1])
                break
        else:
            rm.rectangles.append(
                pygame.rect.Rect((event.pos[0] - margin, event.pos[1] - margin, 2 * margin, 2 * margin)))

    def handle_left_mouse_up(event):
        rm.rect_dragging = -1

    def handle_right_mouse_down(event):
        rm.rectangles.clear()

    def handle_mouse_motion(event):
        for idx, rect in enumerate(rm.rectangles):
            if rect.collidepoint(event.pos):
                rm.indexing = idx
                break
        else:
            rm.indexing = -1

        if rm.rect_dragging >= 0:
            rm.rectangles[rm.rect_dragging].x = event.pos[0] + rm.drag_offset[0]
            rm.rectangles[rm.rect_dragging].y = event.pos[1] + rm.drag_offset[1]

    while not done:
        # This limits the while loop to a max of 10 times per second.
        # Leave this out and we will use all CPU we can.
        time_passed = clock.tick(30)

        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == MOUSE_BUTTON.LEFT:
                    handle_left_mouse_down(event)

                if event.button == MOUSE_BUTTON.RIGHT:
                    handle_right_mouse_down(event)

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == MOUSE_BUTTON.LEFT:
                    handle_left_mouse_up(event)

            elif event.type == pygame.MOUSEMOTION:
                handle_mouse_motion(event)

        mouse_x, mouse_y = pygame.mouse.get_pos()

        for i, rect in enumerate(rm.rectangles):
            pygame.draw.rect(
                screen, RED if i == rm.rect_dragging else BLUE, rect, 2
            )
            if i > 0:
                pygame.draw.line(screen, GREEN, rm.rectangles[i - 1].center, rm.rectangles[i].center, 2)

        # 鼠标位置显示信息等
        # pygame.draw.rect(screen, (170, 170, 170), (0, 0, 300, 75))
        # draw_text(f'LagrangePolynomials : {len(rm.rectangles)}', GREEN, (10, 10))
        # draw_text(f'mouse x:{mouse_x} y:{mouse_y}', GREEN, (10, 30))
        # draw_text(f'FPS :{clock.get_fps():.2f} index :{rm.indexing}', GREEN, (10, 50))

        if len(rm.rectangles) > 1:
            draw_lagrange_polylines([rect.center for rect in rm.rectangles])

        # Go ahead and update the screen with what we've drawn.
        # This MUST happen after all the other drawing commands.
        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    main()