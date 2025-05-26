
import pygame
import random
import heapq
import math
from collections import deque
import platform
import asyncio

# Initialize Pygame
pygame.init()

# Game constants
CELL_SIZE = 30
GRID_WIDTH = 19
GRID_HEIGHT = 21
WIDTH = CELL_SIZE * GRID_WIDTH
HEIGHT = CELL_SIZE * GRID_HEIGHT
FPS = 5  # Increased for smoother animation

# Colors
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
PINK = (255, 192, 203)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pacman with Pathfinding")
clock = pygame.time.Clock()

# Game map
game_map = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1],
    [1, 3, 1, 1, 2, 1, 1, 1, 2, 1, 2, 1, 1, 1, 2, 1, 1, 3, 1],
    [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
    [1, 2, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1, 2, 1],
    [1, 2, 2, 2, 2, 1, 2, 2, 2, 1, 2, 2, 2, 1, 2, 2, 2, 2, 1],
    [1, 1, 1, 1, 2, 1, 1, 1, 0, 1, 0, 1, 1, 1, 2, 1, 1, 1, 1],
    [0, 0, 0, 1, 2, 1, 0, 0, 0, 0, 0, 0, 0, 1, 2, 1, 0, 0, 0],
    [1, 1, 1, 1, 2, 1, 0, 1, 1, 0, 1, 1, 0, 1, 2, 1, 1, 1, 1],
    [0, 0, 0, 0, 2, 0, 0, 1, 0, 0, 0, 1, 0, 0, 2, 0, 0, 0, 0],
    [1, 1, 1, 1, 2, 1, 0, 1, 1, 1, 1, 1, 0, 1, 2, 1, 1, 1, 1],
    [0, 0, 0, 1, 2, 1, 0, 0, 0, 0, 0, 0, 0, 1, 2, 1, 0, 0, 0],
    [1, 1, 1, 1, 2, 1, 0, 1, 1, 1, 1, 1, 0, 1, 2, 1, 1, 1, 1],
    [1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1],
    [1, 2, 1, 1, 2, 1, 1, 1, 2, 1, 2, 1, 1, 1, 2, 1, 1, 2, 1],
    [1, 3, 2, 1, 2, 2, 2, 2, 2, 0, 2, 2, 2, 2, 2, 1, 2, 3, 1],
    [1, 1, 2, 1, 2, 1, 2, 1, 1, 1, 1, 1, 2, 1, 2, 1, 2, 1, 1],
    [1, 2, 2, 2, 2, 1, 2, 2, 2, 1, 2, 2, 2, 1, 2, 2, 2, 2, 1],
    [1, 2, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 2, 1],
    [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
DIRECTIONS = [UP, DOWN, LEFT, RIGHT]

# Difficulty settings
class Difficulty:
    EASY = {"fps": 10, "ghost_update_freq": 10}
    MEDIUM = {"fps": 15, "ghost_update_freq": 7}
    HARD = {"fps": 20, "ghost_update_freq": 5}

async def difficulty_screen():
    screen.fill(BLACK)
    font = pygame.font.Font(None, 74)
    title = font.render("Select Difficulty", True, YELLOW)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 4))

    font = pygame.font.Font(None, 50)
    options = [
        ("Easy", Difficulty.EASY),
        ("Medium", Difficulty.MEDIUM),
        ("Hard", Difficulty.HARD)
    ]

    selected = 0
    option_rects = []

    for i, (text, _) in enumerate(options):
        rendered = font.render(text, True, WHITE)
        rect = rendered.get_rect(center=(WIDTH // 2, HEIGHT // 2 + i * 60))
        option_rects.append((rect, text))
        screen.blit(rendered, rect)

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    return options[selected][1]
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return None

        # Update the display
        screen.fill(BLACK)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 4))
        for i, (rect, text) in enumerate(option_rects):
            color = YELLOW if i == selected else WHITE
            rendered = font.render(text, True, color)
            screen.blit(rendered, rect)

        pygame.display.flip()
        await asyncio.sleep(0.01)  # Avoid blocking the main thread

