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
def ending(sizet,tile_size,visi):
    time.sleep(1)
    game_1.new_game(sizet,tile_size,visi)

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
        #sizet= no of blocks for maze in vertical direction
        pygame.init()  
        self.font = pygame.font.SysFont('Arial', int(900/12-20-10))
        # screen = pygame.display.set_mode((tile_size*sizet,tile_size*sizet))
        screen = pygame.display.set_mode((1600,900),pygame.FULLSCREEN)
        self.screen=screen
        self.new_game(sizet,tile_size,visi) 


    def new_game(self,sizet,tile_size,visi):
        arr=mainmaze(sizet)
        sizetx=int(1.778*sizet)
        sizety=sizet
        self.sizetx=sizetx
        self.sizety=sizety 
        screen=self.screen
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
                    sys.exit()
                elif (event.type == pygame.KEYDOWN):
                    if(event.key!=pygame.K_ESCAPE):
                        ply.update(screen,arr,recheight,recwidth,sizetx,sizety,visibility,event)
                        ply.draw(screen)
                        clock.tick(60)
                    else:
                        self.set_prev_screen(screen)
                        button_coord,menu_coord=self.draw_pause_menu()
                        pygame.display.flip()
                        clock.tick(60)
                        pause_menu=True
                        while pause_menu:
                            for event in pygame.event.get():  
                                if event.type == pygame.QUIT:
                                    pygame.display.quit()
                                    pygame.quit()
                                    sys.exit()
                                elif (event.type == pygame.KEYDOWN):
                                    if(event.key==pygame.K_ESCAPE):
                                        pause_menu=False
                                        self.get_prev_screen()
                                        clock.tick(60)
                                elif (event.type == pygame.MOUSEBUTTONDOWN):
                                    mouse_pos=pygame.mouse.get_pos()
                                    if(mouse_pos[0]>=button_coord[0]+menu_coord[2]) and (mouse_pos[0]<=button_coord[0]+button_coord[1]+menu_coord[2]):#within button holder location in x axis
                                        if(mouse_pos[1]>=menu_coord[3]+button_coord[3]) and (mouse_pos[1]<=menu_coord[3]+button_coord[3]+button_coord[2]):
                                            pause_menu=False
                                            self.get_prev_screen()
                                            clock.tick(60)

                                        elif(mouse_pos[1]>=menu_coord[3]+button_coord[4]) and (mouse_pos[1]<=menu_coord[3]+button_coord[4]+button_coord[2]):
                                            pause_menu=False
                                            ply1.pos_x=1
                                            ply1.pos_y=1
                                            ply.update(screen,arr,recheight,recwidth,sizetx,sizety,visibility,None) 
                                            ply.draw(screen)
                                            clock.tick(60)

                                        elif(mouse_pos[1]>=menu_coord[3]+button_coord[5]) and (mouse_pos[1]<=menu_coord[3]+button_coord[5]+button_coord[2]):
                                            pause_menu=False
                                            ending(sizet,tile_size,visi)
                                            clock.tick(60)

                                        elif(mouse_pos[1]>=menu_coord[3]+button_coord[6]) and (mouse_pos[1]<=menu_coord[3]+button_coord[6]+button_coord[2]):
                                            pygame.display.quit()
                                            pygame.quit()
                                            sys.exit()
                                    
                                            

                        

            screen.blit(background,(0,0))
            pygame.draw.rect(screen, (255, 0, 0), pygame.Rect((sizetx-2)*tile_size,(sizety-2)*tile_size,tile_size,tile_size)) 
            ply.update(screen,arr,recheight,recwidth,sizetx,sizety,visibility,None) 
            ply.draw(screen)
            clock.tick(60) 
            
            if(ply1.at_end(sizetx,sizety)):
                pygame.display.flip()
                clock.tick(1)
                # pygame.display.quit()
                # pygame.quit()
                self.congrats()
                ending(sizet,tile_size,visi)
                return
    def draw_pause_menu(self):
        #pause menu has 4 options: resume,reset, new game, quit
        button_coord,menu_size=self.draw_menu(4)
        self.screen.blit(self.font.render('Resume', True, (255,255,255)), (button_coord[0]+menu_size[2]+20, button_coord[3]+menu_size[3]+20))
        self.screen.blit(self.font.render('Reset', True, (255,255,0)), (button_coord[0]+menu_size[2]+20, button_coord[4]+menu_size[3]+20))
        self.screen.blit(self.font.render('New Game', True, (0,255,0)), (button_coord[0]+menu_size[2]+20, button_coord[5]+menu_size[3]+20))
        self.screen.blit(self.font.render('Quit', True, (255,0,0)), (button_coord[0]+menu_size[2]+20, button_coord[6]+menu_size[3]+20))
        return button_coord,menu_size
    

    def draw_menu(self,num_options):
        border=10.0
        spacing=10.0
        screen_size=self.screen.get_size()
        menu_size=(int(screen_size[0]/3+2*border),int(num_options*screen_size[1]/8+2*border))
        menu=pygame.Surface(menu_size)
        menu.set_alpha(128)
        menu.fill((255,100,255))
        pygame.draw.rect(menu,(185,0,255),pygame.Rect((0,0),menu_size),width=int(border))
        width=int(menu_size[0]-2*(border+spacing))
        height=int((menu_size[1]-2*border)/num_options)-2*spacing
        x_coord=int(border+spacing)
        coord_list=[x_coord,width,height]
        for i in range(num_options):
            y_coord=int(border+spacing+i*(menu_size[1]-2*border)/num_options)
            coord_list.append(y_coord)
            pygame.draw.rect(menu,(80,80,255),pygame.Rect(x_coord,y_coord,width,height))
            pygame.draw.rect(menu,(30,30,200),pygame.Rect(x_coord,y_coord,width,height),width=int(border))


        self.screen.blit(menu,((screen_size[0]-menu_size[0])/2,(screen_size[1]-menu_size[1])/2))
        menu_size=[menu_size[0],menu_size[1],(screen_size[0]-menu_size[0])/2,(screen_size[1]-menu_size[1])/2]
        return coord_list,menu_size
    
    def congrats(self):
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