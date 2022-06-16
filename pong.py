import pygame
from pygame import key
from pygame.locals import *
import random

from pygame.mixer import pause


WIDTH, HEIGH = 900, 600
WINDOW = pygame.display.set_mode((WIDTH, HEIGH))
pygame.display.set_caption("Pong")
pygame.mouse.set_visible(False)
pygame.font.init()
pygame.mixer.init()

FPS = 60
VEL = 10
PAD_HEIGH = 80
PAD_WIDTH = 10

BALL_RAD = 5

BALL_VEL = 7

(GREY) = (16, 18, 36)
(WHITE) = (255, 255, 255)
(GREEN) = (50, 255, 50)

bounce = pygame.mixer.Sound('Assets/bounce.wav')
lost_round = pygame.mixer.Sound('Assets/lost.wav')

font = pygame.font.SysFont('Courier NEw', 60)
START_TEXT = font.render("Press SPACE to start", False, GREEN)

l_posX = 5
l_posY = (HEIGH // 2) - (PAD_HEIGH // 2)

r_posX = (WIDTH - 5) - PAD_WIDTH
r_posY = (HEIGH // 2) - (PAD_HEIGH // 2)

BORDER = pygame.Rect(WIDTH // 2 - 5, 0, 10, HEIGH)
L_PAD = pygame.Rect(l_posX, l_posY, PAD_WIDTH, PAD_HEIGH)
R_PAD = pygame.Rect(r_posX, r_posY, PAD_WIDTH, PAD_HEIGH)



def handle_movement(L_PAD, R_PAD, keys_pressed):
    if keys_pressed[pygame.K_w] and L_PAD.y + VEL > 0:
        L_PAD.y -= VEL
    if keys_pressed[pygame.K_s] and L_PAD.y + PAD_HEIGH < HEIGH:
        L_PAD.y += VEL
    if keys_pressed[pygame.K_UP] and R_PAD.y + VEL > 0:
        R_PAD.y -= VEL
    if keys_pressed[pygame.K_DOWN] and R_PAD.y + PAD_HEIGH < HEIGH:
        R_PAD.y += VEL
    

def draw_window(ball_X, ball_Y, paused, l_score, r_score):
    WINDOW.fill(GREY)
    pygame.draw.rect(WINDOW, WHITE, BORDER)
    pygame.draw.rect(WINDOW, WHITE, L_PAD)
    pygame.draw.rect(WINDOW, WHITE, R_PAD)
    pygame.draw.circle(WINDOW, WHITE, (ball_X, ball_Y), BALL_RAD)
    if paused:
        WINDOW.blit(START_TEXT,(120, HEIGH//2 - 60 )) 

    l_score_text = font.render(l_score, False, WHITE)
    r_score_text = font.render(r_score, False, WHITE)

    WINDOW.blit(l_score_text,(10, 10 )) 
    WINDOW.blit(r_score_text,(WIDTH - 50, 10 )) 
    pygame.display.update()

 
def main():
    ball_X = WIDTH // 2
    ball_Y = HEIGH // 2
    dir_X = random.choice((-1, 1))
    dir_Y = random.choice((-1, 1))

    L_SCORE = 0
    R_SCORE = 0

    clock = pygame.time.Clock()
    run = True
    paused = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == QUIT:
                run = False

        if ball_X - BALL_RAD // 2 < 0:
            R_SCORE += 1
            ball_X = WIDTH // 2
            ball_Y = HEIGH // 2
            pygame.mixer.Sound.play(lost_round)
            pygame.time.wait(2000)
        if ball_X + BALL_RAD // 2 > WIDTH:
            L_SCORE += 1
            ball_X = WIDTH // 2
            ball_Y = HEIGH // 2
            pygame.mixer.Sound.play(lost_round)
            pygame.time.wait(2000)
        if ball_Y - BALL_RAD // 2 < 0 or ball_Y + BALL_RAD // 2 > HEIGH:
             dir_Y *= (-1)
             pygame.mixer.Sound.play(bounce)
        if ball_X - BALL_RAD // 2 < L_PAD.x + PAD_WIDTH and ball_Y in range(L_PAD.y, L_PAD.y + PAD_HEIGH):
            dir_X *= (-1)
            pygame.mixer.Sound.play(bounce)
        if ball_X + BALL_RAD // 2 > R_PAD.x and ball_Y in range(R_PAD.y, R_PAD.y + PAD_HEIGH):
            dir_X *= (-1)
            pygame.mixer.Sound.play(bounce)

        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_SPACE] and paused:
            paused = False
        if keys_pressed[pygame.K_ESCAPE]:
            run = False
        
        if not paused:
            handle_movement(L_PAD, R_PAD, keys_pressed)
            ball_X += dir_X * BALL_VEL
            ball_Y += dir_Y * BALL_VEL


        draw_window(ball_X, ball_Y, paused, str(L_SCORE), str(R_SCORE))
    pygame.quit()

if __name__ == "__main__":
    main()