class Pacman:
    def __init__(self):
        self.x = 9
        self.y = 15
        self.direction = LEFT
        self.next_direction = LEFT
        self.score = 0
        self.lives = 3
        self.power_mode = False
        self.power_timer = 0
        self.prev_x = self.x  # Track previous position for better collision detection
        self.prev_y = self.y

    def move(self):
        # Store previous position before moving
        self.prev_x, self.prev_y = self.x, self.y

        next_x = self.x + self.next_direction[0]
        next_y = self.y + self.next_direction[1]
        
        if 0 <= next_x < GRID_WIDTH and 0 <= next_y < GRID_HEIGHT and game_map[next_y][next_x] != 1:
            self.direction = self.next_direction
        
        next_x = self.x + self.direction[0]
        next_y = self.y + self.direction[1]
        
        if 0 <= next_x < GRID_WIDTH and 0 <= next_y < GRID_HEIGHT and game_map[next_y][next_x] != 1:
            self.x = next_x
            self.y = next_y
            
            # Collect dots
            if game_map[self.y][self.x] == 2:
                game_map[self.y][self.x] = 0
                self.score += 10
            
            # Collect power pellets
            elif game_map[self.y][self.x] == 3:
                game_map[self.y][self.x] = 0
                self.score += 50
                self.power_mode = True
                self.power_timer = self.fps * 10
        
        if self.power_mode:
            self.power_timer -= 1
            if self.power_timer <= 0:
                self.power_mode = False

    def draw(self):
        # Draw Pacman as a circle with a mouth
        center_x = self.x * CELL_SIZE + CELL_SIZE // 2
        center_y = self.y * CELL_SIZE + CELL_SIZE // 2
        radius = CELL_SIZE // 2 - 2
        
        # Determine mouth angle based on direction
        if self.direction == RIGHT:
            start_angle = 30
            end_angle = 330
        elif self.direction == LEFT:
            start_angle = 150
            end_angle = 390
        elif self.direction == UP:
            start_angle = 240
            end_angle = 480
        else:
            start_angle = 60
            end_angle = 300
        
        pygame.draw.arc(screen, YELLOW, (center_x - radius, center_y - radius, 
                                         radius * 2, radius * 2), 
                        math.radians(start_angle), math.radians(end_angle), radius)
        
        # Draw a line from the center to complete the shape
        end_x = center_x + radius * math.cos(math.radians(start_angle))
        end_y = center_y - radius * math.sin(math.radians(start_angle))
        pygame.draw.line(screen, YELLOW, (center_x, center_y), (end_x, end_y), 1)
        
        end_x = center_x + radius * math.cos(math.radians(end_angle))
        end_y = center_y - radius * math.sin(math.radians(end_angle))
        pygame.draw.line(screen, YELLOW, (center_x, center_y), (end_x, end_y), 1)

