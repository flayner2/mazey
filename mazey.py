import pygame as pg
import sys
from dataclasses import dataclass


W_WIDTH, W_HEIGHT = 600, 600
SIZE = 20
STROKE = 1


@dataclass(frozen=True)
class Color:
    white: tuple = 255, 255, 255
    black: tuple = 0, 0, 0
    blue: tuple = 0, 0, 255
    green: tuple = 0, 255, 0


class Cell:
    def __init__(
        self,
        x: float,
        y: float,
        w: float = SIZE,
        h: float = SIZE,
        walls: list = [True, True, True, True],
        visited: bool = False,
    ) -> None:
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.walls = walls
        self.visited = visited

    def render(self, surface: pg.surface.Surface) -> None:
        if self.walls[0]:
            pg.draw.line(
                surface,
                Color.white,
                (self.x, self.y),
                (self.x + self.w, self.y),
                STROKE,
            )
        if self.walls[1]:
            pg.draw.line(
                surface,
                Color.white,
                (self.x + self.w, self.y),
                (self.x + self.w, self.y + self.h),
                STROKE,
            )
        if self.walls[2]:
            pg.draw.line(
                surface,
                Color.white,
                (self.x, self.y + self.h),
                (self.x + self.w, self.y + self.h),
                STROKE,
            )
        if self.walls[3]:
            pg.draw.line(
                surface,
                Color.white,
                (self.x, self.y),
                (self.x, self.y + self.h),
                STROKE,
            )


def create_grid() -> list[Cell]:
    return [
        Cell(i, j)
        for i in range(0, W_WIDTH, int(SIZE))
        for j in range(0, W_HEIGHT, int(SIZE))
    ]


def display_grid(grid: list[Cell], surface: pg.surface.Surface) -> None:
    for cell in grid:
        cell.render(surface)


def main() -> None:
    pg.init()

    screen = pg.display.set_mode((W_WIDTH, W_HEIGHT))

    grid = create_grid()

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

        screen.fill(Color.black)
        display_grid(grid, screen)
        pg.display.update()


if __name__ == "__main__":
    main()
