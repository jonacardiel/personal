import pygame
import sys
import math
import random
import os

# Initialize Pygame
pygame.init()

# --- Music ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SONG_FILENAME = "Evanescence - Bring Me To Life (Official HD Music Video).mp3"
SONG_PATH = os.path.join(SCRIPT_DIR, SONG_FILENAME)
if os.path.exists(SONG_PATH):
    pygame.mixer.init()
    pygame.mixer.music.load(SONG_PATH)
    pygame.mixer.music.play(-1)  # Loop indefinitely
else:
    print(f"Music file not found: {SONG_PATH}")

# --- Game Constants ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TURRET_SIZE = 50
PROJECTILE_RADIUS = 10
PROJECTILE_SPEED = 10
TARGET_SIZE = 30
TARGET_SPEED = 1  # Was 2, now 50% slower
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (100, 100, 100)

# --- Set up the display ---
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Target Practice")

# --- Game Objects ---

# Turret (un-movable, rotatable)
turret_x = SCREEN_WIDTH // 2
turret_y = SCREEN_HEIGHT - 50
turret_angle = 0  # Initial angle in degrees

# Projectiles
projectiles = []

# Targets
targets = []
TARGET_SPAWN_RATE = 60  # Spawn a new target every 60 frames (adjust for difficulty)
spawn_counter = 0

# Score
score = 0
font = pygame.font.Font(None, 36)

# --- Game Functions ---

def create_target():
    side = random.choice(["top", "bottom", "left", "right"])
    if side == "top":
        x = random.randint(0, SCREEN_WIDTH - TARGET_SIZE)
        y = -TARGET_SIZE
    elif side == "bottom":
        x = random.randint(0, SCREEN_WIDTH - TARGET_SIZE)
        y = SCREEN_HEIGHT + TARGET_SIZE
    elif side == "left":
        x = -TARGET_SIZE
        y = random.randint(0, SCREEN_HEIGHT - TARGET_SIZE)
    elif side == "right":
        x = SCREEN_WIDTH + TARGET_SIZE
        y = random.randint(0, SCREEN_HEIGHT - TARGET_SIZE)
    speed_x = random.uniform(-TARGET_SPEED, TARGET_SPEED)
    speed_y = random.uniform(-TARGET_SPEED, TARGET_SPEED)
    # Ensure the target moves towards the screen (general direction)
    if side == "top" and speed_y < 0: speed_y = TARGET_SPEED / 2
    if side == "bottom" and speed_y > 0: speed_y = -TARGET_SPEED / 2
    if side == "left" and speed_x < 0: speed_x = TARGET_SPEED / 2
    if side == "right" and speed_x > 0: speed_x = -TARGET_SPEED / 2

    # Adjust speed slightly to avoid purely horizontal/vertical movement initially
    if speed_x == 0: speed_x = random.uniform(-0.5, 0.5)
    if speed_y == 0: speed_y = random.uniform(-0.5, 0.5)

    targets.append({"rect": pygame.Rect(x, y, TARGET_SIZE, TARGET_SIZE), "speed_x": speed_x, "speed_y": speed_y})

def draw_turret(angle):
    center = (turret_x, turret_y)
    length = TURRET_SIZE
    rad_angle = math.radians(angle - 90)  # Adjust for drawing orientation
    end_x = center[0] + length * math.cos(rad_angle)
    end_y = center[1] + length * math.sin(rad_angle)
    pygame.draw.circle(screen, GRAY, center, TURRET_SIZE // 2)
    pygame.draw.line(screen, GRAY, center, (int(end_x), int(end_y)), 5)

def draw_projectile(projectile):
    pygame.draw.circle(screen, WHITE, (int(projectile["x"]), int(projectile["y"])), PROJECTILE_RADIUS)

def draw_target(target):
    pygame.draw.rect(screen, RED, target["rect"])

def display_score():
    text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(text, (10, 10))

# --- Game Loop ---
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                rad_angle = math.radians(turret_angle - 90)
                projectile_x = turret_x + TURRET_SIZE * math.cos(rad_angle)
                projectile_y = turret_y + TURRET_SIZE * math.sin(rad_angle)
                projectiles.append({
                    "x": projectile_x,
                    "y": projectile_y,
                    "angle": rad_angle,
                    "speed": PROJECTILE_SPEED
                })
        elif event.type == pygame.MOUSEMOTION:
            # Calculate angle to mouse position
            dx = event.pos[0] - turret_x
            dy = event.pos[1] - turret_y
            if dx != 0 or dy != 0:
                turret_angle = math.degrees(math.atan2(dy, dx)) + 90 # Adjust
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # Left mouse button
                rad_angle = math.radians(turret_angle - 90)
                projectile_x = turret_x + TURRET_SIZE * math.cos(rad_angle)
                projectile_y = turret_y + TURRET_SIZE * math.sin(rad_angle)
                projectiles.append({
                    "x": projectile_x,
                    "y": projectile_y,
                    "angle": rad_angle,
                    "speed": PROJECTILE_SPEED
                })

    # --- Game Logic ---

    # Spawn targets
    spawn_counter += 1
    if spawn_counter >= TARGET_SPAWN_RATE:
        create_target()
        spawn_counter = 0

    # Move projectiles
    for projectile in list(projectiles):
        projectile["x"] += projectile["speed"] * math.cos(projectile["angle"])
        projectile["y"] += projectile["speed"] * math.sin(projectile["angle"])
        # Remove off-screen projectiles
        if projectile["x"] < -PROJECTILE_RADIUS or projectile["x"] > SCREEN_WIDTH + PROJECTILE_RADIUS or \
           projectile["y"] < -PROJECTILE_RADIUS or projectile["y"] > SCREEN_HEIGHT + PROJECTILE_RADIUS:
            projectiles.remove(projectile)

    # Move targets
    for target in list(targets):
        target["rect"].x += target["speed_x"]
        target["rect"].y += target["speed_y"]
        # Remove off-screen targets (optional: could decrease score or end game)
        if target["rect"].right < 0 or target["rect"].left > SCREEN_WIDTH or \
           target["rect"].bottom < 0 or target["rect"].top > SCREEN_HEIGHT:
            targets.remove(target)
            # Optionally: score -= 1  # Example penalty for letting a target escape

    # --- Collision Detection ---
    for projectile in list(projectiles): # Iterate over a copy to allow removal
        for target in list(targets): # Iterate over a copy
            if projectile["x"] > target["rect"].left and projectile["x"] < target["rect"].right and \
               projectile["y"] > target["rect"].top and projectile["y"] < target["rect"].bottom:
                projectiles.remove(projectile)
                targets.remove(target)
                score += 1
                # --- Placeholder for Target Hit Sound Effect ---
                # pygame.mixer.Sound("target_hit.wav").play() # Example
                break # Break inner loop since projectile hit a target

    # --- Drawing ---
    screen.fill(BLACK) # Background

    # Draw targets
    for target in targets:
        draw_target(target)

    # Draw projectiles
    for projectile in projectiles:
        draw_projectile(projectile)

    # Draw turret
    draw_turret(turret_angle)

    # Display score
    display_score()

    # Update the display
    pygame.display.flip()


# Quit Pygame
pygame.quit()
sys.exit()