class Ghost:
    def __init__(self, x, y, color, algorithm, ghost_update_freq):
        self.x = x
        self.y = y
        self.color = color
        self.algorithm = algorithm
        self.ghost_update_freq = ghost_update_freq
        self.direction = random.choice(DIRECTIONS)
        self.target_x = 0
        self.target_y = 0
        self.scared = False
        self.path = []
        self.update_counter = 0
        self.respawn_timer = 0  # Timer for respawn after being eaten
        self.eaten = False  # Flag to indicate if ghost is eaten
        self.start_x = 9  # Fixed starting position at the center (9, 9)
        self.start_y = 9
        self.prev_x = self.x  # Track previous position for better collision detection
        self.prev_y = self.y

    def set_target(self, pacman):
        if self.scared:
            # Find the farthest possible position from Pacman
            max_distance = -1
            for y in range(GRID_HEIGHT):
                for x in range(GRID_WIDTH):
                    if game_map[y][x] != 1:  # Not a wall
                        distance = abs(pacman.x - x) + abs(pacman.y - y)
                        if distance > max_distance:
                            max_distance = distance
                            self.target_x, self.target_y = x, y
        else:
            self.target_x = pacman.x
            self.target_y = pacman.y

    def move(self, pacman):
        # Store previous position before moving
        self.prev_x, self.prev_y = self.x, self.y

        if self.respawn_timer > 0:
            self.respawn_timer -= 1
            if self.respawn_timer <= 0:
                self.eaten = False
            return

        self.update_counter += 1
        
        if self.update_counter >= self.ghost_update_freq:
            self.update_counter = 0
            self.set_target(pacman)
            
            if self.algorithm == "bfs":
                self.path = self.bfs((self.x, self.y), (self.target_x, self.target_y))
            elif self.algorithm == "dfs":
                self.path = self.dfs((self.x, self.y), (self.target_x, self.target_y))
            elif self.algorithm == "astar":
                self.path = self.astar((self.x, self.y), (self.target_x, self.target_y))
            else:
                self.path = []
        
        if self.path:
            next_pos = self.path.pop(0)
            self.x, self.y = next_pos
        else:
            possible_moves = []
            for dx, dy in DIRECTIONS:
                next_x, next_y = self.x + dx, self.y + dy
                if 0 <= next_x < GRID_WIDTH and 0 <= next_y < GRID_HEIGHT and game_map[next_y][next_x] != 1:
                    possible_moves.append((dx, dy))
            
            if possible_moves:
                self.direction = random.choice(possible_moves)
                self.x += self.direction[0]
                self.y += self.direction[1]

    def bfs(self, start, target):
        queue = deque([(start, [])])
        visited = set([start])
        
        while queue:
            (x, y), path = queue.popleft()
            
            if (x, y) == target:
                return path + [(x, y)]
            
            for dx, dy in DIRECTIONS:
                nx, ny = x + dx, y + dy
                if (0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT and 
                    game_map[ny][nx] != 1 and (nx, ny) not in visited):
                    queue.append(((nx, ny), path + [(x, y)]))
                    visited.add((nx, ny))
        
        return []

    def dfs(self, start, target):
        stack = [(start, [])]
        visited = set([start])
        
        while stack:
            (x, y), path = stack.pop()
            
            if (x, y) == target:
                return path + [(x, y)]
            
            for dx, dy in DIRECTIONS:
                nx, ny = x + dx, y + dy
                if (0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT and 
                    game_map[ny][nx] != 1 and (nx, ny) not in visited):
                    stack.append(((nx, ny), path + [(x, y)]))
                    visited.add((nx, ny))
        
        return []

    def astar(self, start, target):
        def heuristic(a, b):
            return abs(a[0] - b[0]) + abs(a[1] - b[1])
        
        open_set = []
        heapq.heappush(open_set, (0, start))
        came_from = {}
        g_score = {start: 0}
        f_score = {start: heuristic(start, target)}
        open_set_hash = {start}
        
        while open_set:
            current = heapq.heappop(open_set)[1]
            open_set_hash.remove(current)
            
            if current == target:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.reverse()
                return path
            
            for dx, dy in DIRECTIONS:
                neighbor = (current[0] + dx, current[1] + dy)
                if (0 <= neighbor[0] < GRID_WIDTH and 0 <= neighbor[1] < GRID_HEIGHT and 
                    game_map[neighbor[1]][neighbor[0]] != 1):
                    tentative_g_score = g_score[current] + 1
                    if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                        came_from[neighbor] = current
                        g_score[neighbor] = tentative_g_score
                        f_score[neighbor] = tentative_g_score + heuristic(neighbor, target)
                        if neighbor not in open_set_hash:
                            heapq.heappush(open_set, (f_score[neighbor], neighbor))
                            open_set_hash.add(neighbor)
        
        return []

    def draw(self):
        center_x = self.x * CELL_SIZE + CELL_SIZE // 2
        center_y = self.y * CELL_SIZE + CELL_SIZE // 2
        radius = CELL_SIZE // 2 - 2
        
        if self.eaten:
            # Draw as a red circle when eaten
            pygame.draw.circle(screen, RED, (center_x, center_y), radius)
        else:
            color = BLUE if self.scared else self.color
            pygame.draw.circle(screen, color, (center_x, center_y), radius)
            pygame.draw.rect(screen, color, (center_x - radius, center_y, radius * 2, radius))
            wave_height = radius // 3
            for i in range(3):
                offset = i * (radius * 2) // 3
                pygame.draw.rect(screen, color, (center_x - radius + offset, center_y + radius, (radius * 2) // 3, wave_height))
            eye_radius = radius // 3
            eye_offset = radius // 2
            pygame.draw.circle(screen, WHITE, (center_x - eye_offset, center_y - eye_offset // 2), eye_radius)
            pygame.draw.circle(screen, WHITE, (center_x + eye_offset, center_y - eye_offset // 2), eye_radius)
            pupil_radius = eye_radius // 2
            pupil_offset = eye_radius // 2
            dx, dy = self.direction
            pygame.draw.circle(screen, BLACK, (center_x - eye_offset + dx * pupil_offset, center_y - eye_offset // 2 + dy * pupil_offset), pupil_radius)
            pygame.draw.circle(screen, BLACK, (center_x + eye_offset + dx * pupil_offset, center_y - eye_offset // 2 + dy * pupil_offset), pupil_radius)
        # Draw ghost body
        color = BLUE if self.scared else self.color
        
        # Draw the semi-circle for the body
        pygame.draw.circle(screen, color, (center_x, center_y), radius)
        
        # Draw the rectangular bottom part
        pygame.draw.rect(screen, color, 
                        (center_x - radius, center_y, radius * 2, radius))
        
        # Draw the wavy bottom
        wave_height = radius // 3
        for i in range(3):
            offset = i * (radius * 2) // 3
            pygame.draw.rect(screen, color, 
                            (center_x - radius + offset, center_y + radius, 
                             (radius * 2) // 3, wave_height))
        
        # Draw eyes
        eye_radius = radius // 3
        eye_offset = radius // 2
        
        # Left eye
        pygame.draw.circle(screen, WHITE, 
                          (center_x - eye_offset, center_y - eye_offset // 2), 
                          eye_radius)
        
        # Right eye
        pygame.draw.circle(screen, WHITE, 
                          (center_x + eye_offset, center_y - eye_offset // 2), 
                          eye_radius)
        
        # Pupils
        pupil_radius = eye_radius // 2
        pupil_offset = eye_radius // 2
        
        # Direction of pupils based on ghost direction
        dx, dy = self.direction
        
        # Left pupil
        pygame.draw.circle(screen, BLACK, 
                          (center_x - eye_offset + dx * pupil_offset, 
                           center_y - eye_offset // 2 + dy * pupil_offset), 
                          pupil_radius)
        
        # Right pupil
        pygame.draw.circle(screen, BLACK, 
                          (center_x + eye_offset + dx * pupil_offset, 
                           center_y - eye_offset // 2 + dy * pupil_offset), 
                          pupil_radius)

def draw_map():
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if game_map[y][x] == 1:
                pygame.draw.rect(screen, BLUE, rect)
            elif game_map[y][x] == 2:
                pygame.draw.circle(screen, WHITE, (x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 10)
            elif game_map[y][x] == 3:
                pygame.draw.circle(screen, WHITE, (x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 4)

def draw_score(pacman):
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {pacman.score}", True, WHITE)
    lives_text = font.render(f"Lives: {pacman.lives}", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (WIDTH - 120, 10))
    
    if pacman.power_mode:
        power_time = max(0, pacman.power_timer // pacman.fps)  # Convert frames to seconds
        power_text = font.render(f"Power: {power_time}s", True, WHITE)
        screen.blit(power_text, (WIDTH // 2 - power_text.get_width() // 2, 10))

def check_collision(pacman, ghosts):
    for ghost in ghosts:
        # Check if Pacman and ghost are in the same position
        if pacman.x == ghost.x and pacman.y == ghost.y:
            if pacman.power_mode and not ghost.eaten:
                # Ghost is eaten, teleport to starting point immediately
                ghost.eaten = True
                ghost.x = ghost.start_x  # Teleport to (9, 9)
                ghost.y = ghost.start_y
                ghost.respawn_timer = pacman.fps * 2  # 2 seconds respawn time
                pacman.score += 200
            elif not pacman.power_mode and not ghost.eaten:
                # Pacman loses a life
                pacman.lives -= 1
                if pacman.lives > 0:
                    pacman.x, pacman.y = 9, 15
                    for g in ghosts:
                        if not g.eaten:
                            g.x, g.y = 9, 9
                return True
        # Additional check for crossing paths (Pacman and ghost swap positions)
        elif (pacman.x == ghost.prev_x and pacman.y == ghost.prev_y and
              pacman.prev_x == ghost.x and pacman.prev_y == ghost.y):
            if pacman.power_mode and not ghost.eaten:
                # Ghost is eaten, teleport to starting point immediately
                ghost.eaten = True
                ghost.x = ghost.start_x  # Teleport to (9, 9)
                ghost.y = ghost.start_y
                ghost.respawn_timer = pacman.fps * 2  # 2 seconds respawn time
                pacman.score += 200
            elif not pacman.power_mode and not ghost.eaten:
                # Pacman loses a life
                pacman.lives -= 1
                if pacman.lives > 0:
                    pacman.x, pacman.y = 9, 15
                    for g in ghosts:
                        if not g.eaten:
                            g.x, g.y = 9, 9
                return True
    return False

def check_win():
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if game_map[y][x] in [2, 3]:
                return False
    return True

def game_over_screen():
    screen.fill(BLACK)
    font = pygame.font.Font(None, 74)
    text = font.render("GAME OVER!", True, RED)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
    pygame.display.flip()
    pygame.time.wait(3000)

def win_screen():
    screen.fill(BLACK)
    font = pygame.font.Font(None, 74)
    text = font.render("YOU WIN!", True, YELLOW)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
    pygame.display.flip()
    pygame.time.wait(3000)

async def start_screen():
    screen.fill(BLACK)
    font = pygame.font.Font(None, 74)
    title = font.render("PACMAN", True, YELLOW)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 4))
    
    font = pygame.font.Font(None, 36)
    instructions = [
        "Use arrow keys to move",
        "Eat all dots to win",
        "Avoid ghosts unless powered up",
        "Press SPACE to start"
    ]
    
    for i, line in enumerate(instructions):
        text = font.render(line, True, WHITE)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 + i * 40))
    
    pygame.display.flip()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return True
        await asyncio.sleep(0.01)

async def main():
    difficulty = await difficulty_screen()
    if not difficulty:
        return
    
    pacman = Pacman()
    pacman.fps = difficulty["fps"]
    ghosts = [
        Ghost(9, 9, RED, "astar", difficulty["ghost_update_freq"]),
        Ghost(8, 9, PINK, "bfs", difficulty["ghost_update_freq"]),
        Ghost(10, 9, CYAN, "dfs", difficulty["ghost_update_freq"]),
        Ghost(9, 8, ORANGE, "random", difficulty["ghost_update_freq"])
    ]
    
    if not await start_screen():
        return
    
    running = True
    game_over = False
    win = False
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    pacman.next_direction = UP
                elif event.key == pygame.K_DOWN:
                    pacman.next_direction = DOWN
                elif event.key == pygame.K_LEFT:
                    pacman.next_direction = LEFT
                elif event.key == pygame.K_RIGHT:
                    pacman.next_direction = RIGHT
        
        if not game_over and not win:
            screen.fill(BLACK)
            pacman.move()
            for ghost in ghosts:
                ghost.scared = pacman.power_mode
                ghost.move(pacman)
            
            if check_collision(pacman, ghosts):
                if pacman.lives <= 0:
                    game_over = True
            
            if check_win():
                win = True
            
            draw_map()
            pacman.draw()
            for ghost in ghosts:
                ghost.draw()
            draw_score(pacman)
            pygame.display.flip()
            clock.tick(difficulty["fps"])
            await asyncio.sleep(1.0 / difficulty["fps"])
        elif game_over:
            game_over_screen()
            running = False
        elif win:
            win_screen()
            running = False
    
    pygame.quit()

if platform.system() == "Emscripten":
    asyncio.run_coroutine_threadsafe(main(), asyncio.get_event_loop())
else:
    if __name__ == "__main__":
        asyncio.run(main())
