import pygame
import random
import time
from math import floor
from mapgenerator import generatemaze
from map_gen_wilson import WilsonMazeGenerator
pygame.init()
screensize = (1200,800)
screen = pygame.display.set_mode(screensize) #size of the screen
pygame.display.set_caption("Maze Game")
clock = pygame.time.Clock()
running = True
dt = 0
x=1
n_size = 30                     #size of the maze
player_pos = pygame.Vector2(screen.get_width() / 2 -300, screen.get_height() / 2 -300)
mouseinbox = False
rounded_corn = 10
speed = 2000
frame_speed = 0.3
bg_map = None
walls_horz,walls_vert,maze_full = None,None,None 
marked_map = None
charac_name="cat"          #CREDITS DUE SANCHITA
lnk = "img_assets/"+charac_name+".png"
sprite_img = pygame.image.load(lnk).convert_alpha()
bg_tileset = pygame.image.load("img_assets/sheet.png").convert_alpha()
main_bg = pygame.image.load("img_assets/catbg1.jpg")
opt_bg = pygame.image.load('img_assets/optbg.png')
high_bg = pygame.image.load('img_assets/highbg.jpg')
milk = pygame.image.load('img_assets/milk.png').convert_alpha()
time_im = pygame.image.load('img_assets/time.png').convert_alpha()
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
u_d = 0
mousedown = False
time_tot = 240
flag = 'not hi'
max_time=240
music = './music_cat.mp3'
score = 0
collectable_score=300
timefac = 5
count_coll = 0
pygame.mixer.init()
pygame.mixer.music.load(music)
pygame.mixer.music.play(-1)
NDEBUG = True
path_file = "./path.txt"
highscore_file = './highscore.txt'
score_list = {"e":[],"m":[],"h":[]}

set1 = True
if set1:
    leftkey = pygame.K_a
    rightkey = pygame.K_d
    upkey = pygame.K_w
    downkey = pygame.K_s
else:
    leftkey = pygame.K_LEFT
    rightkey = pygame.K_RIGHT
    upkey = pygame.K_UP
    downkey = pygame.K_DOWN






def get_image(sheet, start_x,start_y,width, height, scale, colour):
		image = pygame.Surface((width, height)).convert_alpha()
		image.blit(sheet, (0, 0), (start_x, start_y, width, height))
		image = pygame.transform.scale(image, (scale[0], scale[1]))
		image.set_colorkey(colour)
		return image
emote_cat = [None]*9
r_l_cat = [None]*9
bg_tileset_acc = [None]*9
img_celeb = [None]*9

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
#celebration keyframes of cat
#img_celeb[1] = get_image(sprite_img,10,303,16,16,scale,(0,0,0))
#img_celeb[2] = get_image(sprite_img,40,303,16,16,scale,(0,0,0))
#img_celeb[3] = get_image(sprite_img,72,303,16,16,scale,(0,0,0))
#img_celeb[4] = get_image(sprite_img,104,303,16,16,scale,(0,0,0))
img_celeb[1] = get_image(sprite_img,8,209,16,16,scale,(0,0,0))
img_celeb[2] = get_image(sprite_img,40,209,16,16,scale,(0,0,0))
img_celeb[3] = get_image(sprite_img,72,209,16,16,scale,(0,0,0))
img_celeb[4] = get_image(sprite_img,104,209,16,16,scale,(0,0,0))

img_celeb[5] = get_image(sprite_img,135,303,17,16,scale,(0,0,0))
img_celeb[6] = get_image(sprite_img,167,303,17,16,scale,(0,0,0))
img_celeb[7] = get_image(sprite_img,200,303,16,16,scale,(0,0,0))
img_celeb[8] = get_image(sprite_img,232,303,16,16,scale,(0,0,0))




