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
charac_name="cat"
lnk = "img_assets/"+charac_name+".png"
sprite_img = pygame.image.load(lnk).convert_alpha()
flip_char = False
emote_yes = False
frame_num = 1
scale = 3



def get_image(sheet, start_x,start_y,width, height, scale, colour):
		image = pygame.Surface((width, height)).convert_alpha()
		image.blit(sheet, (0, 0), (start_x, start_y, width, height))
		image = pygame.transform.scale(image, (width * scale, height * scale))
		image.set_colorkey(colour)

		return image
emote_cat = [None]*8
r_l_cat = [None]*9

img1_cat = get_image(sprite_img, 8,19,15,15, scale, (0, 0, 0))
#emote keyframes for the cat
emote_cat[1] = get_image(sprite_img, 9, 274, 16, 16, scale, (0, 0, 0))
emote_cat[2] = get_image(sprite_img, 40, 272, 16, 16, scale, (0, 0, 0))
emote_cat[3] = get_image(sprite_img, 72, 271, 16, 16, scale, (0, 0, 0))
emote_cat[4] = get_image(sprite_img, 104, 270, 16, 16, scale, (0, 0, 0))
emote_cat[5] = get_image(sprite_img, 136, 274, 16, 16, scale, (0, 0, 0))
emote_cat[6] = get_image(sprite_img, 168, 276, 16, 16, scale, (0, 0, 0))
emote_cat[7] = get_image(sprite_img, 200, 276, 16, 16, scale, (0, 0, 0))
#r/l keyframes of the cat
r_l_cat[1] = get_image(sprite_img,9,178,16,16,scale,(0,0,0))
r_l_cat[2] = get_image(sprite_img,40,178,16,16,scale,(0,0,0))
r_l_cat[3] = get_image(sprite_img,71,178,17,16,scale,(0,0,0))
r_l_cat[4] = get_image(sprite_img,104,178,16,16,scale,(0,0,0))
r_l_cat[5] = get_image(sprite_img,136,178,16,16,scale,(0,0,0))
r_l_cat[6] = get_image(sprite_img,168,178,16,16,scale,(0,0,0))
r_l_cat[7] = get_image(sprite_img,200,178,16,16,scale,(0,0,0))
r_l_cat[8] = get_image(sprite_img,232,178,16,16,scale,(0,0,0))

#to see which type of mode is going on
mode = "gameon"

def r_l_move(screen,player_pos,dt):
    img_copy = r_l_cat[int(frame_num)].copy()
    frame_num += 0.15
    player_pos += pygame.Vector2(1 -2*(int(flip_char)) , 0) * dt * speed *1/10
    if(frame_num >= 9):
        emote_yes = False
        img_copy = img1_cat.copy()
    return img_copy

def u_d_move(screen,player_pos,dt):
    img_copy = emote_cat[int(frame_num)].copy()
    frame_num += 0.15
    player_pos += pygame.Vector2(0, -1) * dt * speed *1/10
    if(frame_num >= 8):
        emote_yes = False
        img_copy = img1_cat.copy()
    return img_copy


#will be changed
# Function to move the player
def move(screen,player_pos,dt,running,key):
    global flip_char
    state=''
    if (key[pygame.K_LEFT] or key[pygame.K_a]) and player_pos.x>=0:
        player_pos += pygame.Vector2(-1, 0) * dt * speed
        flip_char = True
        state += 'l'
    if (key[pygame.K_RIGHT] or key[pygame.K_d]) and player_pos.x<=screen.get_width():
        player_pos += pygame.Vector2(1, 0) * dt * speed
        flip_char = False
        state += 'r'
    if (key[pygame.K_UP] or key[pygame.K_w]) and player_pos.y>=0:
        player_pos += pygame.Vector2(0, -1) * dt * speed
        state += 'u'
    if (key[pygame.K_DOWN] or key[pygame.K_s]) and player_pos.y<=screen.get_height():
        player_pos += pygame.Vector2(0, 1) * dt * speed
        state += 'd'
    if (key[pygame.K_e]):
        state += 'e'
    if key[pygame.K_ESCAPE]:
        running = False
    return player_pos,running,state


# Function to generate the background
def bg_generate(n):
    for i in range(n):
        for j in range(n-1):
            if walls_horz[i][j] == 1:
                pygame.draw.line(screen,(0,0,0),(30*(i),30*(j+1)),(30*(i+1),30*(j+1)),2)
    for i in range(n-1):
        for j in range(n):
            if walls_vert[i][j] == 1:
                pygame.draw.line(screen,(0,0,0),(30*(i+1),30*(j)),(30*(i+1),30*(j+1)),2)

#marking the squares as per the walls and if it is in the main path or not
def mark_squares(map_full,walls_vert,walls_horz):
    marked_map = [[0 for i in range(len(map_full))] for j in range(len(map_full))]
    for i in range(len(map_full)):
        for j in range(len(map_full)):
            if map_full[i][j] == map_full[0][0]:
                marked_map[i][j] = 'i'
            else:
                marked_map[i][j] = ''
            if i>0 and walls_vert[i-1][j] == 0:
                marked_map[i][j] += 'l'
            if i<len(map_full)-1 and walls_vert[i][j] == 0:
                marked_map[i][j] += 'r'
            if j>0 and walls_horz[i][j-1] == 0:
                marked_map[i][j] += 'u'
            if j<len(map_full)-1 and walls_horz[i][j] == 0:
                marked_map[i][j] += 'd'
            if i==0:
                marked_map[i][j] += 'u'
            if i==len(map_full)-1:
                marked_map[i][j] += 'd'
            if j==0:
                marked_map[i][j] += 'l'
            if j==len(map_full)-1:
                marked_map[i][j] += 'r'
    return marked_map




while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    match mode:
        case "gameon":
            screen.fill("gray")
            bg_generate(30)
            player_pos,running,state = move(screen,player_pos,dt,running,key)
            if 'e' in state:
                img_copy = r_l_cat[int(frame_num)].copy()
                frame_num += 0.15
                player_pos += pygame.Vector2(1 -2*(int(flip_char)) , 0) * dt * speed *1/10
                if(frame_num >= 9):
                    emote_yes = False
                    img_copy = img1_cat.copy()
            else:    
                key = pygame.key.get_pressed()
                player_pos,running = move(screen,player_pos,dt,running,key)
                img_copy = img1_cat.copy()
            img_with_flip = pygame.transform.flip(img_copy, flip_char, False).convert_alpha()
            screen.blit(img_with_flip, player_pos)
            if(pygame.key.get_pressed()[pygame.K_e]):
                emote_yes = True
                frame_num = 1
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
                walls_horz,walls_vert,maze_full = generatemaze(n_size)
                print("restart")
    if pygame.key.get_pressed()[pygame.K_SPACE]:
        mode = "gameover"
        print("gameover")
pygame.quit()


