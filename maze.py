import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
CELL_SIZE = 20
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Solver with Levels")


class Cell:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.walls = {"top": True, "right": True, "bottom": True, "left": True}
        self.visited = False

    def draw(self, cell_size):
        x, y = self.x * cell_size, self.y * cell_size
        if self.visited:
            pygame.draw.rect(screen, WHITE, (x, y, cell_size, cell_size))
        if self.walls["top"]:
            pygame.draw.line(screen, BLACK, (x, y), (x + cell_size, y))
        if self.walls["right"]:
            pygame.draw.line(screen, BLACK, (x + cell_size, y),
                             (x + cell_size, y + cell_size))
        if self.walls["bottom"]:
            pygame.draw.line(screen, BLACK, (x, y + cell_size),
                             (x + cell_size, y + cell_size))
        if self.walls["left"]:
            pygame.draw.line(screen, BLACK, (x, y), (x, y + cell_size))


def create_maze(width, height):
    grid = [[Cell(x, y) for y in range(height)] for x in range(width)]
    stack = [(0, 0)]
    grid[0][0].visited = True

    while stack:
        current_x, current_y = stack[-1]
        neighbors = []
        directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]
        for dx, dy in directions:
            nx, ny = current_x + dx, current_y + dy
            if 0 <= nx < width and 0 <= ny < height and not grid[nx][
                    ny].visited:
                neighbors.append((nx, ny))

        if neighbors:
            next_x, next_y = random.choice(neighbors)
            if next_x == current_x + 1:
                grid[current_x][current_y].walls["right"] = False
                grid[next_x][next_y].walls["left"] = False
            elif next_x == current_x - 1:
                grid[current_x][current_y].walls["left"] = False
                grid[next_x][next_y].walls["right"] = False
            elif next_y == current_y + 1:
                grid[current_x][current_y].walls["bottom"] = False
                grid[next_x][next_y].walls["top"] = False
            elif next_y == current_y - 1:
                grid[current_x][current_y].walls["top"] = False
                grid[next_x][next_y].walls["bottom"] = False
            grid[next_x][next_y].visited = True
            stack.append((next_x, next_y))
        else:
            stack.pop()

    for row in grid:
        for cell in row:
            cell.visited = False

    return grid


def draw_maze(grid, player_pos, end_pos, cell_size):
    screen.fill(WHITE)
    for row in grid:
        for cell in row:
            cell.draw(cell_size)

    # Draw player
    pygame.draw.circle(screen, RED,
                       (player_pos[0] * cell_size + cell_size // 2,
                        player_pos[1] * cell_size + cell_size // 2),
                       cell_size // 3)

    # Draw end point
    pygame.draw.rect(
        screen, GREEN,
        (end_pos[0] * cell_size, end_pos[1] * cell_size, cell_size, cell_size))

    pygame.display.flip()


def move_player(grid, player_pos, dx, dy):
    new_x, new_y = player_pos[0] + dx, player_pos[1] + dy
    if 0 <= new_x < len(grid) and 0 <= new_y < len(grid[0]):
        current_cell = grid[player_pos[0]][player_pos[1]]
        if (dx == 1 and not current_cell.walls["right"]) or \
           (dx == -1 and not current_cell.walls["left"]) or \
           (dy == 1 and not current_cell.walls["bottom"]) or \
           (dy == -1 and not current_cell.walls["top"]):
            return (new_x, new_y)
    return player_pos


def solve_maze(grid, start, end):
    stack = [start]
    visited = set()
    parent = {}

    while stack:
        current = stack.pop()
        if current == end:
            path = []
            while current != start:
                path.append(current)
                current = parent[current]
            path.append(start)
            return path[::-1]

        if current in visited:
            continue

        visited.add(current)

        x, y = current
        neighbors = []
        if not grid[x][y].walls["right"] and x + 1 < len(grid):
            neighbors.append((x + 1, y))
        if not grid[x][y].walls["left"] and x - 1 >= 0:
            neighbors.append((x - 1, y))
        if not grid[x][y].walls["bottom"] and y + 1 < len(grid[0]):
            neighbors.append((x, y + 1))
        if not grid[x][y].walls["top"] and y - 1 >= 0:
            neighbors.append((x, y - 1))

        for neighbor in neighbors:
            if neighbor not in visited:
                stack.append(neighbor)
                parent[neighbor] = current

    return None  # No path found


def main():
    levels = [
        {
            "width": 10,
            "height": 10,
            "cell_size": 40
        },
        {
            "width": 15,
            "height": 15,
            "cell_size": 30
        },
        {
            "width": 20,
            "height": 20,
            "cell_size": 25
        },
        {
            "width": 25,
            "height": 25,
            "cell_size": 20
        },
        {
            "width": 30,
            "height": 30,
            "cell_size": 18
        },
    ]

    current_level = 0
    clock = pygame.time.Clock()

    while current_level < len(levels):
        level = levels[current_level]
        grid = create_maze(level["width"], level["height"])
        player_pos = (0, 0)
        end_pos = (level["width"] - 1, level["height"] - 1)
        solving = False
        solution = None
        solution_index = 0

        font = pygame.font.Font(None, 36)
        level_text = font.render(f"Level {current_level + 1}", True, BLUE)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        player_pos = move_player(grid, player_pos, 0, -1)
                    elif event.key == pygame.K_DOWN:
                        player_pos = move_player(grid, player_pos, 0, 1)
                    elif event.key == pygame.K_LEFT:
                        player_pos = move_player(grid, player_pos, -1, 0)
                    elif event.key == pygame.K_RIGHT:
                        player_pos = move_player(grid, player_pos, 1, 0)
                    elif event.key == pygame.K_SPACE:
                        solving = True
                        solution = solve_maze(grid, (0, 0), end_pos)
                        solution_index = 0

            if solving and solution:
                if solution_index < len(solution):
                    player_pos = solution[solution_index]
                    solution_index += 1
                    time.sleep(0.1)  # Slow down the automatic solving
                else:
                    solving = False

            draw_maze(grid, player_pos, end_pos, level["cell_size"])
            screen.blit(level_text, (10, 10))
            pygame.display.flip()

            if player_pos == end_pos:
                font = pygame.font.Font(None, 48)
                if current_level == len(levels) - 1:
                    text = font.render(
                        "Congratulations! You completed all levels!", True,
                        BLUE)
                else:
                    text = font.render("Level Complete!", True, BLUE)
                screen.blit(text, (WIDTH // 2 - text.get_width() // 2,
                                   HEIGHT // 2 - text.get_height() // 2))
                pygame.display.flip()
                time.sleep(2)
                current_level += 1
                running = False

            clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
