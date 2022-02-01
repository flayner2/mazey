import pygame
import sys
from random import choice
from dataclasses import dataclass


W_WIDTH, W_HEIGHT = 600, 600
SIZE = 20
STROKE = 1
ROW_SIZE = int(W_WIDTH / SIZE)
FPS = 60

stack: list["Cell"] = []


@dataclass(frozen=True)
class Color:
    WHITE: tuple = 255, 255, 255
    BLACK: tuple = 0, 0, 0
    BLUE: tuple = 0, 0, 255
    GREEN: tuple = 0, 255, 0
    RED: tuple = 255, 0, 0
    LIGHT_PURPLE: tuple = 177, 156, 217
    DARK_PURPLE: tuple = 85, 9, 140


class Cell:
    def __init__(
        self,
        x: float,
        y: float,
        w: float = SIZE,
        h: float = SIZE,
        walls: list = None,
        visited: bool = False,
        selected: bool = False,
    ) -> None:
        self.x = x
        self.y = y
        self.w = w
        self.h = h

        if walls:
            self.walls = walls
        else:
            self.walls = [True] * 4

        self.visited = visited
        self.selected = selected

    def __repr__(self) -> str:
        return f"Cell({self.x}, {self.y}, visited={self.visited}, selected={self.selected})"

    def highlight(self, surface: pygame.surface.Surface, color: tuple) -> None:
        pygame.draw.rect(surface, color, pygame.Rect(self.x, self.y, self.w, self.h))

    def render(self, surface: pygame.surface.Surface) -> None:
        if self.visited and not self.selected:
            self.highlight(surface, Color.DARK_PURPLE)

        if self.walls[0]:
            pygame.draw.line(
                surface,
                Color.WHITE,
                (self.x, self.y),
                (self.x + self.w, self.y),
                STROKE,
            )
        if self.walls[1]:
            pygame.draw.line(
                surface,
                Color.WHITE,
                (self.x + self.w, self.y),
                (self.x + self.w, self.y + self.h),
                STROKE,
            )
        if self.walls[2]:
            pygame.draw.line(
                surface,
                Color.WHITE,
                (self.x, self.y + self.h),
                (self.x + self.w, self.y + self.h),
                STROKE,
            )
        if self.walls[3]:
            pygame.draw.line(
                surface,
                Color.WHITE,
                (self.x, self.y),
                (self.x, self.y + self.h),
                STROKE,
            )

    def get_neighbors(self, grid: list["Cell"]) -> list["Cell"]:
        last = len(grid) - 1
        position = grid.index(self)

        if position < ROW_SIZE:
            bottom = position + ROW_SIZE

            if position == 0:
                return [grid[1], grid[bottom]]
            elif position == ROW_SIZE - 1:
                return [grid[position - 1], grid[bottom]]
            else:
                return [grid[position - 1], grid[position + 1], grid[bottom]]
        elif position > last - ROW_SIZE:
            top = position - ROW_SIZE

            if position == last:
                return [grid[last - 1], grid[top]]
            elif position == last - ROW_SIZE + 1:
                return [grid[position + 1], grid[top]]
            else:
                return [grid[position - 1], grid[position + 1], grid[top]]
        elif position % ROW_SIZE == 0:
            bottom = position + ROW_SIZE
            top = position - ROW_SIZE
            right = position + 1

            return [grid[top], grid[bottom], grid[right]]
        elif (position + 1) % ROW_SIZE == 0:
            bottom = position + ROW_SIZE
            top = position - ROW_SIZE
            left = position - 1

            return [grid[top], grid[bottom], grid[left]]
        else:
            bottom = position + ROW_SIZE
            top = position - ROW_SIZE
            left = position - 1
            right = position + 1

            return [grid[top], grid[bottom], grid[left], grid[right]]

    def set_selected(self) -> None:
        self.selected = True

    def set_deselected(self) -> None:
        self.selected = False

    def get_selected(self) -> bool:
        return self.selected

    def set_visited(self) -> None:
        self.visited = True

    def set_devisited(self) -> None:
        self.visited = False

    def get_visited(self) -> bool:
        return self.visited

    def remove_wall(self, side: str) -> None:
        match side:
            case "top":
                self.walls[0] = False
                return
            case "right":
                self.walls[1] = False
                return
            case "bottom":
                self.walls[2] = False
                return
            case "left":
                self.walls[3] = False
                return
            case _:
                raise ValueError("Invalid side. Try 'top', 'right', 'bottom' or 'left'.")

    def remove_walls_between(self, other: "Cell") -> None:
        x_pos = self.x - other.x
        y_pos = self.y - other.y

        if x_pos > 0:
            self.remove_wall("left")
            other.remove_wall("right")
        elif x_pos < 0:
            self.remove_wall("right")
            other.remove_wall("left")

        if y_pos > 0:
            self.remove_wall("top")
            other.remove_wall("bottom")
        elif y_pos < 0:
            self.remove_wall("bottom")
            other.remove_wall("top")


def create_grid() -> list[Cell]:
    return [
        Cell(i, j)
        for j in range(0, W_WIDTH, int(SIZE))
        for i in range(0, W_HEIGHT, int(SIZE))
    ]


def display_grid(grid: list[Cell], surface: pygame.surface.Surface) -> None:
    for cell in grid:
        cell.render(surface)


def _any_unvisited(neighbors: list[Cell]) -> bool:
    for neighbor in neighbors:
        if not neighbor.get_visited():
            return True

    return False


def travel(grid: list[Cell], surface) -> None:
    current_cell = stack.pop()
    current_cell.set_selected()
    current_cell.set_visited()
    
    current_cell.highlight(surface, Color.BLUE)
    current_cell.render(surface)

    neighbors = current_cell.get_neighbors(grid)

    if neighbors and _any_unvisited(neighbors):
        stack.append(current_cell)

        unvisited_neighbors = [
            neighbor for neighbor in neighbors if not neighbor.get_visited()
        ]

        next_neighbor = choice(unvisited_neighbors)
        current_cell.remove_walls_between(next_neighbor)
        stack.append(next_neighbor)

    current_cell.set_deselected()



def main() -> None:
    pygame.init()

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((W_WIDTH, W_HEIGHT))

    grid = create_grid()

    current_cell = grid[0]
    current_cell.set_visited()
    current_cell.set_selected()
    current_cell.highlight(screen, Color.BLUE)

    stack.append(current_cell)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
       
        clock.tick(FPS)
        
        screen.fill(Color.BLACK)

        display_grid(grid, screen)
    
        if stack:
            travel(grid, screen)
        else:
            end_cell = grid[len(grid) - 1]
            end_cell.highlight(screen, Color.RED)
            grid[0].highlight(screen, Color.GREEN)
       
        pygame.display.update()


if __name__ == "__main__":
    main()
