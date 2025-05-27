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
BLUE = (65, 105, 225)     # Royal Blue - main wall color
WHITE = (255, 255, 255)
YELLOW = (255, 223, 0)    # Gold - for Pacman
RED = (220, 20, 60)       # Crimson - for ghost
PINK = (255, 105, 180)    # Hot Pink - for ghost
CYAN = (0, 191, 255)      # Deep Sky Blue - for ghost
ORANGE = (255, 140, 0)    # Dark Orange - for ghost
PURPLE = (147, 112, 219)  # Medium Purple - for power pellets
PASTEL_BLUE = (135, 206, 235)  # Sky Blue - for background
PASTEL_GREEN = (144, 238, 144) # Light Green - for dots
PASTEL_YELLOW = (255, 250, 205) # Lemon Chiffon - for menu
WALL_DECOR = (135, 206, 235)   # Sky Blue - elegant wall decorations
GOLD = (218, 165, 32)    # Golden Rod - for special effects
SILVER = (192, 192, 192) # Silver - for metallic effects
PEARL = (240, 234, 214)  # Pearl - for elegant highlights

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
        self.fps = 10  # Thêm thuộc tính fps mặc định
        self.prev_x = self.x
        self.prev_y = self.y
        self.path = []  # Path for autoplay

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

    def evaluate_danger(self, ghosts):
        """Heuristic to evaluate danger from ghosts"""
        total_danger = 0
        for ghost in ghosts:
            if not ghost.eaten and not self.power_mode:  # Only consider active ghosts when not in power mode
                distance = abs(self.x - ghost.x) + abs(self.y - ghost.y)
                if distance < 3:  # Consider ghosts within 3 cells as highly dangerous
                    total_danger += (3 - distance) * 2  # Higher penalty for closer ghosts
        return total_danger

    def find_nearest_food(self):
        """Find the nearest dot or power pellet using A*"""
        min_distance = float('inf')
        nearest_food = None
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                if game_map[y][x] in [2, 3]:  # Dot or power pellet
                    path = self.astar((self.x, self.y), (x, y))
                    if path and len(path) < min_distance:
                        min_distance = len(path)
                        nearest_food = (x, y)
        return nearest_food

    def find_nearest_ghost(self, ghosts):
        """Find the nearest ghost using A*"""
        min_distance = float('inf')
        nearest_ghost_pos = None
        for ghost in ghosts:
            if not ghost.eaten:  # Only chase active ghosts
                path = self.astar((self.x, self.y), (ghost.x, ghost.y))
                if path and len(path) < min_distance:
                    min_distance = len(path)
                    nearest_ghost_pos = (ghost.x, ghost.y)
        return nearest_ghost_pos

    def choose_safe_direction(self, ghosts):
        """Choose a direction that minimizes danger from ghosts"""
        best_direction = self.direction
        min_danger = float('inf')
        for dx, dy in DIRECTIONS:
            next_x, next_y = self.x + dx, self.y + dy
            if 0 <= next_x < GRID_WIDTH and 0 <= next_y < GRID_HEIGHT and game_map[next_y][next_x] != 1:
                # Temporarily move to evaluate danger
                temp_x, temp_y = self.x, self.y
                self.x, self.y = next_x, next_y
                danger = self.evaluate_danger(ghosts)
                self.x, self.y = temp_x, temp_y  # Revert position
                if danger < min_danger:
                    min_danger = danger
                    best_direction = (dx, dy)
        return best_direction

    def autoplay_move(self, ghosts):
        """Logic for autoplay: prioritize eating food to win, chase ghosts only when safe or necessary"""
        # Check if there is any food left
        has_food = any(2 in row or 3 in row for row in game_map)
        
        # Evaluate danger level
        danger = self.evaluate_danger(ghosts)
        
        if has_food:
            # Prioritize eating food unless danger is too high
            if danger > 4:  # High danger threshold to trigger avoidance
                self.next_direction = self.choose_safe_direction(ghosts)
                self.path = []  # Clear path to prioritize avoiding
            else:
                target = self.find_nearest_food()
                if target:
                    self.path = self.astar((self.x, self.y), target)
                    if self.path:
                        next_pos = self.path[0]
                        dx = next_pos[0] - self.x
                        dy = next_pos[1] - self.y
                        self.next_direction = (dx, dy)
                        self.path.pop(0)
                    else:
                        self.next_direction = self.choose_safe_direction(ghosts)
        else:
            # No food left, prioritize chasing ghosts if in power mode or if safe
            if self.power_mode or danger == 0:
                target = self.find_nearest_ghost(ghosts)
                if target:
                    self.path = self.astar((self.x, self.y), target)
                    if self.path:
                        next_pos = self.path[0]
                        dx = next_pos[0] - self.x
                        dy = next_pos[1] - self.y
                        self.next_direction = (dx, dy)
                        self.path.pop(0)
                    else:
                        self.next_direction = self.choose_safe_direction(ghosts)
            else:
                # Avoid ghosts if not in power mode and no food left
                self.next_direction = self.choose_safe_direction(ghosts)

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
        self.eaten = False  # Flag to indicate if ghost is eaten
        self.start_x = 9  # Fixed starting position at the center (9, 9)
        self.start_y = 9
        self.prev_x = self.x  # Track previous position for better collision detection
        self.prev_y = self.y
        self.has_corpse = False  # Flag to indicate if ghost has a corpse
        self.respawn_timer = 0  # Timer for respawn
        self.glow_timer = 0  # Timer for glow effect

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

        # Update glow timer
        if self.has_corpse:
            self.glow_timer += 1

        # Update respawn logic
        if self.eaten:
            self.respawn_timer += 1
            if self.respawn_timer >= pacman.fps * 3:  # Respawn after 3 seconds
                self.eaten = False
                self.has_corpse = False
                self.respawn_timer = 0
                self.glow_timer = 0
            return  # Don't move while eaten

        # Only move if ghost is not eaten
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
        # Only draw ghost if it's not eaten
        if not self.eaten:
            center_x = self.x * CELL_SIZE + CELL_SIZE // 2
            center_y = self.y * CELL_SIZE + CELL_SIZE // 2
            radius = CELL_SIZE // 2 - 2
            
            if self.scared:
                color = BLUE
            else:
                color = self.color
                
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

