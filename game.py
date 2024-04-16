import pygame
import random
from mapgenerator import generatemaze
pygame.init()
screen = pygame.display.set_mode((900, 900))
clock = pygame.time.Clock()
running = True
dt = 0
x=1
n_size = 30
player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
mouseinbox = False
rounded_corn = 10
speed = 50
bg_map = None
walls_horz,walls_vert,maze_full = generatemaze(n_size)

#to see which type of mode is going on
mode = "gameon"
# Function to move the player
def move(screen,player_pos,dt,running,key):
    if (key[pygame.K_LEFT] or key[pygame.K_a]) and player_pos.x>=0:
        player_pos += pygame.Vector2(-1, 0) * dt * speed
    if (key[pygame.K_RIGHT] or key[pygame.K_d]) and player_pos.x<=screen.get_width():
        player_pos += pygame.Vector2(1, 0) * dt * speed
    if (key[pygame.K_UP] or key[pygame.K_w]) and player_pos.y>=0:
        player_pos += pygame.Vector2(0, -1) * dt * speed
    if (key[pygame.K_DOWN] or key[pygame.K_s]) and player_pos.y<=screen.get_height():
        player_pos += pygame.Vector2(0, 1) * dt * speed
    if key[pygame.K_ESCAPE]:
        running = False
    return player_pos,running

def bg_generate(n):
    for i in range(n):
        for j in range(n-1):
            if walls_horz[i][j] == 1:
                pygame.draw.line(screen,(0,0,0),(30*(i),30*(j+1)),(30*(i+1),30*(j+1)),2)
    for i in range(n-1):
        for j in range(n):
            if walls_vert[i][j] == 1:
                pygame.draw.line(screen,(0,0,0),(30*(i+1),30*(j)),(30*(i+1),30*(j+1)),2)



while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    match mode:
        case "gameon":
            screen.fill("purple")
            bg_generate(30)
            key = pygame.key.get_pressed()
            player_pos,running = move(screen,player_pos,dt,running,key)
            pygame.draw.rect(screen, "red", (player_pos.x, player_pos.y, 25, 25))
            pygame.display.flip()
            dt = clock.tick(60) / 100
        case "gameover":
            screen.fill("black")
            font = pygame.font.Font(None, 74)
            text = font.render("Game Over", True, "white")
            text_rect = text.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2))
            screen.blit(text, text_rect)
            restart_butt = pygame.draw.rect(screen,"white", (screen.get_width() / 2 - 60, screen.get_height() / 2 + 100, 120, 50),0,rounded_corn,rounded_corn,rounded_corn,rounded_corn)
            if(restart_butt.collidepoint(pygame.mouse.get_pos())):
                pygame.draw.rect(screen,"grey", (screen.get_width() / 2 - 70, screen.get_height() / 2 + 95, 140, 60),0,rounded_corn,rounded_corn,rounded_corn,rounded_corn)
                mouseinbox = True
            else:
                mouseinbox = False
            font = pygame.font.Font(None, 30)
            text = font.render("Restart", True, "black")
            text_rect = text.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2 + 120))
            screen.blit(text,text_rect)
            pygame.display.flip()
            dt = clock.tick(60) / 100
            if mouseinbox and pygame.mouse.get_pressed()[0]:
                mode = "gameon"
                walls_horz,walls_vert = generatemaze(n_size)
                print("restart")
    if pygame.key.get_pressed()[pygame.K_SPACE]:
        mode = "gameover"
        print("gameover")
pygame.quit()


