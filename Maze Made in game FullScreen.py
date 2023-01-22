# this is going to be a maze game program
# the intent of this pgrm is to design the maze
# a maze will be made but hidden from user. the area around the mouse will be shown in a small distance 
# touching the invalid vlock smeans that you failed

import random
import pygame
import sys
import time

class Player(pygame.sprite.Sprite):
    def __init__(self,path):
        super().__init__()
        self.image = pygame.image.load(path)
        self.rect= self.image.get_rect()
    
    def update(self,screen,arr,height,width,sizetx,sizety,visibility):
        (x,y)=pygame.mouse.get_pos()
        x=int(x/width)
        y=int(y/height)
        lim=visibility
        low=100/lim
        if(x<1) or (x>sizetx-2) or (y<1) or (y>sizety-2) :
            return True
        if(arr[y][x]==0):
            return False
        for i in range(-lim,lim+1):
            for j in range(-lim,lim+1):
                if(x+i<0) or (x+i>=sizetx) or (y+j<0) or (y+j>=sizety) :
                    continue
                if(arr[y+j][x+i]==1):
                        pygame.draw.rect(screen, (255-low*(abs(i)+abs(j)),255-low*(abs(i)+abs(j)),255-low*(abs(i)+abs(j))), pygame.Rect((x+i)*height,(y+j)*width,width,height))  

        self.rect.center=pygame.mouse.get_pos()
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
    end_point=[]
    valid_space.append([(x,y)])
    for i in range(0,4):
        setval.append(int(i))
    while(flag<10000):
        flag+=1
        if(x==maze_sizeX-limit-1) and (y==maze_sizeY-limit-1):
            break
        random.shuffle(setval)
        for i in setval:
            x,y,arr,check=make_path(x,y,arr,i,maze_sizeX,maze_sizeY,limit)
            if(check):
                valid_space.append([(x,y)])
                break
        if(check==False):
            ([(x,y)])=random.choice(valid_space) 
    show_maze(arr,maze_sizeX,maze_sizeY)  


    if(flag==10000):
        return mainmaze(mazesize)

    return arr



# mainmaze(20)
def the_game(sizet,tile_size,visi):
    arr=mainmaze(sizet)
    sizetx=int(1.778*sizet)
    sizety=sizet
    pygame.init()  
    # screen = pygame.display.set_mode((tile_size*sizet,tile_size*sizet))
    screen = pygame.display.set_mode((tile_size*sizetx,tile_size*sizety),pygame.FULLSCREEN)    
    done = True
    x=int(tile_size/2)
    y=int(tile_size/2)
    recwidth=tile_size
    recheight=tile_size
    background=pygame.Surface([1600,900])
    ply1= Player("a.png")
    ply=pygame.sprite.Group()
    ply.add(ply1)
    clock=pygame.time.Clock()


    visibility=visi


    pygame.display.flip()
    for i in range(0,100):
        pygame.mouse.set_pos(recwidth*1.5,recwidth*1.5)
    # pygame.mouse.set_visible(False)

    while True:
        pygame.display.flip()  
        for event in pygame.event.get():  
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
                sys.exit()
        screen.blit(background,(0,0))
        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect((sizetx-2)*tile_size,(sizety-2)*tile_size,tile_size,tile_size))  
        ply.draw(screen)
        (x,y)=pygame.mouse.get_pos()
        ply.update(screen,arr,recheight,recwidth,sizetx,sizety,visibility)
        clock.tick(60) 
        if(y>900):
            print(y)
        if(arr[int(y/recwidth)][int(x/recwidth)]==0):
            pygame.mouse.set_pos(recwidth*1.5,recwidth*1.5)
        
        if(arr[int(y/recwidth)][int(x/recwidth)]==2):
            pygame.display.quit()
            pygame.quit()
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
the_game(val+2,int(scrsize/(val+2)),visibility)


time.sleep(1)

print("Congrats")

time.sleep(1)
time.sleep(1)