import pygame
import random
import heapq
import math
from collections import deque

# Initialize Pygame
pygame.init()

# Game constants
CELL_SIZE = 30
GRID_WIDTH = 19
GRID_HEIGHT = 21
WIDTH = CELL_SIZE * GRID_WIDTH
HEIGHT = CELL_SIZE * GRID_HEIGHT + 60  # Extra space for UI
FPS = 8  # Smoother animation

# Cute color palette
BLACK = (15, 15, 35)  # Dark navy instead of pure black
BLUE = (64, 128, 255)  # Bright blue for walls
WHITE = (255, 255, 255)
YELLOW = (255, 220, 0)  # Warmer yellow
RED = (255, 80, 80)  # Softer red
PINK = (255, 150, 200)  # Cute pink
CYAN = (100, 255, 255)  # Bright cyan
ORANGE = (255, 180, 50)  # Warm orange
PURPLE = (180, 100, 255)  # Cute purple
GREEN = (100, 255, 150)  # Mint green
GOLD = (255, 215, 0)  # Gold for special effects

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🎮 Cute Pacman Adventure 🎮")
clock = pygame.time.Clock()

# Animation variables
frame_count = 0
particles = []

# Game map
# 0: empty path, 1: wall, 2: dot, 3: power pellet
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

class Particle:
    def __init__(self, x, y, color, velocity, life):
        self.x = x
        self.y = y
        self.color = color
        self.velocity = velocity
        self.life = life
        self.max_life = life
        
    def update(self):
        self.x += self.velocity[0]
        self.y += self.velocity[1]
        self.life -= 1
        
    def draw(self):
        if self.life > 0:
            alpha = int(255 * (self.life / self.max_life))
            size = int(3 * (self.life / self.max_life))
            if size > 0:
                pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), size)

