'''from importlib.metadata import pass_none

import pygame
import time
import random
import psycopg2
import json

# === DATABASE SETUP ===
conn = psycopg2.connect(
    dbname="snake_scores",
    user="postgres",
    password="pp2lab10",
    host = "localhost",
    port="5432"
)
cursor = conn.cursor()

# Create tables if they don't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY
)
''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS user_scores (
    username TEXT REFERENCES users(username),
    score INTEGER,
    level INTEGER,
    snake_body TEXT,
    direction TEXT
)
''')
conn.commit()

# === GAME SETUP ===
snake_speed = 10
window_x = 700
window_y = 500

black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)

def get_username():
    input_box = pygame.Rect(window_x // 2 - 100, window_y // 2 - 20, 200, 40)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    font = pygame.font.Font(None, 36)

while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        return text
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

def draw_walls(level):
            if level in walls:
                for wall in walls[level]:
                    pygame.draw.rect(game_window, blue, pygame.Rect(wall[0], wall[1], 10, 10))

def save_game():
            cursor.execute("DELETE FROM user_scores WHERE username = %s", (username,))
            cursor.execute('''
                INSERT INTO user_scores (username, score, level, snake_body, direction)
                VALUES (%s, %s, %s, %s, %s)
            ''', (username, score, level, json.dumps(snake_body), direction))
            conn.commit()
            print("Game saved!")

def show_score_level(choice, color, font, size):
            score_font = pygame.font.SysFont(font, size)
            score_surface = score_font.render(f'Score: {score}', True, color)
            level_surface = score_font.render(f'Level: {level}', True, color)
            score_rect = score_surface.get_rect(topleft=(10, 10))
            level_rect = level_surface.get_rect(topleft=(10, 40))
            game_window.blit(score_surface, score_rect)
            game_window.blit(level_surface, level_rect)

def game_over():
            my_font = pygame.font.SysFont('Helvetica', 50)
            game_over_surface = my_font.render('Your Score is : ' + str(score), True, red)
            game_over_rect = game_over_surface.get_rect()
            game_over_rect.midtop = (window_x / 2, window_y / 4)
            game_window.blit(game_over_surface, game_over_rect)
            pygame.display.flip()
            time.sleep(2)
            pygame.quit()
            quit()

        game_window.fill((30, 30, 30))
        # Render the current text.
        txt_surface = font.render(text, True, color)
        # Resize the box if the text is too long.
        width = max(200, txt_surface.get_width() + 10)
        input_box.w = width
        # Blit the text.
        game_window.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        # Blit the input_box rect.
        pygame.draw.rect(game_window, color, input_box, 2)

        prompt_surface = font.render("Enter your username:", True, white)
        game_window.blit(prompt_surface, (window_x // 2 - prompt_surface.get_width() // 2, window_y // 2 - 70))

        pygame.display.flip()
        fps.tick(30)

pygame.init()
pygame.display.set_caption('The Snake Game')
game_window = pygame.display.set_mode((window_x, window_y))
fps = pygame.time.Clock()

username = get_username()

# === LOGIN SYSTEM ===

cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
user = cursor.fetchone()
if not user:
    cursor.execute("INSERT INTO users (username) VALUES (%s)", (username,))
    conn.commit()
    snake_position = [window_x / 2, window_y / 2]
    snake_body = [[100, 50], [90, 50], [80, 50], [70, 50]]
    direction = 'RIGHT'
    score = 0
    level = 1
    snake_speed = 10
else:
    cursor.execute("SELECT * FROM user_scores WHERE username = %s", (username,))
    saved_game = cursor.fetchone()
    if saved_game:
        score = saved_game[1]
        level = saved_game[2]
        snake_body = json.loads(saved_game[3])
        snake_position = list(snake_body[0])
        direction = saved_game[4]
        snake_speed = 10 + (level - 1) * 5
        print(f"Welcome back {username}! Loaded your level {level} and score {score}.")
    else:
        snake_position = [window_x / 2, window_y / 2]
        snake_body = [[100, 50], [90, 50], [80, 50], [70, 50]]
        direction = 'RIGHT'
        score = 0
        level = 1
        snake_speed = 10

# === FRUIT SETUP ===
fruit_position = [random.randrange(10, window_x, 10), random.randrange(10, window_y, 10)]
fruit_spawn = True
change_to = direction
pause = False

# === WALLS FOR LEVELS ===
walls = {
    2: [(300, i) for i in range(100, 400, 10)],
    3: [(i, 250) for i in range(100, 600, 10)],
    4: [(150, i) for i in range(150, 350, 10)] + [(550, i) for i in range(150, 350, 10)],
}


# === GAME LOOP ===
while True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                change_to = 'UP'
            if event.key == pygame.K_DOWN:
                change_to = 'DOWN'
            if event.key == pygame.K_LEFT:
                change_to = 'LEFT'
            if event.key == pygame.K_RIGHT:
                change_to = 'RIGHT'
            if event.key == pygame.K_p:
                pause = not pause
                if pause:
                    save_game()

    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    if change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    if change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    if change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'

    if pause:
        show_score_level(1, white, 'Helvetica', 20)
        pause_font = pygame.font.SysFont('Helvetica', 50)
        pause_surface = pause_font.render('Paused (Saved)', True, blue)
        pause_rect = pause_surface.get_rect(center=(window_x // 2, window_y // 2))
        game_window.blit(pause_surface, pause_rect)
        pygame.display.update()
        fps.tick(5)
        continue

    if direction == 'UP':
        snake_position[1] -= 10
    if direction == 'DOWN':
        snake_position[1] += 10
    if direction == 'LEFT':
        snake_position[0] -= 10
    if direction == 'RIGHT':
        snake_position[0] += 10

    snake_body.insert(0, list(snake_position))
    if snake_position[0] == fruit_position[0] and snake_position[1] == fruit_position[1]:
        score += 10
        if score % 30 == 0:
            level += 1
            snake_speed += 5
        fruit_spawn = False
    else:
        snake_body.pop()

    if not fruit_spawn:
        fruit_position = [random.randrange(1, (window_x // 10)) * 10, random.randrange(1, (window_y // 10)) * 10]
    fruit_spawn = True
    game_window.fill(black)

    for pos in snake_body:
        pygame.draw.rect(game_window, green, pygame.Rect(pos[0], pos[1], 10, 10))
    pygame.draw.rect(game_window, white, pygame.Rect(fruit_position[0], fruit_position[1], 10, 10))

    draw_walls(level)

    # Game over
    if snake_position[0] < 0 or snake_position[0] > window_x - 10:
        game_over()
    if snake_position[1] < 0 or snake_position[1] > window_y - 10:
        game_over()

    for block in snake_body[1:]:
        if snake_position[0] == block[0] and snake_position[1] == block[1]:
            game_over()

    # Collision with wall
    if level in walls:
        for wall in walls[level]:
            if snake_position[0] == wall[0] and snake_position[1] == wall[1]:
                game_over()

    show_score_level(1, white, 'Helvetica', 20)
    pygame.display.update()
    fps.tick(snake_speed)'''

import pygame
import time
import random
import psycopg2
import json

# === DATABASE SETUP ===
conn = psycopg2.connect(
    dbname="snake_scores",
    user="postgres",
    password="pp2lab10",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

# Create tables if they don't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY
)
''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS user_scores (
    username TEXT REFERENCES users(username),
    score INTEGER,
    level INTEGER,
    snake_body TEXT,
    direction TEXT
)
''')
conn.commit()

# === COLORS AND CONSTANTS ===
snake_speed = 10
window_x = 700
window_y = 500

black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)

walls = {
    2: [(300, i) for i in range(100, 400, 10)],
    3: [(i, 250) for i in range(100, 600, 10)],
    4: [(150, i) for i in range(150, 350, 10)] + [(550, i) for i in range(150, 350, 10)],
}

# === FUNCTIONS ===
def draw_walls(level):
    if level in walls:
        for wall in walls[level]:
            pygame.draw.rect(game_window, blue, pygame.Rect(wall[0], wall[1], 10, 10))

def save_game():
    cursor.execute("DELETE FROM user_scores WHERE username = %s", (username,))
    cursor.execute('''
        INSERT INTO user_scores (username, score, level, snake_body, direction)
        VALUES (%s, %s, %s, %s, %s)
    ''', (username, score, level, json.dumps(snake_body), direction))
    conn.commit()
    print("Game saved!")

def show_score_level(choice, color, font, size):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render(f'Score: {score}', True, color)
    level_surface = score_font.render(f'Level: {level}', True, color)
    score_rect = score_surface.get_rect(topleft=(10,10))
    level_rect = level_surface.get_rect(topleft=(10,40))
    game_window.blit(score_surface, score_rect)
    game_window.blit(level_surface, level_rect)

def game_over():
    my_font = pygame.font.SysFont('Helvetica', 50)
    game_over_surface = my_font.render('Your Score is : ' + str(score), True, red)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (window_x / 2, window_y / 4)
    game_window.blit(game_over_surface, game_over_rect)
    pygame.display.flip()
    time.sleep(2)
    pygame.quit()
    quit()

def get_username():
    input_box = pygame.Rect(window_x // 2 - 100, window_y // 2 - 20, 200, 40)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    font = pygame.font.Font(None, 36)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        return text
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        game_window.fill((30, 30, 30))
        txt_surface = font.render(text, True, color)
        width = max(200, txt_surface.get_width() + 10)
        input_box.w = width
        game_window.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(game_window, color, input_box, 2)

        prompt_surface = font.render("Enter your username:", True, white)
        game_window.blit(prompt_surface, (window_x // 2 - prompt_surface.get_width() // 2, window_y // 2 - 70))

        pygame.display.flip()
        fps.tick(30)

# === GAME INIT ===
pygame.init()
pygame.display.set_caption('The Snake Game')
game_window = pygame.display.set_mode((window_x, window_y))
fps = pygame.time.Clock()

username = get_username()

# === LOGIN SYSTEM ===
cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
user = cursor.fetchone()
if not user:
    cursor.execute("INSERT INTO users (username) VALUES (%s)", (username,))
    conn.commit()

cursor.execute("SELECT * FROM user_scores WHERE username = %s", (username,))
saved_game = cursor.fetchone()

if saved_game:
    score = saved_game[1]
    level = saved_game[2]
    snake_body = json.loads(saved_game[3])
    snake_position = list(snake_body[0])
    direction = saved_game[4]
    snake_speed = 10 + (level - 1) * 5
    print(f"Welcome back {username}! Loaded your level {level} and score {score}.")
else:
    snake_position = [window_x / 2, window_y / 2]
    snake_body = [[100, 50], [90, 50], [80, 50], [70, 50]]
    direction = 'RIGHT'
    score = 0
    level = 1
    snake_speed = 10

# === FRUIT SETUP ===
fruit_position = [random.randrange(10, window_x, 10), random.randrange(10, window_y, 10)]
fruit_spawn = True
change_to = direction
pause = False

# === GAME LOOP ===
while True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                change_to = 'UP'
            if event.key == pygame.K_DOWN:
                change_to = 'DOWN'
            if event.key == pygame.K_LEFT:
                change_to = 'LEFT'
            if event.key == pygame.K_RIGHT:
                change_to = 'RIGHT'
            if event.key == pygame.K_p:
                pause = not pause
                if pause:
                    save_game()

    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    if change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    if change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    if change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'

    if pause:
        show_score_level(1, white, 'Helvetica', 20)
        pause_font = pygame.font.SysFont('Helvetica', 50)
        pause_surface = pause_font.render('Paused (Saved)', True, blue)
        pause_rect = pause_surface.get_rect(center=(window_x // 2, window_y // 2))
        game_window.blit(pause_surface, pause_rect)
        pygame.display.update()
        fps.tick(5)
        continue

    if direction == 'UP':
        snake_position[1] -= 10
    if direction == 'DOWN':
        snake_position[1] += 10
    if direction == 'LEFT':
        snake_position[0] -= 10
    if direction == 'RIGHT':
        snake_position[0] += 10

    snake_body.insert(0, list(snake_position))
    if snake_position[0] == fruit_position[0] and snake_position[1] == fruit_position[1]:
        score += 10
        if score % 30 == 0:
            level += 1
            snake_speed += 5
        fruit_spawn = False
    else:
        snake_body.pop()

    if not fruit_spawn:
        fruit_position = [random.randrange(1, (window_x // 10)) * 10, random.randrange(1, (window_y // 10)) * 10]
    fruit_spawn = True

    game_window.fill(black)

    for pos in snake_body:
        pygame.draw.rect(game_window, green, pygame.Rect(pos[0], pos[1], 10, 10))
    pygame.draw.rect(game_window, white, pygame.Rect(fruit_position[0], fruit_position[1], 10, 10))

    draw_walls(level)

    # Game over conditions
    if snake_position[0] < 0 or snake_position[0] > window_x - 10:
        game_over()
    if snake_position[1] < 0 or snake_position[1] > window_y - 10:
        game_over()
    for block in snake_body[1:]:
        if snake_position[0] == block[0] and snake_position[1] == block[1]:
            game_over()
    if level in walls:
        for wall in walls[level]:
            if snake_position[0] == wall[0] and snake_position[1] == wall[1]:
                game_over()

    show_score_level(1, white, 'Helvetica', 20)
    pygame.display.update()
    fps.tick(snake_speed)

