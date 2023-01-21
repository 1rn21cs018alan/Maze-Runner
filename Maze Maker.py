# this is going to be a maze game program
# the intent of this pgrm is to design the maze
# a maze will be made but hidden from user. the area around the mouse will be shown in a small distance 
# touching the invalid vlock smeans that you failed

import random

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

def mainmaze():
    # limit=int(input("Enter border size:"))
    limit=1
    maze_size=int(input("Enter maze size:"))
    # maze_size=15
    tile_size=75
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


    # for i in range(0,maze_size):
    #     for j in range(0,maze_size):
    #         if(arr[i][j]==1):
    #             arr[i][j]='⬜'
    #         elif(arr[i][j]==0):
    #             arr[i][j]='⬛'
    #         else:
    #             arr[i][j]='🟥'
                
    show_maze(arr,maze_size)

    print(flag)

    # for each in arr:
    #     print(each)















