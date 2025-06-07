h,w=24,30 
from time import sleep as s
from random import randint 
from msvcrt import kbhit, getch 
gameRun=True 
BirdEye='^' 
colorList= [[62, 191, 11],[48, 145, 10], [33, 117, 55],[255,208,1]] 
def createPipePair(height): 
    for i in range(height):
        for k in range(1,4):gameArray[h-1-i][w-k]=(-abs(k-2))+1
        if i==height-1:
            for a in range(1,3): 
                for j in range(3,0,-1):gameArray[h-(a+1)-i][w-j]=a
    for i in range(h-height-8):
        for k in range(1,4):gameArray[i][w-k]=(-abs(k-2))+1
        if i==h-height-9:
            for a in range(1,3):
                for j in range(3,0,-1):gameArray[i+a][w-j]=a

def ShiftPipes(): 
    for y in range(h):
        for x in range(w): 
            if gameArray[y][x] in (0,1,2): 
                if x==0:gameArray[y][x]=getBGpixel(y,x)
                else:
                    if gameArray[y][x-1]==3: raise Exception("Player hit pipe")
                    gameArray[y][x-1]=gameArray[y][x] 
                    if x+1>=w or gameArray[y][x+1]==getBGpixel(y,x+1):gameArray[y][x]=getBGpixel(y,x) 

def PrintGame():
    global BirdEye, prevFrameArray
    outList=[]
    print("\033[H" + '\033[?25l')
    for y in range(h):
        for x in range(w - 3):
            if gameArray[y][x] == prevFrameArray[y][x]:outList.append("\033[2C")  
            else:
                val = gameArray[y][x]
                if len(str(val))==1:
                    if val != 3:outList.append(f'\033[48;2;{colorList[val][0]};{colorList[val][1]};{colorList[val][2]}m  \033[0m')
                    else:outList.append(f'\033[48;2;{colorList[val][0]};{colorList[val][1]};{colorList[val][2]}m\033[38;5;0m«{BirdEye}\033[0m')
                else:outList.append(val*2)
        outList.append('\n')
    for y in range(h):
        for x in range(w):
            prevFrameArray[y][x] = gameArray[y][x]
    print(''.join(outList))

def getBGpixel(y,x):
    if y<=21 and x<=27:return '\033[48;5;14m \033[0m'
    elif y==22: return ['\x1b[48;5;10m \x1b[0m', '\x1b[48;5;2m \x1b[0m'][x%2]
    elif y==23: return '\x1b[48;2;230;211;151m \x1b[0m' 

def moveBird():
    global birdY
    if BirdMoveState in [4,3]: offSet = -1
    elif BirdMoveState == 2: offSet = 0
    elif BirdMoveState in [1,0]: offSet = 1
    if offSet != 0:
        newY = birdY + offSet
        if newY < 0 or newY > 21:
            raise Exception('Player hit bottom' if newY > 21 else 'Player hit top')
        elif gameArray[newY][8] != getBGpixel(newY,8):
            raise Exception("Player hit pipe")
        else:
            gameArray[birdY][8] =getBGpixel(newY,8)
            birdY = newY
            gameArray[birdY][8] = 3

while True and gameRun==True:
    prevFrameArray = [[-1]*w for _ in range(h)] 
    BirdMoveState=0 
    print("\033[2J" + "\033[H" + '\033[?25l')
    gameArray=[[0]*w for _ in range(h)] 
    for y in range(h):
        for x in range(w):gameArray[y][x]=getBGpixel(y,x)
    birdY = 12
    gameArray[birdY][8]=3
    a=0
    GameDifficulty=0.0
    PipeIter=-1
    Score=0
    while True: 
        if kbhit():
            key = getch().decode()  
            if key=='w':
                BirdMoveState=4
            elif key=='q':
                gameRun=False
                break
        else: BirdMoveState=(BirdMoveState-1) if BirdMoveState !=0 else BirdMoveState 
        try:moveBird()
        except Exception as e:print(e);break
        BirdEye='^' if BirdMoveState>0 else 'v'
        if PipeIter%20==0:
            createPipePair(randint(1,15));PipeIter=0;a+=1
            if a%7==0:GameDifficulty+=0.01
        try:ShiftPipes()
        except Exception as e :print(e);break
        PrintGame()
        print('\033[2K\033[1G',end='')
        print(f'{Score=} {GameDifficulty=}')
        if PipeIter==-1:
            while True:
                if kbhit():
                    key=getch().decode()
                    if key=='w':break
                    elif key=='q':
                        gameRun=False
                        break
        s(.07-GameDifficulty)
        PipeIter+=1 
        Score=Score+1 if PipeIter==19 else Score
        if gameRun==False:break
    if gameRun==True:print('You died. Restarting....');s(1) 

