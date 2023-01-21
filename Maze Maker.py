# this is going to be a maze game program
# the intent of this pgrm is to design the maze
# a maze will be made but hidden from user. the area around the mouse will be shown in a small distance 
# touching the invalid vlock smeans that you failed

import random

def make_path(x,y,arr,dir,maze_size):
    sum=0
    tx=x
    ty=y
    if(dir==0):
        ty=y-1  #Y axis is reversed in array
    elif(dir==1):
        tx=x+1
    elif(dir==2):
        ty=y+1
    else:
        tx=x-1
    if (tx==0) or (ty==0) or (ty==maze_size-1) or (tx==maze_size-1):
        return x,y,arr,False
    sum=arr[tx+1][ty]+arr[tx-1][ty]+arr[tx][ty+1]+arr[tx][ty-1]
    if(sum>1):
        return x,y,arr,False
    print("tick-",dir)
    arr[tx][ty]=1
    return tx,ty,arr,True


maze_size=int(input("Enter maze size:"));
tile_size=75
visibility=2
arr =[[0 for i in range(maze_size)]for j in range(maze_size)]
flag=0
x,y=1,1
arr[1][1]=1
check=True
setval=[]
for i in range(0,4):
    setval.append(int(i));
while(flag==0):
    if (x==0) or (x==maze_size-1) or (y==maze_size-1) or (y==0):
        break;
    random.shuffle(setval)
    for i in setval:
        x,y,arr,check=make_path(x,y,arr,i,maze_size)
        if(check):
            break
    if(check==False):    
        break

for each in arr:
    print(each)