def create_particles(x, y, color, count=5):
    for _ in range(count):
        velocity = (random.uniform(-2, 2), random.uniform(-2, 2))
        life = random.randint(15, 30)
        particles.append(Particle(x, y, color, velocity, life))

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
        self.mouth_animation = 0
        self.bounce_offset = 0

    def move(self):
        # Try to move in the next_direction if possible
        next_x = self.x + self.next_direction[0]
        next_y = self.y + self.next_direction[1]
        
        if 0 <= next_x < GRID_WIDTH and 0 <= next_y < GRID_HEIGHT and game_map[next_y][next_x] != 1:
            self.direction = self.next_direction
        
        # Move in the current direction
        next_x = self.x + self.direction[0]
        next_y = self.y + self.direction[1]
        
        if 0 <= next_x < GRID_WIDTH and 0 <= next_y < GRID_HEIGHT and game_map[next_y][next_x] != 1:
            self.x = next_x
            self.y = next_y
            
            # Collect dots with particles
            if game_map[self.y][self.x] == 2:
                game_map[self.y][self.x] = 0
                self.score += 10
                create_particles(self.x * CELL_SIZE + CELL_SIZE // 2, 
                               self.y * CELL_SIZE + CELL_SIZE // 2, GOLD, 3)
            
            # Collect power pellets with more particles
            elif game_map[self.y][self.x] == 3:
                game_map[self.y][self.x] = 0
                self.score += 50
                self.power_mode = True
                self.power_timer = FPS * 10  # 10 seconds of power mode
                create_particles(self.x * CELL_SIZE + CELL_SIZE // 2, 
                               self.y * CELL_SIZE + CELL_SIZE // 2, PURPLE, 8)
        
        # Handle power mode timer
        if self.power_mode:
            self.power_timer -= 1
            if self.power_timer <= 0:
                self.power_mode = False
        
        # Update animations
        self.mouth_animation = (self.mouth_animation + 1) % 20
        self.bounce_offset = math.sin(frame_count * 0.3) * 2

    def draw(self):
        # Draw Pacman with cute animations
        center_x = self.x * CELL_SIZE + CELL_SIZE // 2
        center_y = self.y * CELL_SIZE + CELL_SIZE // 2 + self.bounce_offset
        radius = CELL_SIZE // 2 - 2
        
        # Power mode glow effect
        if self.power_mode:
            glow_radius = radius + 5 + math.sin(frame_count * 0.5) * 3
            pygame.draw.circle(screen, GOLD, (int(center_x), int(center_y)), int(glow_radius), 2)
        
        # Mouth animation
        mouth_size = abs(math.sin(self.mouth_animation * 0.3)) * 60 + 20
        
        # Determine mouth angle based on direction
        if self.direction == RIGHT:
            start_angle = mouth_size // 2
            end_angle = 360 - mouth_size // 2
        elif self.direction == LEFT:
            start_angle = 180 - mouth_size // 2
            end_angle = 180 + mouth_size // 2
        elif self.direction == UP:
            start_angle = 270 - mouth_size // 2
            end_angle = 270 + mouth_size // 2
        else:  # DOWN
            start_angle = 90 - mouth_size // 2
            end_angle = 90 + mouth_size // 2
        
        # Draw Pacman body with gradient effect
        pygame.draw.circle(screen, YELLOW, (int(center_x), int(center_y)), radius)
        pygame.draw.circle(screen, GOLD, (int(center_x - 3), int(center_y - 3)), radius - 5)
        
        # Draw mouth
        if mouth_size > 30:
            mouth_points = []
            mouth_points.append((center_x, center_y))
            for angle in range(int(start_angle), int(end_angle), 5):
                x = center_x + radius * math.cos(math.radians(angle))
                y = center_y - radius * math.sin(math.radians(angle))
                mouth_points.append((x, y))
            if len(mouth_points) > 2:
                pygame.draw.polygon(screen, BLACK, mouth_points)
        
        # Draw cute eye
        eye_x = center_x + (5 if self.direction != LEFT else -5)
        eye_y = center_y - 5
        pygame.draw.circle(screen, BLACK, (int(eye_x), int(eye_y)), 3)
        pygame.draw.circle(screen, WHITE, (int(eye_x + 1), int(eye_y - 1)), 1)

class Ghost:
    def __init__(self, x, y, color, algorithm):
        self.x = x
        self.y = y
        self.color = color
        self.algorithm = algorithm
        self.direction = random.choice(DIRECTIONS)
        self.target_x = 0
        self.target_y = 0
        self.scared = False
        self.path = []
        self.update_counter = 0
        self.float_offset = random.uniform(0, 2 * math.pi)
        self.blink_timer = 0

    def set_target(self, pacman):
        # Set target based on ghost behavior
        if self.scared:
            # When scared, move randomly
            self.target_x = random.randint(0, GRID_WIDTH - 1)
            self.target_y = random.randint(0, GRID_HEIGHT - 1)
        else:
            # Target Pacman
            self.target_x = pacman.x
            self.target_y = pacman.y

    def move(self, pacman):
        self.update_counter += 1
        self.blink_timer += 1
        
        # Update path every few frames to reduce computation
        if self.update_counter >= 10 or not self.path:
            self.update_counter = 0
            self.set_target(pacman)
            
            # Choose pathfinding algorithm
            if self.algorithm == "bfs":
                self.path = self.bfs((self.x, self.y), (self.target_x, self.target_y))
            elif self.algorithm == "dfs":
                self.path = self.dfs((self.x, self.y), (self.target_x, self.target_y))
            elif self.algorithm == "astar":
                self.path = self.astar((self.x, self.y), (self.target_x, self.target_y))
            else:  # Default to random movement
                self.path = []
        
        # Move along the path
        if self.path:
            next_pos = self.path.pop(0)
            self.x, self.y = next_pos
        else:
            # Random movement if no path
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
        
        return []  # No path found

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
        
        return []  # No path found

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
        
        return []  # No path found

    def draw(self):
        center_x = self.x * CELL_SIZE + CELL_SIZE // 2
        center_y = self.y * CELL_SIZE + CELL_SIZE // 2 + math.sin(frame_count * 0.2 + self.float_offset) * 3
        radius = CELL_SIZE // 2 - 2
        
        # Choose color based on state
        if self.scared:
            if self.blink_timer % 20 < 10:  # Blinking effect when scared
                color = BLUE
            else:
                color = WHITE
        else:
            color = self.color
        
        # Draw shadow
        pygame.draw.ellipse(screen, (0, 0, 0, 50), 
                           (center_x - radius, center_y + radius + 5, radius * 2, radius // 2))
        
        # Draw ghost body with cute shape
        # Main body (circle)
        pygame.draw.circle(screen, color, (int(center_x), int(center_y)), radius)
        
        # Bottom wavy part
        wave_points = []
        wave_y = center_y + radius // 2
        for i in range(5):
            wave_x = center_x - radius + (i * radius // 2)
            wave_offset = math.sin(frame_count * 0.3 + i) * 3
            wave_points.append((wave_x, wave_y + wave_offset))
        
        # Create wavy bottom
        bottom_rect = pygame.Rect(center_x - radius, center_y, radius * 2, radius)
        pygame.draw.rect(screen, color, bottom_rect)
        
        # Draw wavy bottom edge
        for i in range(4):
            wave_x = center_x - radius + (i * radius // 2)
            wave_height = radius // 3 + math.sin(frame_count * 0.4 + i) * 2
            pygame.draw.rect(screen, color, 
                           (wave_x, center_y + radius, radius // 2, wave_height))
        
        # Draw cute eyes
        eye_radius = radius // 4
        eye_offset_x = radius // 3
        eye_offset_y = radius // 3
        
        # Left eye
        left_eye_x = center_x - eye_offset_x
        left_eye_y = center_y - eye_offset_y
        pygame.draw.circle(screen, WHITE, (int(left_eye_x), int(left_eye_y)), eye_radius)
        
        # Right eye
        right_eye_x = center_x + eye_offset_x
        right_eye_y = center_y - eye_offset_y
        pygame.draw.circle(screen, WHITE, (int(right_eye_x), int(right_eye_y)), eye_radius)
        
        # Pupils with direction
        pupil_radius = eye_radius // 2
        dx, dy = self.direction
        pupil_offset = 2
        
        # Left pupil
        pygame.draw.circle(screen, BLACK, 
                          (int(left_eye_x + dx * pupil_offset), 
                           int(left_eye_y + dy * pupil_offset)), pupil_radius)
        
        # Right pupil
        pygame.draw.circle(screen, BLACK, 
                          (int(right_eye_x + dx * pupil_offset), 
                           int(right_eye_y + dy * pupil_offset)), pupil_radius)
        
        # Add cute highlights
        pygame.draw.circle(screen, WHITE, 
                          (int(left_eye_x - 1), int(left_eye_y - 1)), 1)
        pygame.draw.circle(screen, WHITE, 
                          (int(right_eye_x - 1), int(right_eye_y - 1)), 1)

def draw_map():
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            
            if game_map[y][x] == 1:  # Wall with gradient
                # Main wall
                pygame.draw.rect(screen, BLUE, rect)
                # Highlight
                pygame.draw.rect(screen, CYAN, 
                               (rect.x + 2, rect.y + 2, rect.width - 4, rect.height - 4), 2)
                
            elif game_map[y][x] == 2:  # Animated dots
                dot_size = 3 + math.sin(frame_count * 0.1 + x + y) * 1
                pygame.draw.circle(screen, WHITE, 
                                  (x * CELL_SIZE + CELL_SIZE // 2, 
                                   y * CELL_SIZE + CELL_SIZE // 2), 
                                  int(dot_size))
                # Glow effect
                pygame.draw.circle(screen, GOLD, 
                                  (x * CELL_SIZE + CELL_SIZE // 2, 
                                   y * CELL_SIZE + CELL_SIZE // 2), 
                                  int(dot_size + 2), 1)
                
            elif game_map[y][x] == 3:  # Animated power pellets
                pellet_size = 8 + math.sin(frame_count * 0.2 + x + y) * 3
                # Main pellet
                pygame.draw.circle(screen, WHITE, 
                                  (x * CELL_SIZE + CELL_SIZE // 2, 
                                   y * CELL_SIZE + CELL_SIZE // 2), 
                                  int(pellet_size))
                # Pulsing glow
                glow_size = pellet_size + 5 + math.sin(frame_count * 0.3) * 3
                pygame.draw.circle(screen, PURPLE, 
                                  (x * CELL_SIZE + CELL_SIZE // 2, 
                                   y * CELL_SIZE + CELL_SIZE // 2), 
                                  int(glow_size), 2)

def draw_cute_ui(pacman):
    # Background for UI
    ui_rect = pygame.Rect(0, GRID_HEIGHT * CELL_SIZE, WIDTH, 60)
    pygame.draw.rect(screen, (30, 30, 60), ui_rect)
    pygame.draw.rect(screen, CYAN, ui_rect, 3)
    
    # Score with cute font effect
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"🍒 Score: {pacman.score}", True, GOLD)
    screen.blit(score_text, (10, GRID_HEIGHT * CELL_SIZE + 10))
    
    # Lives with heart icons
    lives_x = 10
    lives_y = GRID_HEIGHT * CELL_SIZE + 35
    font_small = pygame.font.Font(None, 24)
    lives_label = font_small.render("Lives:", True, WHITE)
    screen.blit(lives_label, (lives_x, lives_y))
    
    for i in range(pacman.lives):
        heart_x = lives_x + 60 + i * 25
        # Draw heart shape
        pygame.draw.circle(screen, RED, (heart_x, lives_y + 8), 6)
        pygame.draw.circle(screen, RED, (heart_x + 8, lives_y + 8), 6)
        pygame.draw.polygon(screen, RED, [(heart_x - 6, lives_y + 10), 
                                        (heart_x + 14, lives_y + 10), 
                                        (heart_x + 4, lives_y + 20)])
    
    # Power mode indicator
    if pacman.power_mode:
        power_text = font_small.render(f"⚡ POWER! {pacman.power_timer // FPS}s", True, YELLOW)
        screen.blit(power_text, (WIDTH - 150, GRID_HEIGHT * CELL_SIZE + 10))
        
        # Power mode glow effect around screen
        glow_alpha = int(100 + 50 * math.sin(frame_count * 0.5))
        glow_surface = pygame.Surface((WIDTH, HEIGHT))
        glow_surface.set_alpha(glow_alpha)
        pygame.draw.rect(glow_surface, GOLD, (0, 0, WIDTH, HEIGHT), 5)
        screen.blit(glow_surface, (0, 0))

def check_collision(pacman, ghosts):
    for ghost in ghosts:
        if pacman.x == ghost.x and pacman.y == ghost.y:
            if pacman.power_mode:
                # Ghost is eaten with particles
                create_particles(ghost.x * CELL_SIZE + CELL_SIZE // 2, 
                               ghost.y * CELL_SIZE + CELL_SIZE // 2, ghost.color, 10)
                ghost.x, ghost.y = 9, 9  # Return to center
                pacman.score += 200
            else:
                # Pacman loses a life
                pacman.lives -= 1
                create_particles(pacman.x * CELL_SIZE + CELL_SIZE // 2, 
                               pacman.y * CELL_SIZE + CELL_SIZE // 2, RED, 15)
                if pacman.lives > 0:
                    # Reset positions
                    pacman.x, pacman.y = 9, 15
                    for g in ghosts:
                        g.x, g.y = 9, 9
                return True
    return False

def check_win():
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if game_map[y][x] in [2, 3]:  # If there are still dots or power pellets
                return False
    return True

def cute_game_over_screen():
    # Animated background
    for i in range(50):
        screen.fill((20 + i, 20 + i, 40 + i))
        
        font = pygame.font.Font(None, 84)
        text = font.render("💀 GAME OVER 💀", True, RED)
        shadow = font.render("💀 GAME OVER 💀", True, BLACK)
        
        screen.blit(shadow, (WIDTH // 2 - text.get_width() // 2 + 3, 
                            HEIGHT // 2 - text.get_height() // 2 + 3))
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 
                          HEIGHT // 2 - text.get_height() // 2))
        
        # Sad face
        pygame.draw.circle(screen, YELLOW, (WIDTH // 2, HEIGHT // 2 + 80), 30)
        # Eyes
        pygame.draw.circle(screen, BLACK, (WIDTH // 2 - 10, HEIGHT // 2 + 70), 5)
        pygame.draw.circle(screen, BLACK, (WIDTH // 2 + 10, HEIGHT // 2 + 70), 5)
        # Sad mouth
        pygame.draw.arc(screen, BLACK, (WIDTH // 2 - 15, HEIGHT // 2 + 85, 30, 20), 
                       0, math.pi, 3)
        
        pygame.display.flip()
        pygame.time.wait(60)
    
    pygame.time.wait(2000)

def cute_win_screen():
    # Celebration animation
    for i in range(100):
        # Rainbow background
        colors = [RED, ORANGE, YELLOW, GREEN, CYAN, BLUE, PURPLE]
        color = colors[i % len(colors)]
        screen.fill(color)
        
        font = pygame.font.Font(None, 84)
        text = font.render("🎉 YOU WIN! 🎉", True, WHITE)
        shadow = font.render("🎉 YOU WIN! 🎉", True, BLACK)
        
        # Bouncing text
        bounce = math.sin(i * 0.3) * 10
        screen.blit(shadow, (WIDTH // 2 - text.get_width() // 2 + 3, 
                            HEIGHT // 2 - text.get_height() // 2 + 3 + bounce))
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 
                          HEIGHT // 2 - text.get_height() // 2 + bounce))
        
        # Happy face
        pygame.draw.circle(screen, YELLOW, (WIDTH // 2, HEIGHT // 2 + 80), 30)
        # Eyes
        pygame.draw.circle(screen, BLACK, (WIDTH // 2 - 10, HEIGHT // 2 + 70), 5)
        pygame.draw.circle(screen, BLACK, (WIDTH // 2 + 10, HEIGHT // 2 + 70), 5)
        # Happy mouth
        pygame.draw.arc(screen, BLACK, (WIDTH // 2 - 15, HEIGHT // 2 + 80, 30, 20), 
                       math.pi, 2 * math.pi, 3)
        
        # Confetti particles
        for j in range(20):
            x = random.randint(0, WIDTH)
            y = random.randint(0, HEIGHT)
            color = random.choice([RED, YELLOW, GREEN, BLUE, PINK])
            pygame.draw.circle(screen, color, (x, y), 3)
        
        pygame.display.flip()
        pygame.time.wait(50)
    
    pygame.time.wait(2000)

def cute_start_screen():
    # Animated start screen
    waiting = True
    animation_frame = 0
    
    while waiting:
        # Gradient background
        for y in range(HEIGHT):
            color_intensity = int(50 + 30 * math.sin(y * 0.01 + animation_frame * 0.1))
            pygame.draw.line(screen, (color_intensity, color_intensity // 2, color_intensity * 2), 
                           (0, y), (WIDTH, y))
        
        # Title with glow effect
        font_large = pygame.font.Font(None, 96)
        title = font_large.render("🎮 CUTE PACMAN 🎮", True, YELLOW)
        title_glow = font_large.render("🎮 CUTE PACMAN 🎮", True, GOLD)
        
        # Bouncing title
        title_bounce = math.sin(animation_frame * 0.2) * 5
        screen.blit(title_glow, (WIDTH // 2 - title.get_width() // 2 + 2, 
                                HEIGHT // 4 + title_bounce + 2))
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 
                           HEIGHT // 4 + title_bounce))
        
        # Instructions with cute styling
        font = pygame.font.Font(None, 36)
        instructions = [
            "🎯 Use arrow keys to move",
            "🍒 Eat all dots to win", 
            "👻 Avoid ghosts unless powered up",
            "⚡ Power pellets make you invincible!",
            "💝 Press SPACE to start"
        ]
        
        for i, line in enumerate(instructions):
            text_color = [WHITE, YELLOW, PINK, CYAN, GREEN][i]
            text = font.render(line, True, text_color)
            y_pos = HEIGHT // 2 + i * 45 + math.sin(animation_frame * 0.1 + i) * 3
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, y_pos))
        
        # Cute Pacman preview
        preview_x = WIDTH // 2 - 50
        preview_y = HEIGHT - 100
        pygame.draw.circle(screen, YELLOW, (preview_x, preview_y), 20)
        # Animated mouth
        mouth_angle = abs(math.sin(animation_frame * 0.3)) * 60 + 20
        pygame.draw.arc(screen, BLACK, (preview_x - 20, preview_y - 20, 40, 40),
                       math.radians(mouth_angle // 2), math.radians(360 - mouth_angle // 2), 20)
        
        # Ghost preview
        ghost_x = WIDTH // 2 + 50
        ghost_y = HEIGHT - 100 + math.sin(animation_frame * 0.2) * 5
        pygame.draw.circle(screen, RED, (ghost_x, int(ghost_y)), 20)
        pygame.draw.rect(screen, RED, (ghost_x - 20, int(ghost_y), 40, 20))
        # Ghost eyes
        pygame.draw.circle(screen, WHITE, (ghost_x - 8, int(ghost_y - 8)), 5)
        pygame.draw.circle(screen, WHITE, (ghost_x + 8, int(ghost_y - 8)), 5)
        pygame.draw.circle(screen, BLACK, (ghost_x - 8, int(ghost_y - 8)), 2)
        pygame.draw.circle(screen, BLACK, (ghost_x + 8, int(ghost_y - 8)), 2)
        
        pygame.display.flip()
        animation_frame += 1
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                waiting = False
        
        clock.tick(30)
    
    return True

def main():
    global frame_count, particles
    
    # Create game objects
    pacman = Pacman()
    ghosts = [
        Ghost(9, 9, RED, "astar"),      # Red ghost uses A*
        Ghost(8, 9, PINK, "bfs"),       # Pink ghost uses BFS
        Ghost(10, 9, CYAN, "dfs"),      # Cyan ghost uses DFS
        Ghost(9, 8, ORANGE, "random")   # Orange ghost moves randomly
    ]
    
    # Show start screen
    if not cute_start_screen():
        return
    
    # Main game loop
    running = True
    game_over = False
    win = False
    
    while running:
        frame_count += 1
        
        # Handle events
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
            # Clear screen with cute background
            screen.fill(BLACK)
            
            # Update game state
            pacman.move()
            
            # Update ghost states based on pacman's power mode
            for ghost in ghosts:
                ghost.scared = pacman.power_mode
                ghost.move(pacman)
            
            # Check for collisions
            if check_collision(pacman, ghosts):
                if pacman.lives <= 0:
                    game_over = True
            
            # Check for win condition
            if check_win():
                win = True
            
            # Update particles
            particles = [p for p in particles if p.life > 0]
            for particle in particles:
                particle.update()
            
            # Draw everything
            draw_map()
            pacman.draw()
            for ghost in ghosts:
                ghost.draw()
            
            # Draw particles
            for particle in particles:
                particle.draw()
            
            draw_cute_ui(pacman)
            
            # Update display
            pygame.display.flip()
            
            # Cap the frame rate
            clock.tick(FPS)
        elif game_over:
            cute_game_over_screen()
            running = False
        elif win:
            cute_win_screen()
            running = False
    
    pygame.quit()

if __name__ == "__main__":
    main()