#bg_tileset reading
bg_tileset_acc[1] = get_image(bg_tileset, 96, 0, 32, 32, scalebg, (0, 0, 0))
bg_tileset_acc[2] = get_image(bg_tileset, 128, 0, 32, 32, scalebg, (0, 0, 0))
bg_tileset_acc[3] = get_image(bg_tileset, 160, 0, 32, 32, scalebg, (0, 0, 0))
bg_tileset_acc[4] = get_image(bg_tileset, 176, 0, 32, 32, scalebg, (0, 0, 0))
bg_tileset_acc[5] = get_image(bg_tileset, 96, 32, 32, 32, scalebg,(0,0,0))
bg_tileset_acc[6] = get_image(bg_tileset, 128, 32, 32, 32, scalebg,(0,0,0))
bg_tileset_acc[7] = get_image(bg_tileset, 160, 32, 32, 32, scalebg, (0, 0, 0))
bg_tileset_acc[8] = get_image(bg_tileset,176,64,32,32,scalebg,(0,0,0))

bg_rest = get_image(bg_tileset, 2, 2, 44, 44, scalebg, (0, 0, 0))
bg_rest = get_image(bg_tileset, 98, 82, 28, 28, scalebg, (0, 0, 0))
bg_start = get_image(bg_tileset, 176, 96, 32, 32, scalebg, (0, 0, 0))
bg_end = get_image(bg_tileset, 176, 128, 32, 32, scalebg, (0, 0, 0))

main_img_backg = get_image(main_bg,120,25,1200,800,screensize,(0,0,0))
opt_img_bg = get_image(opt_bg,0,0,1087,605,screensize,(0,0,0))
high_img_bg = get_image(high_bg,33,2,1313,891,screensize,(0,0,0))

milk_img = get_image(milk,450,550,1000,1000,(50,50),(0,0,0))
time_img = get_image(time_im,125,0,600,850,(50,50),(0,0,0))
#to see which type of mode is going on
def generate_current_tiles(marked_map,player_pos):
    current_tiles = []
    global mode
    x = int((player_pos[0]-initpos[0])/100)
    y = int((player_pos[1]-initpos[1])/100)
    if 'z' in marked_map[x][y] and mode!='winscreen':
        mode='winscreen'
        global score, timefac, time_tot,score_list,highscore_file
        score = score + int(timefac*time_tot)
        score_list = get_score(highscore_file)
        if n_size == 20:
            score_list["e"].append(score)
            score_list["e"].sort(reverse=True)
            if len(score_list["e"])>5:
                score_list["e"] = score_list["e"][:5]
        elif n_size == 40:
            score_list["m"].append(score)
            score_list["m"].sort(reverse=True)
            if len(score_list["m"])>5:
                score_list["m"] = score_list["m"][:5]
        elif n_size == 60:
            score_list["h"].append(score)
            score_list["h"].sort(reverse=True)
            if len(score_list["h"])>5:
                score_list["h"] = score_list["h"][:5]
        write_score(highscore_file,score_list)

    for i in range(-4,5):
        for j in range(-4,5):
            current_tiles.append(marked_map[x+i][y+j])
    return current_tiles

def create_bg(screen,marked_map,player_pos):
    global frame_num , running_anim , r_l_is , u_d_is
    current_tiles = generate_current_tiles(marked_map,player_pos)
    if running_anim == 'r_l':
        if flip_char:
            player_x = floor((player_pos[0]-initpos[0]-40)/100)
        else:
            player_x = floor((player_pos[0]-initpos[0]+40)/100)
        player_y = floor((player_pos[1]-initpos[1])/100)
    elif running_anim == 'u_d':
        player_x = floor((player_pos[0]-initpos[0])/100)
        if u_d == 1:
            player_y = floor((player_pos[1]-initpos[1]+40)/100)
        else:
            player_y = floor((player_pos[1]-initpos[1]-40)/100)
    else:
        player_x = floor((player_pos[0]-initpos[0])/100)
        player_y = floor((player_pos[1]-initpos[1])/100)
    #print(player_x,player_y,player_pos)
    #collisions here
    if NDEBUG: 
        if 'i' not in marked_map[player_x][player_y]:
            if running_anim == 'r_l':
                player_pos[0] -= speed/100 * (1 -2*(int(flip_char)))
                running_anim = 'idle'
                frame_num = 1
                r_l_is = False
            elif running_anim == 'u_d':
                player_pos[1] -= speed/100 * u_d
                running_anim = 'idle'
                frame_num = 1
                u_d_is = False
    if 'c' in marked_map[player_x][player_y]:
        marked_map[player_x][player_y] = marked_map[player_x][player_y][0:2]
        global score
        score += collectable_score
    if 't' in marked_map[player_x][player_y]:
        global time_tot
        time_tot += 15
        marked_map[player_x][player_y] = marked_map[player_x][player_y][0:2]

    
    
    for x in range(len(current_tiles)):
        i = x//9
        j = x%9 
        if 'i' in current_tiles[x]:
            val = int(current_tiles[x][0])
            img_now = bg_tileset_acc[val]
            if 'q' in current_tiles[x]:
                img_now = bg_start
            if 'z' in current_tiles[x]:
                img_now = bg_end
            screen.blit(img_now,(i*100 -25+ 50-((player_pos[0]-initpos[0])%100), j*100-25+50-((player_pos[1]-initpos[1])%100)))
            if 'c' in current_tiles[x]:
                screen.blit(milk_img,(i*100+50-((player_pos[0]-initpos[0])%100), j*100+50-((player_pos[1]-initpos[1])%100)))
            if 't' in current_tiles[x]:
                screen.blit(time_img,(i*100+50-((player_pos[0]-initpos[0])%100), j*100+50-((player_pos[1]-initpos[1])%100)))
        else:
            screen.blit(bg_rest,(i*100 -25+ 50-((player_pos[0]-initpos[0])%100), j*100-25+50-((player_pos[1]-initpos[1])%100)))
            
    return

