from random import randint
from time import sleep
from msvcrt import kbhit, getch 
class TetrisBlock:                                                                                 
    def __init__(self, BlockColor, BlockType):                                                                                 
        self.BlockColor = colorDict.get(BlockColor)                                                                                 
        self.BlockType = TypeList.index(BlockType)                                                                                 
        self.CoordinateList = []                                                                                                                                                                                                                                            

    def spawnBlock(self, blockY, blockX):
        self.CoordinateList = []
        for i in range(0, 4):
            newY, newX = blockY + spawnYcoordinateList[self.BlockType][i], blockX + spawnXcoordinateList[self.BlockType][i]
            if newY >= len(gameArray) or newX < 0 or newX >= len(gameArray[0]): 
                raise Exception("Block out of bounds during spawn")
            gameArray[newY][newX] = f'\033[48;5;{self.BlockColor}m \033[0m'
            self.CoordinateList.append([newY, newX])

    def getFreeCoordinates(self, direction):
        freeCoords = []
        Xoffset,Yoffset = {'down': (0, 1), 'right': (1, 0), 'left': (-1, 0), 'Sright': (2, 0),'Sleft': (-2, 0)}.get(direction)  
        for y, x in self.CoordinateList:
            if [y + Yoffset, x + Xoffset] not in self.CoordinateList: freeCoords.append([y + Yoffset, x + Xoffset])
        return freeCoords

    def updateBlock(self, direction:str):
        if direction in ['down', 'left', 'right','Sleft', 'Sright']:
            if direction.startswith('S'):
                offsetY, offsetX = 0, -2 if direction == 'Sleft' else 2
            else:
                offsetY, offsetX = (1, 0) if direction == 'down' else (0, -1 if direction == 'left' else 1)
            freeFallingCoords = self.getFreeCoordinates(direction)
            for y, x in freeFallingCoords:
                if y >= len(gameArray) or x < 0 or x >= len(gameArray[0]) or gameArray[y][x] != backgroundPixel:
                    if direction == 'Sleft': return self.updateBlock('left')
                    elif direction == 'Sright': return self.updateBlock('right')
                    return False 
            for y, x in self.CoordinateList:
                gameArray[y][x] = backgroundPixel
            self.CoordinateList = [[y + offsetY, x + offsetX] for y, x in self.CoordinateList]
            for y, x in self.CoordinateList:
                gameArray[y][x] = f'\033[48;5;{self.BlockColor}m \033[0m'
            return True
        elif direction in ['c','cc']:
            if self.BlockType == 'Oblock': return False                                                                                 
            pivotY, pivotX = self.CoordinateList[1]                                                                                 
            newCoordinates = []                                                                                 
            for y, x in self.CoordinateList:                                                                                 
                if direction == 'c': newX, newY = pivotX - y + pivotY, pivotY + x - pivotX                                                                                 
                elif direction == 'cc': newX, newY = pivotX + y - pivotY, pivotY - x + pivotX         
                else: return False                                                                        
                newCoordinates.append([newY, newX])                                                                                 
            for newY, newX in newCoordinates:                                                                                 
                if [newY, newX] not in self.CoordinateList:                                                                                 
                    if newY >= len(gameArray) or newX < 0 or newX >= len(gameArray[0]) \
                        or gameArray[newY][newX] != backgroundPixel \
                        or TypeList[self.BlockType] == 'Oblock':return False                                                                                   
            for y, x in self.CoordinateList:gameArray[y][x] = backgroundPixel                                                                                 
            self.CoordinateList = newCoordinates                                                                                 
            for y, x in self.CoordinateList:gameArray[y][x] = f'\033[48;5;{self.BlockColor}m \033[0m'                                                                                 
            return True     
        else:
            for y, x in block.CoordinateList:gameArray[y][x] = backgroundPixel
            block.CoordinateList = calculateEndCoordinates(block)
            for y, x in block.CoordinateList:gameArray[y][x] = f'\033[48;5;{block.BlockColor}m \033[0m'
            return True

