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
    
    def update(self,screen,arr,height,width,sizet,visibility):
        (y,x)=pygame.mouse.get_pos()
        x=int(x/width)
        y=int(y/height)
        lim=visibility
        low=100/lim
        if(x<1) or (x>sizet-2) or (y<1) or (y>sizet-2) :
            return True
        if(arr[x][y]==0):
            return False
        for i in range(-lim,lim+1):
            for j in range(-lim,lim+1):
                if(x+i<0) or (x+i>=sizet) or (y+j<0) or (y+j>=sizet) :
                    continue
                if(arr[x+i][y+j]==1):
                        pygame.draw.rect(screen, (255-low*(abs(i)+abs(j)),255-low*(abs(i)+abs(j)),255-low*(abs(i)+abs(j))), pygame.Rect((y+j)*width,(x+i)*height,width,height))  

        # if(arr[x][y]==1):
        #         pygame.draw.rect(screen, (255, 255, 255), pygame.Rect((y)*width,(x)*height,width,height))  
                        
        # if(arr[y][x]==1):
        #         pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(x*width,y*height,width,height))  
        
        self.rect.center=pygame.mouse.get_pos()
        return True

def show_maze(arr,maze_size):
    for i in range(0,maze_size):
        for j in range(0,maze_size):
            if(arr[i][j]==1):
                print('⬜',end='')
            elif(arr[i][j]==0):
                print('⬛',end='')
            else:
                print('🟥',end='')
        print()

def make_path(x,y,arr,dir,maze_size,limit):
    sum=0
    tx=x
    ty=y
    if((tx==maze_size-limit -2)and(ty==maze_size-limit-1))or((tx==maze_size-limit -1)and(ty==maze_size-limit -2)):
        tx=maze_size-limit-1
        ty=maze_size-limit-1
        arr[tx][ty]=2
        # arr[maze_size-limit-1][maze_size-limit-1]=2
        return tx,ty,arr,True

    if(dir==0):
        ty=y-1  #Y axis is reversed in array
    elif(dir==1):
        tx=x+1
    elif(dir==2):
        ty=y+1
    else:
        tx=x-1
    if (tx<limit) or (ty<limit) or (ty==maze_size-limit) or (tx==maze_size-limit):
        return x,y,arr,False
    sum=arr[tx+1][ty]+arr[tx-1][ty]+arr[tx][ty+1]+arr[tx][ty-1]
    if(sum>1):
        return x,y,arr,False
    # print("tick-",dir)
    arr[tx][ty]=1
    return tx,ty,arr,True

def mainmaze(mazesize):
    # limit=int(input("Enter border size:"))
    limit=1
    # maze_size=int(input("Enter maze size:"))
    # maze_size=15
    maze_size=mazesize
    arr =[[0 for i in range(maze_size)]for j in range(maze_size)]
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
        # if (x<limit) or (x==maze_size-limit) or (y==maze_size-limit) or (y<limit):
        if(x==maze_size-limit-1) and (y==maze_size-limit-1):
            break
            # ([(x,y)])=random.choice(valid_space) 
            # continue
        random.shuffle(setval)
        for i in setval:
            x,y,arr,check=make_path(x,y,arr,i,maze_size,limit)
            if(check):
                valid_space.append([(x,y)])
                break
        if(check==False):
            # end_point.append([(x,y)])
            ([(x,y)])=random.choice(valid_space) 
    show_maze(arr,maze_size)  


    # for i in range(0,maze_size):
    #     for j in range(0,maze_size):
    #         if(arr[i][j]==1):
    #             arr[i][j]='⬜'
    #         elif(arr[i][j]==0):
    #             arr[i][j]='⬛'
    #         else:
    #             arr[i][j]='🟥'
                
    # show_maze(arr,maze_size)

    if(flag==10000):
        return mainmaze(mazesize)

    # for each in arr:
    #     print(each)
    return arr



# mainmaze(20)
def the_game(sizet,tile_size):
    arr=mainmaze(sizet)
    pygame.init()  
    screen = pygame.display.set_mode((tile_size*sizet,tile_size*sizet))
    # screen = pygame.display.set_mode((tile_size*sizet,tile_size*sizet),pygame.FULLSCREEN)    
    done = True
    x=int(tile_size/2)
    y=int(tile_size/2)
    recwidth=tile_size
    recheight=tile_size
    background=pygame.Surface([tile_size*sizet,tile_size*sizet])
    ply1= Player("a.png")
    ply=pygame.sprite.Group()
    ply.add(ply1)
    clock=pygame.time.Clock()


    visibility=2


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
        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect((sizet-2)*tile_size,(sizet-2)*tile_size,tile_size,tile_size))  
        ply.draw(screen)
        (y,x)=pygame.mouse.get_pos()
        ply.update(screen,arr,recheight,recwidth,sizet,visibility)
        clock.tick(60) 
        if(arr[int(x/recwidth)][int(y/recwidth)]==0):
            pygame.mouse.set_pos(recwidth*1.5,recwidth*1.5)
        
        if(arr[int(x/recwidth)][int(y/recwidth)]==2):
            pygame.display.quit()
            pygame.quit()
            return
    

val=10
al=""
with open("siz.txt",mode="r") as MyFile:
    for x in MyFile:
        al=al+x
val=int(al)
# val=int(input("Enter no of tiles: "))
time.sleep(1)
scrsize=750
the_game(val+2,int(scrsize/(val+2)))


time.sleep(1)

print("Congrats")

time.sleep(1)
time.sleep(1)