def get_score(file):
    score_list = {"e":[],"m":[],"h":[]}
    with open(file,"r") as f:
        for line in f:
            if line[0] == 'e':
                score_list["e"].append(int(line[1:]))
            elif line[0] == 'm':
                score_list["m"].append(int(line[1:]))
            elif line[0] == 'h':
                score_list["h"].append(int(line[1:]))
    return score_list

def write_score(file,score_list):
    with open(file,"w") as f:
        for i in range(len(score_list["e"])):
            f.write(f"e{score_list['e'][i]}\n")
        for i in range(len(score_list["m"])):
            f.write(f"m{score_list['m'][i]}\n")
        for i in range(len(score_list["h"])):
            f.write(f"h{score_list['h'][i]}\n")
    return



def bg_generate_2(screen,marked_map):
    for i in range(len(marked_map)):
        for j in range(len(marked_map)):
            if 'i' in marked_map[i][j]:
                pygame.draw.rect(screen,(0,255,0),(20*(i)+10,20*(j)+10,20,20))
            else:
                pygame.draw.rect(screen,(255,0,0),(20*(i)+10,20*(j)+10,20,20))
            if 'q' in marked_map[i][j]:
                pygame.draw.circle(screen,(0,0,255),(20*(i)+20,20*(j)+20),10)
            if 'z' in marked_map[i][j]:
                pygame.draw.circle(screen,(0,0,255),(20*(i)+20,20*(j)+20),10)
            if 'c' in marked_map[i][j]:
                pygame.draw.circle(screen,(255,255,0),(20*(i)+20,20*(j)+20),10)
            if 't' in marked_map[i][j]:
                pygame.draw.circle(screen,(0,255,255),(20*(i)+20,20*(j)+20),10)
                
    pygame.draw.line(screen,(0,0,0),(10,10),(10+20*len(marked_map),10),2)
    pygame.draw.line(screen,(0,0,0),(10+20*len(marked_map),10+20*len(marked_map)),(10+20*len(marked_map),10),2)
    pygame.draw.line(screen,(0,0,0),(10+20*len(marked_map),10+20*len(marked_map)),(10,10+20*len(marked_map)),2)
    pygame.draw.line(screen,(0,0,0),(10,10),(10,10+20*len(marked_map)),2)


def mask(screen,time,time_tot):
    # Define the radius and color for the visible circle
    visible_circle_radius = 400*(time/time_tot)
    #visible_circle_color = (0, 0, 0)  # White color for visibility circle

    mask_surface = pygame.Surface((800, 800), pygame.SRCALPHA)  # Use SRCALPHA for transparency
    if time_tot - time > 0:
        mask_color = (0, 0, 0, time_tot - time)  # Semi-ransparent black (adjust alpha as needed)cls
    else:
        mask_color=(0,0,0,0)

    # Clear the mask surface with semi-transparent black
    mask_surface.fill(mask_color)


    # Draw the visible circle on the mask surface (fully transparent inside circle, opaque outside)
    pygame.draw.circle(mask_surface, (0, 0, 0, 0), (400+25,25+screen.get_width()/2), visible_circle_radius)
    
    # Blit the mask surface onto the game screen with the correct blending mode
    screen.blit(mask_surface, (0, 0))
    
    
    return


