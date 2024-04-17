import pygame
import random
from mapgenerator import generatemaze
pygame.init()
screen = pygame.display.set_mode((600, 600)) #size of the screen
clock = pygame.time.Clock()
running = True
dt = 0
x=1
n_size = 30                     #size of the maze
player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
mouseinbox = False
rounded_corn = 10
speed = 50
bg_map = None
walls_horz,walls_vert,maze_full = generatemaze(n_size)
marked_map = None
charac_name="cat"          #CREDITS DUE SANCHITA
lnk = "img_assets/"+charac_name+".png"
sprite_img = pygame.image.load(lnk).convert_alpha()
bg_tileset = pygame.image.load("img_assets/sheet.png").convert_alpha()
flip_char = False               #is the character facing left?
r_l_is = False                  #is it moving right and left?
u_d_is = False                  #is it moving up and down?
frame_num = 1                   #frame number for the animation
scale = (50,50)                 # a tuple for scaling the character
scalebg = (100,100)
mode = "startmenu"
initpos = (50,50)
running_anim= 'idle'
not_collide=True



def get_image(sheet, start_x,start_y,width, height, scale, colour):
		image = pygame.Surface((width, height)).convert_alpha()
		image.blit(sheet, (0, 0), (start_x, start_y, width, height))
		image = pygame.transform.scale(image, (scale[0], scale[1]))
		image.set_colorkey(colour)

		return image
emote_cat = [None]*9
r_l_cat = [None]*9
bg_tileset_acc = [None]*9

img1_cat = get_image(sprite_img, 8,19,15,15, scale, (0, 0, 0))
#emote keyframes for the cat
emote_cat[1] = get_image(sprite_img, 9, 274, 16, 16, scale, (0, 0, 0))
emote_cat[2] = get_image(sprite_img, 40, 272, 16, 16, scale, (0, 0, 0))
emote_cat[3] = get_image(sprite_img, 72, 271, 16, 16, scale, (0, 0, 0))
emote_cat[4] = get_image(sprite_img, 104, 270, 16, 16, scale, (0, 0, 0))
emote_cat[5] = get_image(sprite_img, 136, 274, 16, 16, scale, (0, 0, 0))
emote_cat[6] = get_image(sprite_img, 168, 276, 16, 16, scale, (0, 0, 0))
emote_cat[7] = get_image(sprite_img, 200, 276, 16, 16, scale, (0, 0, 0))
emote_cat[8] = get_image(sprite_img, 200, 276, 16, 16, scale, (0, 0, 0))
#r/l keyframes of the cat
r_l_cat[1] = get_image(sprite_img,9,178,16,16,scale,(0,0,0))
r_l_cat[2] = get_image(sprite_img,40,178,16,16,scale,(0,0,0))
r_l_cat[3] = get_image(sprite_img,71,178,17,16,scale,(0,0,0))
r_l_cat[4] = get_image(sprite_img,104,178,16,16,scale,(0,0,0))
r_l_cat[5] = get_image(sprite_img,136,178,16,16,scale,(0,0,0))
r_l_cat[6] = get_image(sprite_img,168,178,16,16,scale,(0,0,0))
r_l_cat[7] = get_image(sprite_img,200,178,16,16,scale,(0,0,0))
r_l_cat[8] = get_image(sprite_img,232,178,16,16,scale,(0,0,0))
#bg_tileset reading
bg_tileset_acc[1] = get_image(bg_tileset, 96, 0, 32, 32, scalebg, (0, 0, 0))
bg_tileset_acc[2] = get_image(bg_tileset, 128, 0, 32, 32, scalebg, (0, 0, 0))
bg_tileset_acc[3] = get_image(bg_tileset, 160, 0, 32, 32, scalebg, (0, 0, 0))
bg_tileset_acc[4] = get_image(bg_tileset, 176, 0, 32, 32, scalebg, (0, 0, 0))
bg_tileset_acc[5] = get_image(bg_tileset, 96, 32, 32, 32, scalebg,(0,0,0))
bg_tileset_acc[6] = get_image(bg_tileset, 128, 32, 32, 32, scalebg,(0,0,0))
bg_tileset_acc[7] = get_image(bg_tileset, 160, 32, 32, 32, scalebg, (0, 0, 0))
bg_tileset_acc[8] = get_image(bg_tileset,176,64,32,32,scalebg,(0,0,0))






#to see which type of mode is going on

