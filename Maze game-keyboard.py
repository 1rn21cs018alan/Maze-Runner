# this is going to be a maze game program
# the intent of this pgrm is to design the maze
# a maze will be made but hidden from user. the area around the mouse will be shown in a small distance 
# touching the invalid vlock smeans that you failed

import random
import pygame
import sys
import time
import math
import copy
def ending():
    time.sleep(1)

    print("Congrats")

class Player(pygame.sprite.Sprite):
    def __init__(self,path):
        super().__init__()
        self.image = pygame.image.load(path)
        self.rect= self.image.get_rect()
        self.pos_x=1
        self.pos_y=1
    def position_update(self,arr,size_x,size_y,offset_x,offset_y):
        if not((self.pos_x+offset_x<0) or (self.pos_x+offset_x>=size_x) or (self.pos_y+offset_y<0) or (self.pos_y+offset_y>=size_y)) :
            if(arr[self.pos_y+offset_y][self.pos_x+offset_x]>=1):
                self.pos_x+=offset_x
                self.pos_y+=offset_y
                return True
            else:
                return False
        else:
            return False
        
    def update(self,screen,arr,height,width,sizetx,sizety,visibility,event):
        prev_x=self.pos_x
        prev_y=self.pos_y
        if(event!=None):
            changed_flag=True
            if (event.key==pygame.K_w):
                # self.pos_y-=1
                changed_flag=self.position_update(arr,sizetx,sizety,0,-1)
            elif(event.key==pygame.K_s):
                # self.pos_y+=1
                changed_flag=self.position_update(arr,sizetx,sizety,0,1)
            elif(event.key==pygame.K_a):
                # self.pos_x-=1
                changed_flag=self.position_update(arr,sizetx,sizety,-1,0)
            elif(event.key==pygame.K_d):
                # self.pos_x+=1
                changed_flag=self.position_update(arr,sizetx,sizety,1,0)
            else:
                event=None
                changed_flag=False
            if not changed_flag:
                return
        lim=visibility
        low=100/lim
        x=self.pos_x
        y=self.pos_y
        if(event!=None):
            self.slow_move_before(x,y,height,width,prev_x,prev_y)
        game_1.blank_screen(width)
        for i in range(-lim,lim+1):
            for j in range(-lim,lim+1):
                if(x+i<0) or (x+i>=sizetx) or (y+j<0) or (y+j>=sizety) :
                    continue
                if(arr[y+j][x+i]==1):
                        pygame.draw.rect(screen, (255-low*(abs(i)+abs(j)),255-low*(abs(i)+abs(j)),255-low*(abs(i)+abs(j))), pygame.Rect((x+i)*height,(y+j)*width,width,height))  
        
        game_1.set_prev_screen(screen)
        if(event!=None):
            self.slow_move_after(x,y,height,width,prev_x,prev_y)
        self.rect.center=[(x+0.5)*height,(y+0.5)*width]
        return True
    
    def slow_move_before(self,x,y,height,width,prev_x,prev_y):
        for i in range(0,16):
            game_1.get_prev_screen()
            self.rect.center=[(prev_x+(x-prev_x)*math.sin(math.pi*i/64)+0.5)*height,(prev_y+(y-prev_y)*math.sin(math.pi*i/64)+0.5)*width]
            game_1.animation_tick()
            
    def slow_move_after(self,x,y,height,width,prev_x,prev_y):
        for i in range(16,32):
            game_1.get_prev_screen()
            self.rect.center=[(prev_x+(x-prev_x)*math.sin(math.pi*i/64)+0.5)*height,(prev_y+(y-prev_y)*math.sin(math.pi*i/64)+0.5)*width]
            game_1.animation_tick()
    def at_end(self,size_x,size_y):
        if((self.pos_x==size_x-2) and (self.pos_y==size_y-2)):
            return True

def show_maze(arr,maze_sizeX,maze_sizeY):
    for i in range(0,maze_sizeY):
        for j in range(0,maze_sizeX):
            if(arr[i][j]==1):
                print('⬜',end='')
            elif(arr[i][j]==0):
                print('⬛',end='')
            else:
                print('🟥',end='')
        print()

def make_path(x,y,arr,dir,maze_sizeX,maze_sizeY,limit):
    sum=0
    tx=x
    ty=y
    if((tx==maze_sizeX-limit -2)and(ty==maze_sizeY-limit-1))or((tx==maze_sizeX-limit -1)and(ty==maze_sizeY-limit -2)):
        tx=maze_sizeX-limit-1
        ty=maze_sizeY-limit-1
        arr[ty][tx]=2
        return tx,ty,arr,True

    if(dir==0):
        ty=y-1  #Y axis is reversed in array
    elif(dir==1):
        tx=x+1
    elif(dir==2):
        ty=y+1
    else:
        tx=x-1
    if (tx<limit) or (ty<limit) or (ty==maze_sizeY-limit) or (tx==maze_sizeX-limit):
        return x,y,arr,False
    # print(tx," ",ty)
    sum=arr[ty+1][tx]+arr[ty-1][tx]+arr[ty][tx+1]+arr[ty][tx-1]
    if(sum>1):
        return x,y,arr,False
    # print("tick-",dir)
    arr[ty][tx]=1
    return tx,ty,arr,True