######## wilson maze renderer ########
def wilson_maze(n_size):
    maze = WilsonMazeGenerator(n_size,n_size)
    maze.generate_maze()
    maze.solve_maze()
    solution = maze.solution
    path =[]
    for i in range(len(solution)-1):
        if(solution[i][0] == solution[i+1][0]):
            if solution[i][1] < solution[i+1][1]:
                path.append('right ')
            else:
                path.append('left ')
        else:
            if solution[i][0] < solution[i+1][0]:
                path.append('up ')
            else:
                path.append('down ')
    maze.show_solution(True)
    path = path[::-1]
    with open(path_file,"w") as file:
        file.write("Path to the solution :\n")
        for x in range(len(path)):
            file.write(path[x] + '\n')
    marked_map = [['' for i in range(n_size +9)] for j in range(n_size +9)]
    global count_coll
    count_coll = 0
    for i in range(n_size +1):
        for j in range(n_size +1):
            if maze.grid[j][n_size -i] != 0:
                marked_map[i][j] = str(random.randint(1,8))
                marked_map[i][j] += 'i'
                temp = random.random()*100
                if temp < 4 and (i!=0 and j!=0) and (i!=n_size and j!=n_size):
                        marked_map[i][j] += "c"
                        count_coll += 1
                elif temp > 99   and (i!=0 and j!=0) and (i!=n_size and j!=n_size):
                        marked_map[i][j] += "t"
    marked_map[0][0] += 'q'
    marked_map[n_size][n_size] += 'z'
    
    
    return marked_map, solution


