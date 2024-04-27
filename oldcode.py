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
'''


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
    marked_map = [['lrud' for i in range(len(map_full)*2+5)] for j in range(len(map_full)*2+5)]
    print(len(walls_horz))
    for i in range(len(map_full)*2-1):
        for j in range(len(map_full)*2-1):
            if i%2 == 0 and j%2 == 0:
                if map_full[i//2][j//2] == map_full[0][0]:
                    marked_map[i][j] = str(random.randint(1,8))
                    marked_map[i][j] +='i'
                else:
                    marked_map[i][j] = ''
            elif i%2 == 0 and j%2 == 1:
                if walls_horz[i//2][j//2] == 0:
                    marked_map[i][j] = str(random.randint(1,8))
                    marked_map[i][j] += 'i'
                else:
                    marked_map[i][j] = ''
            elif i%2 == 1 and j%2 == 0:
                if walls_vert[i//2][j//2] == 0:
                    marked_map[i][j] = str(random.randint(1,8))
                    marked_map[i][j] += 'i'
                else:
                    marked_map[i][j] = ''
            else:
                if marked_map[i-1][j] and marked_map[i+1][j] and marked_map[i][j-1] and marked_map[i][j+1]:
                    marked_map[i][j] = str(random.randint(1,8))
                    marked_map[i][j] += 'i'
                else:
                    marked_map[i][j] = ''
    marked_map[0][0] += 'q' #first
    marked_map[len(map_full)*2-2][len(map_full)*2-2] += 'z' #last
    return marked_map