'''
def r_l_move(screen,player_pos,dt):
    img_copy = r_l_cat[int(frame_num)].copy()
    frame_num += 0.15
    player_pos += pygame.Vector2(1 -2*(int(flip_char)) , 0) * dt * speed *1/10
    if(frame_num >= 9):
        r_l_is = False
        img_copy = img1_cat.copy()
    return img_copy

def u_d_move(screen,player_pos,dt):
    img_copy = emote_cat[int(frame_num)].copy()
    frame_num += 0.15
    player_pos += pygame.Vector2(0, -1) * dt * speed *1/10
    if(frame_num >= 8):
        u_d_is = False
        img_copy = img1_cat.copy()
    return img_copy
'''

	
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
    if key[pygame.K_ESCAPE]:
        running = False
    print("is this running?")
    return player_pos,running


# Function to generate the background , will be changed
def bg_generate(screen ,map_full,n):
    for i in range(len(map_full)):
        for j in range(len(map_full)):
            if map_full[i][j] == map_full[0][0]:
                pygame.draw.rect(screen,(0,255,0),(30*(i)+initpos[0],30*(j)+initpos[1],30,30))
            else:
                pygame.draw.rect(screen,(255,0,0),(30*(i)+initpos[0],30*(j)+initpos[1],30,30))
    for i in range(n):
        for j in range(n-1):
            if walls_horz[i][j] == 1:
                pygame.draw.line(screen,(0,0,0),(30*(i)+initpos[0],30*(j+1)+initpos[1]),(30*(i+1)+initpos[0],30*(j+1)+initpos[1]),2)
    for i in range(n-1):
        for j in range(n):
            if walls_vert[i][j] == 1:
                pygame.draw.line(screen,(0,0,0),(30*(i+1)+initpos[0],30*(j)+initpos[1]),(30*(i+1)+initpos[0],30*(j+1)+initpos[1]),2)
    pygame.draw.circle(screen,(0,0,255),(initpos[0]+30*(n//2)-15,initpos[1]+30*(n//2)-15),10)
    pygame.draw.line(screen,(0,0,0),initpos,(initpos[0]+30*n,initpos[0]),2)
    pygame.draw.line(screen,(0,0,0),(initpos[0]+30*n,initpos[0]+30*n),(initpos[0]+30*n,initpos[0]),2)
    pygame.draw.line(screen,(0,0,0),(initpos[0]+30*n,initpos[0]+30*n),(initpos[0],initpos[0]+30*n),2)
    pygame.draw.line(screen,(0,0,0),initpos,(initpos[0],initpos[0]+30*n),2)



#marking the squares as per the walls and if it is in the main path or not
def mark_squares(map_full,walls_vert,walls_horz):
    marked_map = [['lrud' for i in range(len(map_full)+5)] for j in range(len(map_full)+5)]
    for i in range(len(map_full)):
        for j in range(len(map_full)):
            if map_full[i][j] == map_full[0][0]:
                marked_map[i][j] = str(random.randint(1,8))
                marked_map[i][j] +='i'

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

def generate_current_tiles(marked_map,player_pos):
    current_tiles = []
    x = int((player_pos[0]-initpos[0])/100)
    y = int((player_pos[1]-initpos[1])/100)
    for i in range(-3,4):
        for j in range(-3,4):
            current_tiles.append(marked_map[x+i][y+j])
    return current_tiles

def create_bg(screen,marked_map,player_pos):
    current_tiles = generate_current_tiles(marked_map,player_pos)
    player_x = int((player_pos[0]-initpos[0])/100)
    player_y = int((player_pos[1]-initpos[1])/100)
    if 'i' not in marked_map[player_x][player_y]:
        if running_anim == 'r_l':
            player_pos[0] -= 30 * (1 -2*(int(flip_char)))
        elif running_anim == 'u_d':
            player_pos[1] -= 30 * u_d
    for x in range(len(current_tiles)):
        i = x//7
        j = x%7 
        if 'i' in current_tiles[x]:
            img_now = bg_tileset_acc[int(current_tiles[x][0])]
            screen.blit(img_now,(i*100 + 50-((player_pos[0]-initpos[0])%100), j*100+50-((player_pos[1]-initpos[1])%100)))


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    match mode:
        case "startmenu":
            screen.fill("black")
            font = pygame.font.Font(None, 74)
            text = font.render("Start Menu", True, "white")
            text_rect = text.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2))
            screen.blit(text, text_rect)
            start_butt = pygame.draw.rect(screen,"white", (screen.get_width() / 2 - 60, screen.get_height() / 2 + 100, 120, 50),0,rounded_corn,rounded_corn,rounded_corn,rounded_corn)
            if(start_butt.collidepoint(pygame.mouse.get_pos())):
                pygame.draw.rect(screen,"grey", (screen.get_width() / 2 - 70, screen.get_height() / 2 + 95, 140, 60),0,rounded_corn,rounded_corn,rounded_corn,rounded_corn)
                mouseinbox = True
            else:
                mouseinbox = False
            font = pygame.font.Font(None, 30)
            text = font.render("Start", True, "black")
            text_rect = text.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2 + 120))
            screen.blit(text,text_rect)
            pygame.display.flip()
            dt = clock.tick(60) / 100
            if mouseinbox and pygame.mouse.get_pressed()[0]:
                mode = "gameon"
                walls_horz,walls_vert,maze_full = generatemaze(n_size)
                marked_map = mark_squares(maze_full,walls_vert,walls_horz)
                maze_img = pygame.display.set_mode((1020, 1020))
                maze_img.fill("gray")
                bg_generate(maze_img,maze_full,30)
                pygame.image.save(maze_img,"maze.png")
                screen = pygame.display.set_mode((600, 800))
                print("start")

        case "gameon":
            screen.fill("gray")
            #bg_generate(30)
            create_bg(screen,marked_map,player_pos)
            if not_collide:
                if r_l_is:
                    if pygame.key.get_pressed()[pygame.K_a]:
                        flip_char = True
                    elif pygame.key.get_pressed()[pygame.K_d]:
                        flip_char = False
                    player_pos += pygame.Vector2(1 -2*(int(flip_char)) , 0) * dt * speed *1/10
                    if(frame_num >= 9):
                        r_l_is = False
                        running_anim = 'idle'
                        img_copy = img1_cat.copy()
                    else:
                        img_copy = r_l_cat[int(frame_num)].copy()
                        frame_num += 0.25
                
                elif u_d_is:
                    
                    if pygame.key.get_pressed()[pygame.K_s]:
                        u_d =1
                    if pygame.key.get_pressed()[pygame.K_w]:
                        u_d = -1
                    player_pos += pygame.Vector2(0, u_d) * dt * speed *1/10
                    if(frame_num >= 9):
                        u_d_is = False
                        running_anim='idle'
                        img_copy = img1_cat.copy()
                    else:
                        img_copy = emote_cat[int(frame_num)].copy()
                        frame_num += 0.25
                else:    
                    #key = pygame.key.get_pressed()
                    #player_pos,running = move(screen,player_pos,dt,running,key)
                    img_copy = img1_cat.copy()
                img_with_flip = pygame.transform.flip(img_copy, flip_char, False).convert_alpha()
                screen.blit(img_with_flip, pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2))
                if not (u_d_is or r_l_is):
                    if(pygame.key.get_pressed()[pygame.K_a] or pygame.key.get_pressed()[pygame.K_d] and (running_anim == 'idle') and (not (pygame.key.get_pressed()[pygame.K_s] or pygame.key.get_pressed()[pygame.K_w]))):
                        r_l_is = True
                        running_anim = 'r_l'
                        if frame_num >=9:
                            frame_num = 1
                    elif(pygame.key.get_pressed()[pygame.K_s] or pygame.key.get_pressed()[pygame.K_w]):
                        if not r_l_is:
                            u_d_is = True
                            running_anim = 'u_d'
                        if frame_num >= 9:
                            frame_num = 1
            else:
                #will write now
                frame_num = 1
                u_d_is = False
                r_l_is = False
                running_anim = 'idle'
                img_copy = img1_cat.copy()
                img_with_flip = pygame.transform.flip(img_copy, flip_char, False).convert_alpha()
                screen.blit(img_with_flip, pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2))

                continue
            pygame.draw.rect(screen,"black",(0,600,600,200))
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
                player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
                walls_horz,walls_vert,maze_full = generatemaze(n_size)
                marked_map = mark_squares(maze_full,walls_vert,walls_horz)
                maze_img = pygame.display.set_mode((1020, 1020))
                maze_img.fill("gray")
                bg_generate(maze_img,maze_full,30)
                pygame.image.save(maze_img,"maze.png")
                screen = pygame.display.set_mode((600, 800))
                print("restart")
    if pygame.key.get_pressed()[pygame.K_SPACE]:
        mode = "gameover"
        print("gameover")
pygame.quit()