def mainmaze(mazesize):
    limit=1
    maze_sizeX=int(1.778*mazesize)
    maze_sizeY=int(mazesize)
    print(maze_sizeX," ",maze_sizeY)
    arr =[[0 for i in range(maze_sizeX)]for j in range(maze_sizeY)]
    print(arr[maze_sizeY-1][maze_sizeX-1])
    flag=0
    x,y=limit,limit
    arr[limit][limit]=1
    check=True
    setval=[]
    valid_space=[]
    number_of_paths=0
    new_path_flag=0
    valid_space.append([(x,y)])
    for i in range(0,4):
        setval.append(int(i))
    while(flag<10000):
        flag+=1
        if(x==maze_sizeX-limit-1) and (y==maze_sizeY-limit-1):
            number_of_paths+=1
            check=False
            if(number_of_paths>6):
                break
        random.shuffle(setval)
        for i in setval:
            x,y,arr,check=make_path(x,y,arr,i,maze_sizeX,maze_sizeY,limit)
            if(check):
                new_path_flag=1
                valid_space.append([(x,y)])
                break
        if(check==False):
            if(new_path_flag!=0):
                number_of_paths+=1
            ([(x,y)])=random.choice(valid_space) 
    show_maze(arr,maze_sizeX,maze_sizeY)  


    if(flag==10000):
        return mainmaze(mazesize)

    return arr



# mainmaze(20)
class Game():
    def __init__(self) -> None:
        self.clock=None
        self.sprite_grp=None
        self.screen=None
        self.sizetx=None
        self.sizety=None
        self.prev_screen=None
        self.speed=1.0
    def animation_tick(self):
        self.clock.tick(60*self.speed)
        self.sprite_grp.draw(self.screen)
        pygame.display.flip()

    def blank_screen(self,tile_size):
        self.screen.blit(pygame.Surface([1600,900]),(0,0))
        pygame.draw.rect(self.screen, (255, 0, 0), pygame.Rect((self.sizetx-2)*tile_size,(self.sizety-2)*tile_size,tile_size,tile_size)) 

    def set_prev_screen(self,screen):
        self.prev_screen=pygame.Surface.copy(screen)


    def get_prev_screen(self):
        self.screen.blit(self.prev_screen,(0,0))

    def set_speed(self,speed:float=1.0):
        self.speed=speed
    def start_game(self,sizet,tile_size,visi):
        arr=mainmaze(sizet)
        sizetx=int(1.778*sizet)
        sizety=sizet
        self.sizetx=sizetx
        self.sizety=sizety
        pygame.init()  
        # screen = pygame.display.set_mode((tile_size*sizet,tile_size*sizet))
        screen = pygame.display.set_mode((tile_size*sizetx,tile_size*sizety),pygame.FULLSCREEN)    
        self.screen=screen
        done = True
        x=int(tile_size/2)
        y=int(tile_size/2)
        recwidth=tile_size
        recheight=tile_size
        background=pygame.Surface([1600,900])
        clock=pygame.time.Clock()
        self.clock=clock
        ply1= Player("a.png")
        ply=pygame.sprite.Group()
        ply.add(ply1)
        self.sprite_grp=ply


        visibility=visi


        pygame.display.flip()
        # pygame.mouse.set_visible(False)

        while True:
            pygame.display.flip()  
            for event in pygame.event.get():  
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    pygame.quit()
                    ending()
                    sys.exit()
                elif (event.type == pygame.KEYDOWN):
                    ply.update(screen,arr,recheight,recwidth,sizetx,sizety,visibility,event)
                    ply.draw(screen)
                    clock.tick(60)

            screen.blit(background,(0,0))
            pygame.draw.rect(screen, (255, 0, 0), pygame.Rect((sizetx-2)*tile_size,(sizety-2)*tile_size,tile_size,tile_size)) 
            ply.update(screen,arr,recheight,recwidth,sizetx,sizety,visibility,None) 
            ply.draw(screen)
            clock.tick(60) 
            
            if(ply1.at_end(sizetx,sizety)):
                pygame.display.flip()
                clock.tick(1)
                pygame.display.quit()
                pygame.quit()
                ending()
                return
        

val=10
al=[]
with open("siz.txt",mode="r") as MyFile:
    for x in MyFile:
        al.append(x)
val=int(al[0])
visibility=int(al[1])
# val=int(input("Enter no of tiles: "))
print(visibility)
time.sleep(1)
scrsize=900
game_1=Game()
game_1.set_speed(3.5)
game_1.start_game(val+2,int(scrsize/(val+2)),visibility)


time.sleep(1)
time.sleep(1)