# Pacman Game with AI Pathfinding

A Python implementation of the classic Pacman game featuring different AI pathfinding algorithms for ghost behavior.

## Features

- Classic Pacman gameplay mechanics
- Multiple ghost AI behaviors using different pathfinding algorithms:
  - Red Ghost: A* pathfinding for intelligent chase
  - Pink Ghost: Breadth-First Search (BFS) for systematic pursuit
  - Cyan Ghost: Depth-First Search (DFS) for unpredictable movement
  - Orange Ghost: Random movement patterns
- Power pellets that allow Pacman to eat ghosts
- Score tracking system
- Multiple lives system
- Responsive controls
- Start and end game screens

## Requirements

- Python 3.x
- Pygame library

## Installation

1. Make sure you have Python installed on your system
2. Install the required dependency:
   ```
   pip install pygame
   ```
3. Run the game:
   ```
   python pacman.py
   ```

## How to Play

### Controls
- Use Arrow Keys to move Pacman
- Press SPACE to start the game

### Gameplay
- Navigate Pacman through the maze
- Collect dots (10 points each) and power pellets (50 points each)
- Avoid ghosts unless powered up
- When powered up (after eating a power pellet):
  - Ghosts turn blue and become vulnerable
  - Eating a ghost awards 200 points
  - Power mode lasts for 10 seconds
- Clear all dots and power pellets to win

### Scoring System
- Regular Dot: 10 points
- Power Pellet: 50 points
- Ghost (when powered up): 200 points

## Game Elements

### Pacman
- Starts with 3 lives
- Dies upon ghost contact (unless powered up)
- Can eat ghosts when powered up

### Ghosts
- Each ghost uses a different pathfinding strategy:
  - Red Ghost (A*): Most efficient pathfinding to chase Pacman
  - Pink Ghost (BFS): Methodical pursuit using breadth-first search
  - Cyan Ghost (DFS): Depth-first search for more varied movement
  - Orange Ghost: Random movement for unpredictability
- Ghosts become vulnerable when Pacman eats a power pellet
- Return to their starting position when eaten

## Game States

- Start Screen: Shows game title and basic instructions
- Gameplay: Active game state with score and lives display
- Game Over: Appears when all lives are lost
- Win Screen: Appears when all dots and power pellets are collected