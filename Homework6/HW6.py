"""
Modified on Feb 20 2020
@author: lbg@dongseo.ac.kr
"""

import functools
import itertools
import time
from typing import List, Tuple, Optional, Any, Iterable

import numpy as np
import pygame

width = 800
height = 600

pygame.init()
screen = pygame.display.set_mode((width, height), 0, 32)
font = pygame.font.SysFont("consolas", 20)

pygame.display.set_caption("ImagePolylineMouseButton-Hermite")

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

    def get_colide_rect(self, pos: Tuple[int, int]) -> Tuple[int, Optional[pygame.rect.Rect]]:
        for idx, rect in enumerate(self.rectangles):
            if rect.collidepoint(pos):
                return idx, rect
        else:
            return -1, None


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

@functools.lru_cache()
def get_cubic_bezier_matrix(steps):
    
    M = np.array([[-1, 3, -3, 1],
                  [3, -6, 3, 0],
                  [-3, 3, 0, 0],
                  [1, 0, 0, 0]])

    t = np.arange(0, 1, 1 / steps)
    t_arr = np.array([t ** (3 - i) for i in range(4)])

    return t_arr.T @ M


def draw_cubic_bezier_vectorize(points, color=BLUE, steps=100):
    
    A = np.array(points)
    M = get_cubic_bezier_matrix(steps)

    XY = M @ A

    pygame.draw.lines(screen, color, False, XY)


def draw_cubic_bezier(points, color=BLUE, steps=100, thick=3):
    """
    Draw Cubic Bezier Curve
    """
    A = np.array(points)
    pt0, pt1, pt2, pt3 = points

    ox, oy = pt0

    for t in np.arange(0, 1, 1 / steps):
        x = (pt0[0] * (1 - t) ** 3) + (pt1[0] * 3 * t * (1 - t) ** 2) + (pt2[0] * 3 * t ** 2 * (1 - t)) + (
                pt3[0] * t ** 3)
        y = (pt0[1] * (1 - t) ** 3) + (pt1[1] * 3 * t * (1 - t) ** 2) + (pt2[1] * 3 * t ** 2 * (1 - t)) + (
                pt3[1] * t ** 3)

        pygame.draw.line(screen, color, (ox, oy), (x, y), thick)
        ox, oy = x, y


@functools.lru_cache()
def calc_next_coefficients(values: Tuple[int]) -> Tuple[int]:
    result = [1]
    for i in range(len(values) - 1):
        result += [values[i] + values[i + 1]]
    result += [1]
    return tuple(result)


@functools.lru_cache()
def calc_coefficients(degree: int) -> Tuple[int]:
    if degree == 0: return (1,)

    result = calc_next_coefficients(calc_coefficients(degree - 1))
    return result


@functools.lru_cache()
def bezier_polylines(points: Iterable[Tuple[int, int]], steps: int) -> List[Tuple[int, int]]:
    result = []

    point_cnt = len(points)

    for t in np.arange(0, 1, 1 / steps):
        x, y = 0, 0

        for i, coef in zip(range(point_cnt), calc_coefficients(point_cnt - 1)):
            x += points[i][0] * coef * (t ** i) * (1 - t) ** (point_cnt - 1 - i)
            y += points[i][1] * coef * (t ** i) * (1 - t) ** (point_cnt - 1 - i)

        result += [(x, y)]

    return result


def draw_generalize_bezier_v2(points, color=BLUE, steps=100, thick=3):
    

    ox, oy = points[0]

    for x, y in bezier_polylines(points, steps):
        pygame.draw.line(screen, color, (ox, oy), (x, y), thick)
        ox, oy = x, y


def draw_generalize_bezier(points, color=BLUE, steps=100, thick=3):
   

    point_cnt = len(points)

    ox, oy = points[0]

    for t in np.arange(0, 1, 1 / steps):
        x, y = 0, 0

        for i, coef in zip(range(point_cnt), calc_coefficients(point_cnt - 1)):
            x += points[i][0] * coef * (t ** i) * (1 - t) ** (point_cnt - 1 - i)
            y += points[i][1] * coef * (t ** i) * (1 - t) ** (point_cnt - 1 - i)

        pygame.draw.line(screen, color, (ox, oy), (x, y), thick)
        ox, oy = x, y


def time_it(fn, *args, **kwargs) -> Tuple[float, Optional[Any]]:
    start = time.time()
    result = fn(*args, **kwargs)
    end = time.time()

    return (end - start) * 1000, result

# HW 6 

def calc_hermite_coefficient(pt0, pt1, slope):
   
    x0, y0 = pt0
    x1, y1 = pt1
    s0, s1 = slope

    X = np.array([[x0 ** 3, x0 ** 2, x0, 1],
                  [x1 ** 3, x1 ** 2, x1, 1],
                  [3 * x0 ** 2, 2 * x0, 1, 0],
                  [3 * x1 ** 2, 2 * x1, 1, 0]])

    Y = np.array([[y0],
                  [y1],
                  [s0],
                  [s1]])

    A = np.linalg.inv(X) @ Y
    return A


def draw_cubic_hermite_curve(points, color=BLUE, steps=100, thick=3):
   
    mat_points = np.array(points)

    dx, dy = np.diff(mat_points, axis=0).T

    slope = dy / dx
    slope = np.concatenate(([0], slope))

    for i in range(len(points) - 1):
        pt0, pt1 = points[i:i + 2]
        x0, y0 = pt0
        x1, y1 = pt1

        A = calc_hermite_coefficient(pt0, pt1, slope[i:i + 2])

        X = np.arange(x0, x1, (x1 - x0) / steps)

        X_polynomial = np.array([(x ** 3, x ** 2, x, 1) for x in X])

        Y = X_polynomial @ A

        ox, oy = pt0

        for x, y in zip(X, Y):
            pygame.draw.line(screen, color, (ox, oy), (x, y), thick)
            ox, oy = x, y


# HW 6 


# Loop until the user clicks the close button.

def main():
    done = False
    margin = 6
    rm = RectManager()

    def handle_left_mouse_down(event):
        idx, rect = rm.get_colide_rect(event.pos)

        if idx > -1:
            rm.rect_dragging = idx
            rm.drag_offset = (rect.x - event.pos[0], rect.y - event.pos[1])

        else:
            # if len(rm.rectangles) >= 4: return

            rm.rectangles.append(
                pygame.rect.Rect((event.pos[0] - margin, event.pos[1] - margin, 2 * margin, 2 * margin)))

    def handle_left_mouse_up(event):
        rm.rect_dragging = -1

    def handle_right_mouse_down(event):
        rm.rectangles.clear()

    def handle_mouse_motion(event):
        idx, _ = rm.get_colide_rect(event.pos)
        rm.indexing = idx

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

        

        if len(rm.rectangles) >= 2:
            # calc_time, _ = time_it(draw_cubic_bezier, tuple(rect.center for rect in rm.rectangles), steps=500)
            # calc_time, _ = time_it(draw_cubic_bezier_vectorize, tuple(rect.center for rect in rm.rectangles), steps=500)
            calc_time, _ = time_it(draw_cubic_hermite_curve, tuple(rect.center for rect in rm.rectangles), steps=100)
            # draw_text(f'draw_time :{calc_time:.2f} ms', RED, (10, 70))

        # Go ahead and update the screen with what we've drawn.
        # This MUST happen after all the other drawing commands.
        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    main()