while running:
    total_min = time_tot//60
    total_sec = time_tot%60
    total_min = int(total_min)
    total_sec = int(total_sec)
    if mode == "gameon1":
        time_tot -= dt
    if mode == "gameon2":
        time_tot -= dt
    time_strng = f"{total_min}:{total_sec}" if total_sec>=10 else f"{total_min}:0{total_sec}"
    if time_tot <= 0:
        mode = "gameover"
        screen = pygame.display.set_mode(screensize)
        pygame.mixer.music.stop()
    mousedown = False
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mousedown = True
        if event.type == pygame.MOUSEBUTTONUP:
            mousedown = False
        if event.type ==pygame.KEYDOWN:
            ##cheats##
                if event.key == pygame.K_m:
                    NDEBUG = False
                elif event.key == pygame.K_n:
                    NDEBUG = True
            ##########

    match mode:
        case "startmenu":
            if set1:
                leftkey = pygame.K_a
                rightkey = pygame.K_d
                upkey = pygame.K_w
                downkey = pygame.K_s
            else:
                leftkey = pygame.K_LEFT
                rightkey = pygame.K_RIGHT
                upkey = pygame.K_UP
                downkey = pygame.K_DOWN
            #print(flag)
            NDEBUG= True
            score = 0
            screen.fill("black")
            screen.blit(main_img_backg,(0,0))
            font = pygame.font.Font(None, 110)
            font2= pygame.font.Font(None,112)
            text = font.render("Start Menu", True, "turquoise")
            text2 = font2.render("Start Menu",True,"black")
            text_rect2 = text.get_rect(center=(screen.get_width() / 2-5, screen.get_height() / 2 - 300))
            text_rect = text.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2 - 300))
            screen.blit(text2,text_rect2)
            screen.blit(text, text_rect)
            
            #options button
            option_butt = pygame.draw.rect(screen, "white" , (screen.get_width() / 2 - 60, screen.get_height() / 2, 120, 50),0,rounded_corn,rounded_corn,rounded_corn,rounded_corn)
            if(option_butt.collidepoint(pygame.mouse.get_pos())):
                pygame.draw.rect(screen,"grey", (screen.get_width() / 2 - 70, screen.get_height() / 2 -5, 140, 60),0,rounded_corn,rounded_corn,rounded_corn,rounded_corn)
                mouseinoptbx = True
            else:
                mouseinoptbx = False
            font = pygame.font.Font(None, 30)
            text = font.render("Options",True,"black")
            text_opt = text.get_rect(center=(screen.get_width()/2 , screen.get_height()/2+25))
            screen.blit(text,text_opt)
            
            
            #level 1 button
            level1_butt = pygame.draw.rect(screen,"white", (screen.get_width() / 2 - 280, screen.get_height() / 2 + 100, 120, 50),0,rounded_corn,rounded_corn,rounded_corn,rounded_corn)
            if(level1_butt.collidepoint(pygame.mouse.get_pos())):
                pygame.draw.rect(screen,"grey", (screen.get_width() / 2 - 290, screen.get_height() / 2 + 95, 140, 60),0,rounded_corn,rounded_corn,rounded_corn,rounded_corn)
                mouseinbox1 = True
            else:
                mouseinbox1 = False
            
            text = font.render("Level 1", True, "black")
            text_rect = text.get_rect(center=(screen.get_width() / 2-220, screen.get_height() / 2 + 125))
            screen.blit(text,text_rect)
            
            
            #level 2 button
            lvl2_button = pygame.draw.rect(screen,"white", (screen.get_width() / 2 - 60, screen.get_height() / 2 + 100, 120, 50),0,rounded_corn,rounded_corn,rounded_corn,rounded_corn)
            if(lvl2_button.collidepoint(pygame.mouse.get_pos())): 
                pygame.draw.rect(screen,"grey", (screen.get_width() / 2 - 70, screen.get_height() / 2 + 95, 140, 60),0,rounded_corn,rounded_corn,rounded_corn,rounded_corn)
                mouseinbox2 = True
            else:
                mouseinbox2 = False
            text = font.render("Level 2", True, "black")
            text_rect = text.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2 + 125))
            screen.blit(text,text_rect)

            #level 3 button
            lvl3_button = pygame.draw.rect(screen,"white", (screen.get_width() / 2 +160, screen.get_height() / 2 + 100, 120, 50),0,rounded_corn,rounded_corn,rounded_corn,rounded_corn)
            if(lvl3_button.collidepoint(pygame.mouse.get_pos())): 
                pygame.draw.rect(screen,"grey", (screen.get_width() / 2 + 150, screen.get_height() / 2 + 95, 140, 60),0,rounded_corn,rounded_corn,rounded_corn,rounded_corn)
                mouseinbox3 = True
            else:
                mouseinbox3 = False
            text = font.render("Level 3", True, "black")
            text_rect = text.get_rect(center=(screen.get_width() / 2 +220, screen.get_height() / 2 + 125))
            screen.blit(text,text_rect)

            #highscore button
            highscore_butt = pygame.draw.rect(screen,"white", (screen.get_width() / 2 - 60, screen.get_height() / 2 + 200, 120, 50),0,rounded_corn,rounded_corn,rounded_corn,rounded_corn)
            if(highscore_butt.collidepoint(pygame.mouse.get_pos())):
                pygame.draw.rect(screen,"grey", (screen.get_width() / 2 - 70, screen.get_height() / 2 + 195, 140, 60),0,rounded_corn,rounded_corn,rounded_corn,rounded_corn)
                mouseinbox4 = True
            else:
                mouseinbox4 = False
            text = font.render("High Score", True, "black")
            text_rect = text.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2 + 225))
            screen.blit(text,text_rect)

            pygame.display.flip()
            dt = 0
            clock.tick(60)
            
            if mouseinbox1 and pygame.mouse.get_pressed()[0]:
                mode = "gameon1"
                n_size = 20
                marked_map,solution = wilson_maze(n_size)
                maze_img = pygame.display.set_mode((50+20*len(marked_map),50+20*len(marked_map)))
                bg_generate_2(maze_img,marked_map)
                pygame.image.save(maze_img,"marked_maze.png")
                screen = pygame.display.set_mode((800, 1000))
                time_tot = 240
                pygame.time.delay(100)
                pygame.mixer.music.play(-1)
                player_pos = (100,100)
                frame_num=1
                u_d_is = False
                r_l_is = False
                running_anim = 'idle'
                print("start")
                print(count_coll)
            if mouseinbox2 and pygame.mouse.get_pressed()[0]:
                mode = "gameon1"
                n_size = 40
                marked_map,solution = wilson_maze(n_size)
                maze_img = pygame.display.set_mode((50+20*len(marked_map),50+20*len(marked_map)))
                bg_generate_2(maze_img,marked_map)
                pygame.image.save(maze_img,"marked_maze.png")
                screen = pygame.display.set_mode((800, 1000))
                time_tot = 240
                pygame.time.delay(100)
                pygame.mixer.music.play(-1)
                player_pos = (100,100)
                frame_num=1
                u_d_is = False
                r_l_is = False
                running_anim = 'idle'
                print("start")
            if mouseinbox3 and pygame.mouse.get_pressed()[0]:
                mode = "gameon1"
                n_size = 60
                marked_map,solution = wilson_maze(n_size)
                maze_img = pygame.display.set_mode((50+20*len(marked_map),50+20*len(marked_map)))
                bg_generate_2(maze_img,marked_map)
                pygame.image.save(maze_img,"marked_maze.png")
                screen = pygame.display.set_mode((800, 1000))
                time_tot = 240
                pygame.time.delay(100)
                pygame.mixer.music.play(-1)
                player_pos = (100,100)
                frame_num=1
                u_d_is = False
                r_l_is = False
                running_anim = 'idle'
                print("start")
            if mouseinbox4 and pygame.mouse.get_pressed()[0]:
                mode = "highscore"
                score_list = get_score(highscore_file)
            if mouseinoptbx and pygame.mouse.get_pressed()[0]:
                mode = 'options'
        
        case "highscore":
            screen.fill("black")
            screen.blit(high_img_bg,(0,0))
            font = pygame.font.Font(None, 74)
            text = font.render("High Score", True, "yellow")
            text_rect = text.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2 - 200))
            screen.blit(text, text_rect)
            pygame.draw.rect(screen,"blue",(screen.get_width()/2 - 300,screen.get_height()/2-70 ,600,400))
            font = pygame.font.Font(None, 50)
            text = font.render("Easy", True, "yellow")
            text_rect = text.get_rect(center=(screen.get_width() / 2-200, screen.get_height() / 2 -20))
            screen.blit(text, text_rect)
            text = font.render("Medium", True, "yellow")
            text_rect = text.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2 - 20))
            screen.blit(text, text_rect)
            text = font.render("Hard", True, "yellow")
            text_rect = text.get_rect(center=(screen.get_width() / 2+200, screen.get_height() / 2 - 20 ))
            screen.blit(text, text_rect)
            font = pygame.font.Font(None, 40)
            for i in range(len(score_list["e"])):
                text = font.render(f"{score_list['e'][i]}",True,"orange")
                text_rect = text.get_rect(center=(screen.get_width()/2 - 200, screen.get_height()/2 + 80 + i*50))
                screen.blit(text,text_rect)
            for i in range(len(score_list["m"])):
                text = font.render(f"{score_list['m'][i]}",True,"orange")
                text_rect = text.get_rect(center=(screen.get_width()/2 , screen.get_height()/2 + 80 + i*50))
                screen.blit(text,text_rect)
            for i in range(len(score_list["h"])):
                text = font.render(f"{score_list['h'][i]}",True,"orange")
                text_rect = text.get_rect(center=(screen.get_width()/2 + 200, screen.get_height()/2 + 80 + i*50))
                screen.blit(text,text_rect)
            mainscreen_butt = pygame.draw.rect(screen,"white",(screen.get_width()/2 - 100,screen.get_height()/2 + 300,200,50),0,rounded_corn,rounded_corn,rounded_corn,rounded_corn)
            font = pygame.font.Font(None, 30)
            if mainscreen_butt.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(screen,"grey",(screen.get_width()/2 - 110,screen.get_height()/2 + 295,220,60),0,rounded_corn,rounded_corn,rounded_corn,rounded_corn)
                mouseinbox5 = True
            else:
                mouseinbox5 = False
            text = font.render("Main Screen",True,"black")
            text_rect = text.get_rect(center=(screen.get_width()/2,screen.get_height()/2 + 325))
            screen.blit(text,text_rect)
            if mouseinbox5 and pygame.mouse.get_pressed()[0]:
                mode = "startmenu"
            pygame.display.flip()
            dt = 0
            clock.tick(60)
        
        case "gameon1":
            screen.fill("gray")
            #bg_generate(30)
            create_bg(screen,marked_map,player_pos)
            if not_collide:
                if r_l_is:
                    if pygame.key.get_pressed()[leftkey]:
                        flip_char = True
                    elif pygame.key.get_pressed()[rightkey]:
                        flip_char = False
                    player_pos += pygame.Vector2(1 - 2*(int(flip_char)) , 0) * dt * speed *1/10
                    if(frame_num >= 9):
                        r_l_is = False
                        running_anim = 'idle'
                        img_copy = img1_cat.copy()
                    else:
                        img_copy = r_l_cat[int(frame_num)].copy()
                        frame_num += frame_speed
                
                elif u_d_is:
                    
                    if pygame.key.get_pressed()[downkey]:
                        u_d =1
                    if pygame.key.get_pressed()[upkey]:
                        u_d = -1
                    player_pos += pygame.Vector2(0, u_d) * dt * speed *1/10
                    if(frame_num >= 9):
                        u_d_is = False
                        running_anim='idle'
                        img_copy = img1_cat.copy()
                    else:
                        img_copy = emote_cat[int(frame_num)].copy()
                        frame_num += frame_speed
                else:    
                    #key = pygame.key.get_pressed()
                    #player_pos,running = move(screen,player_pos,dt,running,key)
                    img_copy = img1_cat.copy()
                img_with_flip = pygame.transform.flip(img_copy, flip_char, False).convert_alpha()
                screen.blit(img_with_flip, pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2-100))
                if not (u_d_is or r_l_is):
                    if(pygame.key.get_pressed()[leftkey] or pygame.key.get_pressed()[rightkey] and (running_anim == 'idle') and (not (pygame.key.get_pressed()[downkey] or pygame.key.get_pressed()[upkey]))):
                        r_l_is = True
                        running_anim = 'r_l'
                        if frame_num >=9:
                            frame_num = 1
                    elif(pygame.key.get_pressed()[downkey] or pygame.key.get_pressed()[upkey]):
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
                screen.blit(img_with_flip, pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2 -100))
            pygame.draw.rect(screen,"black",(0,800,800,200))
            font2 = pygame.font.Font("./dpcomic/dpcomic.ttf",60)
            text = font2.render(time_strng, True, "white")
            screen.blit(text, (500,830))
            text2 = font2.render(f"Score: {score + int(timefac* time_tot)}",True,"orange")
            screen.blit(text2,(50,830))
            mask(screen,time_tot,max_time)
            pygame.display.flip()
            dt = clock.tick(60) / 1000

        case "winscreen":
            k = 15
            dt = 0
            for i in range(1*k,4*k):
                
                create_bg(screen,marked_map,[(n_size)*100+initpos[0]+50,(n_size)*100+initpos[1]+50])
                img_copy = img_celeb[i//k].copy()
                img_with_flip = pygame.transform.flip(img_copy, flip_char, False).convert_alpha()
                screen.blit(img_copy, pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2-100))
                pygame.draw.rect(screen,"black",(0,800,800,200))
                font2 =pygame.font.Font("./dpcomic/dpcomic.ttf",60)
                text = font2.render("Congratulations!!!", True, "White")
                text2= font2.render("You have reached the end",True,"White")
                text_rect = text.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2 + 350))
                text_rect2 = text.get_rect(center=(screen.get_width() / 2 - 100, screen.get_height() / 2 + 450))
                screen.blit(text,text_rect)
                screen.blit(text2,text_rect2)
                font2 = pygame.font.Font("./dpcomic/dpcomic.ttf",90)
                text3 = font2.render(f"Score:{score}",True,"white")
                text3_rect = text.get_rect(center=(screen.get_width()/2 + 50 , screen.get_height()/2 -250))
                pygame.draw.rect(screen, "black", (screen.get_width()/2 -160 , screen.get_height()/2 -275,400,70), border_radius=10)
                screen.blit(text3,text3_rect)
                font2 = pygame.font.Font("./dpcomic/dpcomic.ttf",92)
                text3 = font2.render(f"Score:{score}",True,"orange")
                text3_rect = text.get_rect(center=(screen.get_width()/2 + 47 , screen.get_height()/2 -250))
                screen.blit(text3,text3_rect)
                pygame.display.flip()
                if mousedown:
                    mode = "startmenu"
                    pygame.mixer.music.stop()
                clock.tick(60)

        
        case "gameover":
            screen.fill("black")
            screen.blit(main_img_backg,(0,0 ))
            font = pygame.font.Font(None, 74)
            text = font.render("Game Over", True, "white")
            text_rect = text.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2))
            screen.blit(text, text_rect)
            restart_butt = pygame.draw.rect(screen,"white", (screen.get_width() / 2 - 100, screen.get_height() / 2 + 100, 200, 50),0,rounded_corn,rounded_corn,rounded_corn,rounded_corn)
            if(restart_butt.collidepoint(pygame.mouse.get_pos())):
                pygame.draw.rect(screen,"grey", (screen.get_width() / 2 - 110, screen.get_height() / 2 + 95, 220, 60),0,rounded_corn,rounded_corn,rounded_corn,rounded_corn)
                mouseinbox = True
            else:
                mouseinbox = False
            font = pygame.font.Font(None, 30)
            text = font.render("Back to Main Menu", True, "black")
            text_rect = text.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2 + 120))
            screen.blit(text,text_rect)
            pygame.display.flip()
            dt = 0
            clock.tick(60)

            if mouseinbox and mousedown:
                mode = "startmenu" 
                flag = 'hi'
                screen = pygame.display.set_mode(screensize)
                pygame.time.delay(500)
                clock.tick(60)
                print("restart")
                mousedown = False
        
        case "options":        
            screen.fill("black")
            screen.blit(opt_img_bg,(0,0))
            font = pygame.font.Font(None, 74)
            text = font.render("Options", True, "white")
            text_rect = text.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2 - 180))
            screen.blit(text, text_rect)
            back_butt = pygame.draw.rect(screen,"white", (screen.get_width() / 2 - 60, screen.get_height() / 2 + 100, 120, 50),0,rounded_corn,rounded_corn,rounded_corn,rounded_corn)
            if(back_butt.collidepoint(pygame.mouse.get_pos())):
                pygame.draw.rect(screen,"grey", (screen.get_width() / 2 - 70, screen.get_height() / 2 + 95, 140, 60),0,rounded_corn,rounded_corn,rounded_corn,rounded_corn)
                mouseinbox = True
            else:
                mouseinbox = False
            font = pygame.font.Font(None, 30)
            text = font.render("Back", True, "black")
            text_rect = text.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2 + 120))
            change_butt = pygame.draw.rect(screen,"white", (screen.get_width() / 2 - 90, screen.get_height() / 2 - 30, 180, 50),0,rounded_corn,rounded_corn,rounded_corn,rounded_corn)
            screen.blit(text,text_rect)
            text_2 = font.render("Change Controls",True,"black")
            text_rect_2 = text_2.get_rect(center=(screen.get_width()/2,screen.get_height()/2))
            
            if(change_butt.collidepoint(pygame.mouse.get_pos())): 
                pygame.draw.rect(screen,"grey", (screen.get_width() / 2 - 95, screen.get_height() / 2 -35, 190, 60),0,rounded_corn,rounded_corn,rounded_corn,rounded_corn)
                mouseinoptbx = True
            else:
                mouseinoptbx = False
            screen.blit(text_2,text_rect_2)
            font= pygame.font.Font(None,50)
            if mouseinoptbx and mousedown:
                if set1:
                    set1 = False
                else:
                    set1 = True
                pygame.time.delay(500)
                mousedown = False
            if set1:
                text3 = font.render("WASD mode",True,"white")
            else:
                text3 = font.render("Arrow mode",True,"white")
            text_rect3 = text3.get_rect(center=(screen.get_width()/2,screen.get_height()/2+50))
            screen.blit(text3,text_rect3)
            pygame.display.flip()
            dt = 0
            clock.tick(60)
            if mouseinbox and mousedown:
                mode = "startmenu"
                pygame.time.delay(500)
                clock.tick(60)
                print("back")
                mousedown = False
    
    if pygame.key.get_pressed()[pygame.K_SPACE]: 
        if mode == "gameon1" or mode=="winscreen":
            mode = "gameover"
            screen = pygame.display.set_mode(screensize)
            pygame.mixer.music.stop()
        print("gameover")

pygame.quit()