def draw_map():
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if game_map[y][x] == 1:
                # Draw main wall
                pygame.draw.rect(screen, BLUE, rect)
                
                # Add cute brick pattern
                brick_height = CELL_SIZE // 3
                for i in range(3):
                    # Draw horizontal brick lines
                    offset = (i % 2) * (CELL_SIZE // 2)
                    pygame.draw.line(screen, PASTEL_BLUE, 
                                   (x * CELL_SIZE + offset, y * CELL_SIZE + i * brick_height),
                                   (x * CELL_SIZE + CELL_SIZE - offset, y * CELL_SIZE + i * brick_height), 2)
                
                # Add cute corner decorations
                if (x > 0 and game_map[y][x-1] == 1) and (y > 0 and game_map[y-1][x] == 1):
                    # Top-left corner
                    pygame.draw.circle(screen, PASTEL_BLUE, (x * CELL_SIZE + 4, y * CELL_SIZE + 4), 3)
                if (x < GRID_WIDTH-1 and game_map[y][x+1] == 1) and (y > 0 and game_map[y-1][x] == 1):
                    # Top-right corner
                    pygame.draw.circle(screen, PASTEL_BLUE, (x * CELL_SIZE + CELL_SIZE - 4, y * CELL_SIZE + 4), 3)
                if (x > 0 and game_map[y][x-1] == 1) and (y < GRID_HEIGHT-1 and game_map[y+1][x] == 1):
                    # Bottom-left corner
                    pygame.draw.circle(screen, PASTEL_BLUE, (x * CELL_SIZE + 4, y * CELL_SIZE + CELL_SIZE - 4), 3)
                if (x < GRID_WIDTH-1 and game_map[y][x+1] == 1) and (y < GRID_HEIGHT-1 and game_map[y+1][x] == 1):
                    # Bottom-right corner
                    pygame.draw.circle(screen, PASTEL_BLUE, (x * CELL_SIZE + CELL_SIZE - 4, y * CELL_SIZE + CELL_SIZE - 4), 3)
                
                # Add cute dots in the middle of walls
                if (x > 0 and game_map[y][x-1] == 1) and (x < GRID_WIDTH-1 and game_map[y][x+1] == 1):
                    # Horizontal wall
                    pygame.draw.circle(screen, PASTEL_BLUE, (x * CELL_SIZE + CELL_SIZE//2, y * CELL_SIZE + CELL_SIZE//2), 2)
                if (y > 0 and game_map[y-1][x] == 1) and (y < GRID_HEIGHT-1 and game_map[y+1][x] == 1):
                    # Vertical wall
                    pygame.draw.circle(screen, PASTEL_BLUE, (x * CELL_SIZE + CELL_SIZE//2, y * CELL_SIZE + CELL_SIZE//2), 2)
                
                # Add cute patterns for T-junctions
                if (x > 0 and game_map[y][x-1] == 1) and (x < GRID_WIDTH-1 and game_map[y][x+1] == 1) and (y > 0 and game_map[y-1][x] == 1):
                    # T-junction facing up
                    pygame.draw.line(screen, PASTEL_BLUE, 
                                   (x * CELL_SIZE + CELL_SIZE//4, y * CELL_SIZE + CELL_SIZE//2),
                                   (x * CELL_SIZE + CELL_SIZE*3//4, y * CELL_SIZE + CELL_SIZE//2), 2)
                if (x > 0 and game_map[y][x-1] == 1) and (x < GRID_WIDTH-1 and game_map[y][x+1] == 1) and (y < GRID_HEIGHT-1 and game_map[y+1][x] == 1):
                    # T-junction facing down
                    pygame.draw.line(screen, PASTEL_BLUE, 
                                   (x * CELL_SIZE + CELL_SIZE//4, y * CELL_SIZE + CELL_SIZE//2),
                                   (x * CELL_SIZE + CELL_SIZE*3//4, y * CELL_SIZE + CELL_SIZE//2), 2)
                if (y > 0 and game_map[y-1][x] == 1) and (y < GRID_HEIGHT-1 and game_map[y+1][x] == 1) and (x > 0 and game_map[y][x-1] == 1):
                    # T-junction facing left
                    pygame.draw.line(screen, PASTEL_BLUE, 
                                   (x * CELL_SIZE + CELL_SIZE//2, y * CELL_SIZE + CELL_SIZE//4),
                                   (x * CELL_SIZE + CELL_SIZE//2, y * CELL_SIZE + CELL_SIZE*3//4), 2)
                if (y > 0 and game_map[y-1][x] == 1) and (y < GRID_HEIGHT-1 and game_map[y+1][x] == 1) and (x < GRID_WIDTH-1 and game_map[y][x+1] == 1):
                    # T-junction facing right
                    pygame.draw.line(screen, PASTEL_BLUE, 
                                   (x * CELL_SIZE + CELL_SIZE//2, y * CELL_SIZE + CELL_SIZE//4),
                                   (x * CELL_SIZE + CELL_SIZE//2, y * CELL_SIZE + CELL_SIZE*3//4), 2)
                
            elif game_map[y][x] == 2:
                pygame.draw.circle(screen, PASTEL_GREEN, (x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 6)
            elif game_map[y][x] == 3:
                pygame.draw.circle(screen, PURPLE, (x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 4)

def draw_score(pacman):
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {pacman.score}", True, WHITE)
    lives_text = font.render(f"Lives: {pacman.lives}", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (WIDTH - 120, 10))
    
    if pacman.power_mode:
        power_time = max(0, pacman.power_timer // pacman.fps)
        power_text = font.render(f"Power: {power_time}s", True, WHITE)
        screen.blit(power_text, (WIDTH // 2 - power_text.get_width() // 2, 10))

def check_collision(pacman, ghosts):
    for ghost in ghosts:
        # Check if Pacman and ghost are in the same position
        if pacman.x == ghost.x and pacman.y == ghost.y:
            if pacman.power_mode and not ghost.eaten:
                # Ghost is eaten, create corpse at spawn point
                ghost.eaten = True
                ghost.has_corpse = True
                ghost.respawn_timer = 0  # Start respawn timer
                ghost.x = ghost.start_x  # Move to spawn point
                ghost.y = ghost.start_y
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
                # Ghost is eaten, create corpse at spawn point
                ghost.eaten = True
                ghost.has_corpse = True
                ghost.respawn_timer = 0  # Start respawn timer
                ghost.x = ghost.start_x  # Move to spawn point
                ghost.y = ghost.start_y
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

def reset_game_map():
    """Reset the game map to initial state"""
    global game_map
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

async def game_over_screen():
    """Game over screen with options to restart or return to menu"""
    selected = 0
    options = ["Play Again", "Return to Menu", "Exit"]
    
    while True:
        screen.fill(BLACK)
        
        # Game Over title
        font = pygame.font.Font(None, 74)
        text = font.render("GAME OVER!", True, RED)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 3))
        
        # Options
        font = pygame.font.Font(None, 48)
        for i, option in enumerate(options):
            color = YELLOW if i == selected else WHITE
            option_text = font.render(option, True, color)
            y_pos = HEIGHT // 2 + i * 60
            screen.blit(option_text, (WIDTH // 2 - option_text.get_width() // 2, y_pos))
        
        # Instructions
        font = pygame.font.Font(None, 36)
        instruction = font.render("Use arrow keys and Enter to select", True, WHITE)
        screen.blit(instruction, (WIDTH // 2 - instruction.get_width() // 2, HEIGHT - 80))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    if selected == 0:  # Play Again
                        return "restart"
                    elif selected == 1:  # Return to Menu
                        return "menu"
                    else:  # Exit
                        return "quit"
        
        await asyncio.sleep(0.016)

async def start_screen():
    """Start screen with beautiful effects and mode selection"""
    selected = 0
    options = ["Manual Mode", "Autoplay Mode", "Exit"]
    
    # Animation variables
    title_bounce = 0
    time_counter = 0
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False, False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    if selected == 0:  # Manual Mode
                        return True, False
                    elif selected == 1:  # Autoplay Mode
                        return True, True
                    else:  # Exit
                        pygame.quit()
                        return False, False
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return False, False

        time_counter += 1
        title_bounce = math.sin(time_counter * 0.1) * 5
        
        # Blue gradient background
        for y in range(HEIGHT):
            blue_intensity = int(25 + (y / HEIGHT) * 100)
            color = (0, 0, blue_intensity + 100)
            pygame.draw.line(screen, color, (0, y), (WIDTH, y))
        
        # Title
        font = pygame.font.Font(None, 84)
        title = font.render("PACMAN AI", True, YELLOW)
        title_y = HEIGHT // 4 + title_bounce
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, title_y))
        
        # Subtitle
        font = pygame.font.Font(None, 36)
        subtitle = font.render("Artificial Intelligence - Pathfinding Algorithms", True, PASTEL_BLUE)
        screen.blit(subtitle, (WIDTH // 2 - subtitle.get_width() // 2, title_y + 80))
        
        # Menu options
        font = pygame.font.Font(None, 48)
        for i, option in enumerate(options):
            color = YELLOW if i == selected else PASTEL_BLUE
            option_text = font.render(option, True, color)
            screen.blit(option_text, (WIDTH // 2 - option_text.get_width() // 2, HEIGHT // 2 + i * 60))
        
        # Instructions
        font = pygame.font.Font(None, 32)
        instruction = font.render("Arrow Keys: Move | Enter: Select | ESC: Exit", True, WHITE)
        screen.blit(instruction, (WIDTH // 2 - instruction.get_width() // 2, HEIGHT - 100))
        
        # Animated Pacman preview
        pacman_x = WIDTH // 4
        pacman_y = HEIGHT - 150
        pacman_radius = 15
        mouth_angle = (time_counter * 10) % 60
        
        pygame.draw.arc(screen, YELLOW, 
                       (pacman_x - pacman_radius, pacman_y - pacman_radius, 
                        pacman_radius * 2, pacman_radius * 2),
                       math.radians(mouth_angle), math.radians(360 - mouth_angle), pacman_radius)
        
        # Animated dots
        for i in range(5):
            dot_x = pacman_x + 40 + i * 20
            pygame.draw.circle(screen, PASTEL_BLUE, (dot_x, pacman_y), 3)
        
        # Ghost preview
        ghost_colors = [RED, PINK, CYAN, ORANGE]
        for i, color in enumerate(ghost_colors):
            ghost_x = WIDTH * 3 // 4 + i * 25
            ghost_y = HEIGHT - 150 + math.sin(time_counter * 0.15 + i) * 5
            pygame.draw.circle(screen, color, (int(ghost_x), int(ghost_y)), 12)
            pygame.draw.rect(screen, color, (ghost_x - 12, ghost_y, 24, 12))
        
        pygame.display.flip()
        await asyncio.sleep(0.016)  # Add small delay to prevent high CPU usage

async def win_screen():
    """Win screen with options to restart or return to menu"""
    selected = 0
    options = ["Play Again", "Return to Menu", "Exit"]
    time_counter = 0
    
    while True:
        time_counter += 1
        
        # Celebration background
        for y in range(HEIGHT):
            color_intensity = int(30 + (y / HEIGHT) * 50)
            color = (color_intensity, color_intensity // 2, 0)
            pygame.draw.line(screen, color, (0, y), (WIDTH, y))
        
        # Animated confetti
        for i in range(20):
            x = (i * 50 + time_counter * 2) % WIDTH
            y = (i * 30 + time_counter) % HEIGHT
            color = [RED, YELLOW, CYAN, PINK][i % 4]
            pygame.draw.circle(screen, color, (x, y), 3)
        
        # Victory title
        font = pygame.font.Font(None, 84)
        title_bounce = math.sin(time_counter * 0.1) * 8
        text = font.render("VICTORY!", True, YELLOW)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 3 + title_bounce))
        
        # Options
        font = pygame.font.Font(None, 48)
        for i, option in enumerate(options):
            color = YELLOW if i == selected else WHITE
            if i == selected:
                glow_text = font.render(option, True, (255, 255, 150))
                screen.blit(glow_text, (WIDTH // 2 - glow_text.get_width() // 2 + 2, HEIGHT // 2 + i * 60 + 2))
            
            option_text = font.render(option, True, color)
            screen.blit(option_text, (WIDTH // 2 - option_text.get_width() // 2, HEIGHT // 2 + i * 60))
        
        # Instructions
        font = pygame.font.Font(None, 36)
        instruction = font.render("Use arrow keys and Enter to select", True, WHITE)
        screen.blit(instruction, (WIDTH // 2 - instruction.get_width() // 2, HEIGHT - 80))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    if selected == 0:  # Play Again
                        reset_game_map()  # Reset map before restarting
                        return "restart"
                    elif selected == 1:  # Return to Menu
                        reset_game_map()  # Reset map before returning to menu
                        return "menu"
                    else:  # Exit
                        return "quit"
        
        await asyncio.sleep(0.016)

async def game_loop(difficulty, autoplay=False):
    """Main game loop with autoplay option"""
    pacman = Pacman()
    pacman.fps = difficulty["fps"]
    ghosts = [
        Ghost(9, 9, RED, "astar", difficulty["ghost_update_freq"]),
        Ghost(8, 9, PINK, "bfs", difficulty["ghost_update_freq"]),
        Ghost(10, 9, CYAN, "dfs", difficulty["ghost_update_freq"]),
        Ghost(9, 8, ORANGE, "random", difficulty["ghost_update_freq"])
    ]
    
    running = True
    game_over = False
    win = False
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "menu"  # Return to menu
                if not autoplay:  # Manual mode: handle player input
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
            
            # Autoplay logic
            if autoplay:
                pacman.autoplay_move(ghosts)
            
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
            # Draw ghost corpses (red dots) at spawn points with glow effect
            for ghost in ghosts:
                if ghost.has_corpse:
                    # Calculate glow intensity using sine wave
                    glow_intensity = (math.sin(ghost.glow_timer * 0.2) + 1) / 2  # Range from 0 to 1
                    # Create glowing red color
                    glow_red = int(255 * glow_intensity)
                    glow_color = (glow_red, 0, 0)
                    
                    # Draw outer glow
                    glow_radius = int(CELL_SIZE // 2 * (1 + glow_intensity * 0.3))  # Vary size with glow
                    pygame.draw.circle(screen, glow_color, 
                                     (ghost.start_x * CELL_SIZE + CELL_SIZE // 2,
                                      ghost.start_y * CELL_SIZE + CELL_SIZE // 2),
                                     glow_radius)
                    
                    # Draw inner solid circle
                    pygame.draw.circle(screen, RED, 
                                     (ghost.start_x * CELL_SIZE + CELL_SIZE // 2,
                                      ghost.start_y * CELL_SIZE + CELL_SIZE // 2),
                                     CELL_SIZE // 2)
            
            pacman.draw()
            # Only draw ghosts that are not eaten
            for ghost in ghosts:
                if not ghost.eaten:
                    ghost.draw()
            draw_score(pacman)
            pygame.display.flip()
            clock.tick(difficulty["fps"])
            await asyncio.sleep(1.0 / difficulty["fps"])
        elif game_over:
            result = await game_over_screen()
            return result
        elif win:
            result = await win_screen()
            return result

async def main():
    """Main function with menu loop"""
    try:
        while True:
            # Show start screen and get mode (manual or autoplay)
            start_game, autoplay = await start_screen()
            if not start_game:
                break
            
            # Show difficulty selection
            difficulty = await difficulty_screen()
            if difficulty is None:
                break
            
            # Reset game map before starting new game
            reset_game_map()
            
            # Game loop with restart/menu options
            while True:
                result = await game_loop(difficulty, autoplay)
                
                if result == "quit":
                    pygame.quit()
                    return
                elif result == "menu":
                    reset_game_map()  # Reset map before returning to menu
                    break  # Return to start screen
                elif result == "restart":
                    reset_game_map()  # Reset map before restarting
                    continue  # Restart the game with same difficulty
    
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        pygame.quit()
        return

if platform.system() == "Emscripten":
    asyncio.run_coroutine_threadsafe(main(), asyncio.get_event_loop())
else:
    if __name__ == "__main__":
        try:
            asyncio.run(main())
        except KeyboardInterrupt:
            pygame.quit()