def createNewBlock():
    global PrevColor
    colorIndex = randint(0, len(colorDict) - 1)
    while list(colorDict.keys())[colorIndex] == PrevColor: colorIndex = randint(0, len(colorDict) - 1)
    PrevColor = list(colorDict.keys())[colorIndex]
    blockType = randint(0, len(TypeList) - 1)
    block = TetrisBlock(PrevColor, TypeList[blockType])
    block.spawnBlock(0, 4)
    return block

def clearFullRow():
    global score
    for i in range(len(gameArray)):
        if all(cell != backgroundPixel for cell in gameArray[i]):
            gameArray[i] = [backgroundPixel for _ in range(20)]
            for row in range(i, 0, -1):
                gameArray[row] = gameArray[row - 1][:]
            score += 9

def calculateEndCoordinates(block:TetrisBlock):
    endCoords = [coord[:] for coord in block.CoordinateList]  
    while True:
        newEndCoords = [[y + 1, x] for y, x in endCoords]
        for y, x in newEndCoords:
            if y >= len(gameArray) or x < 0 or x >= len(gameArray[0]) or \
               (gameArray[y][x] != backgroundPixel and [y, x] not in block.CoordinateList):
                return endCoords  
        endCoords = newEndCoords 

def CheckLoss():
    for i in range(len(gameArray[0])):
        if gameArray[0][i] != backgroundPixel and [0, i] not in block.CoordinateList:
            return True
    return False

def printGame(z):
    outList = ['\033[H\033[?25l']  
    shadowCoords = calculateEndCoordinates(block)
    tempArray = [[cell for cell in row] for row in gameArray]
    for y, x in shadowCoords:
        if [y, x] not in block.CoordinateList:tempArray[y][x] = f'\033[48;5;240m \033[0m'
    for row in tempArray:
        for cell in row:outList.append(cell * 2) 
        outList.append('\n')
    if z != 1: outList.append(f'Score: {score}\n')
    else:outList.append(f'Your Final Score was: {score}\n')
    print(''.join(outList))


gameRun = True
spawnXcoordinateList = [[0, 1, 0, 1], [0, 1, 2, 1], [0, 1, 1, 2], [0, 0, 0, 1], [0, 1, 1, 2], [0, 1, 1, 1], [0, 0, 0, 0]]
spawnYcoordinateList = [[0, 0, 1, 1], [0, 0, 0, 1], [0, 0, 1, 1], [0, 1, 2, 2], [0, 0, 1, 1], [0, 0, 1, 2], [0, 1, 2, 3]]
background = [1, 1, 1]
colorDict =  {'Red': 9, 'Green': 46, 'Yellow': 226, 'Blue': 26, 'Orange': 208}
TypeList = ['Oblock', 'Tblock', 'Zblock', 'Lblock', 'Sblock', 'Jblock', 'Iblock']
backgroundPixel = f'\033[48;2;{background[0]};{background[1]};{background[2]}m \033[0m'
while gameRun == True:    
    print("\033[2J" + "\033[H" + '\033[?25l')
    gameArray = [[backgroundPixel for _ in range(14)] for _ in range(20)]
    score = 0
    PrevColorIndex = randint(0, len(colorDict) - 1)
    PrevColor = list(colorDict.keys())[PrevColorIndex]
    block = createNewBlock()
    while True and (gameRun == True):
        if CheckLoss():break
        sleep(.09)
        if not block.updateBlock('down'):
            clearFullRow()
            del block
            block = createNewBlock()
            score += 1
        printGame(0)
        if kbhit():
            key = getch().decode()
            inStr={'a':'left','d':'right','c':'Sright','z':'Sleft','m':'cc','n':'c','b':'slam'}.get(key)
            if inStr != None: block.updateBlock(inStr)
            elif key == 'r':break
            elif key == 'q':gameRun = False                
            while kbhit():getch()
        print("\033[K", end='') 
    if gameRun:
        printGame(1)
        print("Restarting Game....")
        sleep(1)
    else:print("Program Ended")  



