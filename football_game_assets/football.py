import pygame
import sys
import time

pygame.init()

# Window setup
WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Football Game")
clock = pygame.time.Clock()

# Load images
player1_img = pygame.image.load("player1.png")
player2_img = pygame.image.load("player2.png")
player1_img = pygame.transform.scale(player1_img, (50, 50))
player2_img = pygame.transform.scale(player2_img, (50, 50))

# Colors and fonts
WHITE = (255, 255, 255)
GREEN = (34, 139, 34)
YELLOW = (255, 215, 0)
RED = (255, 0, 0)
font = pygame.font.SysFont(None, 40)
big_font = pygame.font.SysFont(None, 60)

# Game constants
player_size = 50
ball_radius = 20
goal_width = 20
goal_height = 150
score1 = 0
score2 = 0
match_time = 60
speed = 6
shoot_power = 8
game_mode = "two"

# Positions
player1 = pygame.Rect(100, HEIGHT//2 - player_size//2, player_size, player_size)
player2 = pygame.Rect(WIDTH - 150, HEIGHT//2 - player_size//2, player_size, player_size)
ball = pygame.Rect(WIDTH//2 - ball_radius, HEIGHT//2 - ball_radius, ball_radius*2, ball_radius*2)
ball_speed = [4, 4]
start_time = None

# UI & Field Drawing
def draw_field():
    screen.fill(GREEN)
    pygame.draw.rect(screen, WHITE, (0, 0, WIDTH, HEIGHT), 10)
    pygame.draw.line(screen, WHITE, (WIDTH//2, 0), (WIDTH//2, HEIGHT), 5)
    pygame.draw.circle(screen, WHITE, (WIDTH//2, HEIGHT//2), 80, 5)
    pygame.draw.rect(screen, YELLOW, (0, HEIGHT//2 - goal_height//2, goal_width, goal_height))
    pygame.draw.rect(screen, YELLOW, (WIDTH - goal_width, HEIGHT//2 - goal_height//2, goal_width, goal_height))

def draw_ui():
    draw_field()
    
    # Scoreboard
    name1 = font.render("Ronaldo", True, WHITE)
    name2 = font.render("Messi", True, WHITE)
    score_text = font.render(f"{score1} : {score2}", True, WHITE)
    
    screen.blit(name1, (WIDTH//2 - 150, 20))
    screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, 20))
    screen.blit(name2, (WIDTH//2 + 80, 20))

    elapsed = int(time.time() - start_time)
    remaining = max(0, match_time - elapsed)
    timer_text = font.render(f"Time: {remaining}", True, WHITE)
    screen.blit(timer_text, (WIDTH//2 - timer_text.get_width()//2, HEIGHT - 50))
    return remaining

def reset_positions():
    player1.center = (150, HEIGHT//2)
    player2.center = (WIDTH - 150, HEIGHT//2)
    ball.center = (WIDTH//2, HEIGHT//2)
    ball_speed[0] *= -1
    ball_speed[1] = 4

def show_goal_celebration(player_name):
    draw_field()
    screen.blit(player1_img, player1)
    screen.blit(player2_img, player2)
    pygame.draw.ellipse(screen, WHITE, ball)
    message = f"GOAL by {player_name}!"
    goal_text = big_font.render(message, True, YELLOW)
    screen.blit(goal_text, (WIDTH//2 - goal_text.get_width()//2, HEIGHT//2 - 50))
    pygame.display.flip()
    pygame.time.wait(2000)

def show_winner():
    if score1 > score2:
        winner_text = "Ronaldo Wins!"
    elif score2 > score1:
        winner_text = "Messi Wins!"
    else:
        winner_text = "It's a Draw!"

    draw_field()
    final_text = big_font.render(winner_text, True, WHITE)
    screen.blit(final_text, (WIDTH//2 - final_text.get_width()//2, HEIGHT//2 - 50))
    pygame.display.flip()
    pygame.time.wait(3000)

def show_main_menu():
    while True:
        screen.fill(GREEN)
        title_text = big_font.render("2D Football Game", True, WHITE)
        start_text = font.render("Press SPACE to Start", True, WHITE)
        settings_text = font.render("Press S for Settings", True, WHITE)
        exit_text = font.render("Press ESC to Exit", True, WHITE)

        screen.blit(title_text, (WIDTH//2 - title_text.get_width()//2, HEIGHT//2 - 100))
        screen.blit(start_text, (WIDTH//2 - start_text.get_width()//2, HEIGHT//2 + 20))
        screen.blit(settings_text, (WIDTH//2 - settings_text.get_width()//2, HEIGHT//2 + 60))
        screen.blit(exit_text, (WIDTH//2 - exit_text.get_width()//2, HEIGHT//2 + 100))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return "start"
                elif event.key == pygame.K_s:
                    return "settings"
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

def select_game_mode():
    while True:
        screen.fill(GREEN)
        title_text = big_font.render("Select Game Mode", True, WHITE)
        single_text = font.render("Press 1 for Single Player", True, WHITE)
        two_text = font.render("Press 2 for Two Player", True, WHITE)

        screen.blit(title_text, (WIDTH//2 - title_text.get_width()//2, HEIGHT//2 - 100))
        screen.blit(single_text, (WIDTH//2 - single_text.get_width()//2, HEIGHT//2))
        screen.blit(two_text, (WIDTH//2 - two_text.get_width()//2, HEIGHT//2 + 40))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return "single"
                elif event.key == pygame.K_2:
                    return "two"

def show_settings():
    global match_time, speed
    while True:
        screen.fill(GREEN)
        title_text = big_font.render("Settings", True, WHITE)
        time_text = font.render(f"Game Time: {match_time} secs", True, WHITE)
        difficulty_text = font.render(f"Difficulty: {speed}", True, WHITE)
        back_text = font.render("Press ESC to Go Back", True, WHITE)

        screen.blit(title_text, (WIDTH//2 - title_text.get_width()//2, HEIGHT//2 - 100))
        screen.blit(time_text, (WIDTH//2 - time_text.get_width()//2, HEIGHT//2))
        screen.blit(difficulty_text, (WIDTH//2 - difficulty_text.get_width()//2, HEIGHT//2 + 40))
        screen.blit(back_text, (WIDTH//2 - back_text.get_width()//2, HEIGHT//2 + 80))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                elif event.key == pygame.K_UP:
                    match_time = max(30, match_time - 10)
                    speed = max(3, speed - 1)
                elif event.key == pygame.K_DOWN:
                    match_time = min(180, match_time + 10)
                    speed = min(10, speed + 1)

def show_pause_menu():
    while True:
        screen.fill(GREEN)
        title_text = big_font.render("Game Paused", True, WHITE)
        resume_text = font.render("Press R to Resume", True, WHITE)
        restart_text = font.render("Press P to Restart", True, WHITE)
        exit_text = font.render("Press ESC to Exit", True, WHITE)

        screen.blit(title_text, (WIDTH//2 - title_text.get_width()//2, HEIGHT//2 - 100))
        screen.blit(resume_text, (WIDTH//2 - resume_text.get_width()//2, HEIGHT//2))
        screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2 + 40))
        screen.blit(exit_text, (WIDTH//2 - exit_text.get_width()//2, HEIGHT//2 + 80))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return "resume"
                elif event.key == pygame.K_p:
                    return "restart"
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

def ai_move_and_shoot():
    if player2.centery < ball.centery - 10:
        player2.y += speed - 2
    elif player2.centery > ball.centery + 10:
        player2.y -= speed - 2
    player2.clamp_ip(screen.get_rect())

    if player2.colliderect(ball):
        ball_speed[0] = -shoot_power
        ball_speed[1] = (ball.centery - player2.centery) // 3

# --- Game Start ---
menu_action = show_main_menu()
if menu_action == "settings":
    show_settings()

game_mode = select_game_mode()
start_time = time.time()
running = True

while running:
    remaining_time = draw_ui()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            action = show_pause_menu()
            if action == "restart":
                reset_positions()
                score1 = 0
                score2 = 0
                start_time = time.time()
            elif action == "resume":
                continue

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]: player1.y -= speed
    if keys[pygame.K_s]: player1.y += speed

    if game_mode == "two":
        if keys[pygame.K_UP]: player2.y -= speed
        if keys[pygame.K_DOWN]: player2.y += speed
    else:
        ai_move_and_shoot()

    if keys[pygame.K_SPACE] and player1.colliderect(ball):
        ball_speed[0] = shoot_power
        ball_speed[1] = (ball.centery - player1.centery) // 3

    player1.clamp_ip(screen.get_rect())
    player2.clamp_ip(screen.get_rect())

    # Move and clamp ball
    ball.x += ball_speed[0]
    ball.y += ball_speed[1]

    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_speed[1] *= -1

    if ball.left < 0:
        ball.left = 0
        ball_speed[0] *= -1
    if ball.right > WIDTH:
        ball.right = WIDTH
        ball_speed[0] *= -1

    if ball.colliderect(player1):
        ball_speed[0] = abs(ball_speed[0])
    if ball.colliderect(player2):
        ball_speed[0] = -abs(ball_speed[0])

    # Check goal
    goal_top = HEIGHT // 2 - goal_height // 2
    goal_bottom = HEIGHT // 2 + goal_height // 2

    if ball.left <= goal_width and goal_top < ball.centery < goal_bottom:
        score2 += 1
        show_goal_celebration("Messi")
        reset_positions()

    elif ball.right >= WIDTH - goal_width and goal_top < ball.centery < goal_bottom:
        score1 += 1
        show_goal_celebration("Ronaldo")
        reset_positions()

    screen.blit(player1_img, player1)
    screen.blit(player2_img, player2)
    pygame.draw.ellipse(screen, WHITE, ball)

    if remaining_time <= 0:
        show_winner()
        running = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
