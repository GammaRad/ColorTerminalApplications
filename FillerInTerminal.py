print("\033[1;1H\033[2J")
from random import (randint,choice)

ColorList = [
    '\033[48;2;67;64;67m ',   
    '\033[48;2;242;39;111m ', 
    '\033[48;2;242;208;47m ', 
    '\033[48;2;164;218;91m ', 
    '\033[48;2;69;192;238m ', 
    '\033[48;2;100;70;162m '  
]

GameArray = []


def CreateGameArray(w, h):
    global GameArray
    GameArray = [[6 for _ in range(w)] for _ in range(h)]

def CreateRandomBoard():
    print("\033[1;1H")

    for row in range(len(GameArray)):
        for col in range(len(GameArray[row])):
            while True:
                RandNumber = randint(0,5)
                if (col > 0 and RandNumber == GameArray[row][col - 1]) or (row > 0 and RandNumber == GameArray[row - 1][col]):
                    continue
                else:
                    GameArray[row][col] = RandNumber
                    break

def PrintStyledGA():
    global PixelDefinition
    for row in GameArray:
        for number in row:
            print(ColorList[number]*PixelDefinition, end='')
        print('')
    print('\033[0m')  

def GetPlayerColor(x):
    global currentPlayer
    return PlayerColorList[x % 2]

def updatePlayerBoxes(playerNum,colorNum):
    for CoordinateTuple in PlayerBoxes[playerNum]:
        GameArray[CoordinateTuple[0]][CoordinateTuple[1]] = colorNum

def integrateNewBoxes(playerNum):
    new_boxes = set(PlayerBoxes[playerNum])  
    current_color = PlayerColorList[playerNum]
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    while True:
        added_boxes = set()
        for box in new_boxes:  
            for direction in directions:
                new_row, new_col = box[0] + direction[0], box[1] + direction[1]
                if 0 <= new_row < len(GameArray) and 0 <= new_col < len(GameArray[0]):
                    if GameArray[new_row][new_col] == current_color and (new_row, new_col) not in new_boxes:
                        added_boxes.add((new_row, new_col))
        if not added_boxes:  
            break
        new_boxes.update(added_boxes)  
    PlayerBoxes[playerNum] = list(new_boxes)  
    for box in PlayerBoxes[playerNum]:
        GameArray[box[0]][box[1]] = current_color


def GetAdjacentColorCounts(boxes):
    color_counts = [0] * 6
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for box in boxes:
        for direction in directions:
            new_row, new_col = box[0] + direction[0], box[1] + direction[1]
            if 0 <= new_row < len(GameArray) and 0 <= new_col < len(GameArray[0]):
                adjacent_color = GameArray[new_row][new_col]
                if adjacent_color != GetPlayerColor(0) and adjacent_color != GetPlayerColor(1):
                    color_counts[adjacent_color] += 1

    return color_counts

def GetAiMove():
    best_color = None
    best_gain = -1
    opponent_color = GetPlayerColor(0)
    ai_current_color = GetPlayerColor(1)

    for color in range(6):
        if color == ai_current_color or color == opponent_color:
            continue  # Skip colors already occupied by AI or opponent

        # Simulate taking this color
        simulated_boxes = set(PlayerBoxes[1])
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for box in simulated_boxes.copy():
            for direction in directions:
                new_row, new_col = box[0] + direction[0], box[1] + direction[1]
                if 0 <= new_row < len(GameArray) and 0 <= new_col < len(GameArray[0]):
                    if GameArray[new_row][new_col] == color:
                        simulated_boxes.add((new_row, new_col))

        # Calculate potential gain
        gain = len(simulated_boxes) - len(PlayerBoxes[1])

        # Avoid giving the opponent an advantage
        opponent_simulated_boxes = set(PlayerBoxes[0])
        for box in opponent_simulated_boxes.copy():
            for direction in directions:
                new_row, new_col = box[0] + direction[0], box[1] + direction[1]
                if 0 <= new_row < len(GameArray) and 0 <= new_col < len(GameArray[0]):
                    if GameArray[new_row][new_col] == color:
                        gain -= 0.5  # Reduce score if the move benefits the opponent

        # Choose the color with the highest gain
        if gain > best_gain:
            best_gain = gain
            best_color = color

    return best_color if best_color is not None else choice(range(6))  # Fallback choice

def GetAiMove1():
    ai_color_counts = GetAdjacentColorCounts(PlayerBoxes[1])
    opponent_color_counts = GetAdjacentColorCounts(PlayerBoxes[0])
    ai_max_count = max(ai_color_counts)
    opponent_max_count = max(opponent_color_counts)
    if opponent_max_count > ai_max_count:
        best_colors = [i for i, count in enumerate(opponent_color_counts) if count == opponent_max_count]
    else:
        best_colors = [i for i, count in enumerate(ai_color_counts) if count == ai_max_count]
    if len(best_colors) == 1:
        return best_colors[0]
    else:
        return choice(best_colors)

currentPlayer = 0
winningPlayer = None
try:BoardHeight = abs(int(input('How tall is the board?')))
except Exception: BoardHeight = 7
try:BoardWidth = abs(int(input('How wide is the board?')))
except Exception: BoardWidth = 8
try: PixelDefinition = abs(int(input('Pixel Definition?')))
except Exception: PixelDefinition = 3
try:PlayerNumber = abs(int(input('How many players?'))) % 3
except Exception: PlayerNumber = 1
if PixelDefinition == 0:PixelDefinition = 1
if BoardHeight == 0 or BoardHeight == 1:BoardHeight = 2
if BoardWidth == 0 or BoardWidth == 1:BoardWidth = 2



print("\033[1;1H\033[2J")
CreateGameArray(BoardWidth,BoardHeight)
PlayerColorList = [GameArray[len(GameArray) - 1 ][0], GameArray[0][len(GameArray[0]) - 1]]
PlayerBoxes = [[(len(GameArray) - 1 ,0)],[(0,len(GameArray[0]) - 1)]]
CreateRandomBoard()
print('Black 0|Pink 1|Yellow 2|Green 3|Blue 4|Purple 5|End Game -1|Rules -2|')
PrintStyledGA()
print(f'P1 Score:{len(PlayerBoxes[0])} | P2 Score:{len(PlayerBoxes[1])}')

if PlayerNumber != 0:
    while True:
        while True:
            currentPlayerColor = GetPlayerColor(currentPlayer)
            if PlayerNumber == 2 or (currentPlayer % 2) == 0:
                try: colorNum = int(input(f'Player {(currentPlayer % 2) + 1} What color do you want to switch to: '))
                except ValueError:colorNum = currentPlayerColor
                if colorNum == -1:
                    winningPlayer = 0
                    break
                elif colorNum == -2:
                    input('This game is called "Filler". Both players start with 1 conquered box. Player 1\'s starting box is the bottom left box while Player 2\'s starting box is the top right box. Both players take turns picking a color that is not their own, nor the opponents. If any boxes are the same color as the newly changed color, they will become apart of the Player\'s conquered boxes, and will increase the score of the player by how many boxes they conquered. The goal is to capture more boxes then the other player until every box is either conquered by player 1 or 2. Type anything to exit this message') 
                    print('\033[F\033[K', end='') 
                    continue
                elif colorNum < 0 or colorNum > 5:
                    colorNum = currentPlayerColor
            elif PlayerNumber == 1 and (currentPlayer % 2) == 1: 
                _=randint(0,1)
                if _ ==1:colorNum = GetAiMove()
                else: colorNum=GetAiMove1()
        
            
            if colorNum == currentPlayerColor or colorNum == GetPlayerColor(currentPlayer + 1):
                print('\033[F\033[K', end='') 
                continue
            else:
                PlayerColorList[currentPlayer % 2] = colorNum
                updatePlayerBoxes(currentPlayer % 2, PlayerColorList[currentPlayer % 2])
                integrateNewBoxes(currentPlayer % 2)
                currentPlayer += 1
                print('\033[F\033[K', end='')
                break
            
        print("\033[1;1H\033[2J")
        print('Black 0|Pink 1|Yellow 2|Green 3|Blue 4|Purple 5|End Game -1|Rules -2|')
        PrintStyledGA()
        print(f'P1 Score:{len(PlayerBoxes[0])} | P2 Score:{len(PlayerBoxes[1])}')
        if (len(PlayerBoxes[0]) + len(PlayerBoxes[1])) == (len(GameArray) * len(GameArray[0])) or winningPlayer == 0:
            if winningPlayer == 0: 
                print(f"Player {(currentPlayer % 2) + 1} has ended the Game")
                break
            elif len(PlayerBoxes[0]) == len(PlayerBoxes[1]):
                print('Player 1 has tied with Player 2')
                break
            else:
                winningPlayer = 1 if len(PlayerBoxes[0]) > len(PlayerBoxes[1]) else 2
                print(f"Player {winningPlayer} has won. ")
                break
else:
    print("\033[1;1H\033[2J")
    while True:
        PrintStyledGA()
        colorNum = GetAiMove()   
        PlayerColorList[currentPlayer % 2] = colorNum
        updatePlayerBoxes(currentPlayer % 2, PlayerColorList[currentPlayer % 2])
        integrateNewBoxes(currentPlayer % 2)
        currentPlayer += 1
        print(f'P1 Score:{len(PlayerBoxes[0])} | P2 Score:{len(PlayerBoxes[1])}')

        if (len(PlayerBoxes[0]) + len(PlayerBoxes[1])) == (len(GameArray) * len(GameArray[0])):
            print("\033[1;1H")
            PrintStyledGA()
            if winningPlayer == 0: 
                print("\033[2K" + f"Player {(currentPlayer % 2) + 1} has ended the Game")
                print(f'P1 Score:{len(PlayerBoxes[0])} | P2 Score:{len(PlayerBoxes[1])}')
                break
            elif len(PlayerBoxes[0]) == len(PlayerBoxes[1]):
                print("\033[2K" + 'Player 1 has tied with Player 2')
                print(f'P1 Score:{len(PlayerBoxes[0])} | P2 Score:{len(PlayerBoxes[1])}')
                break
            else:
                winningPlayer = 1 if len(PlayerBoxes[0]) > len(PlayerBoxes[1]) else 2
                print("\033[2K" + f"Player {winningPlayer} has won. ")
                print(f'P1 Score:{len(PlayerBoxes[0])} | P2 Score:{len(PlayerBoxes[1])}')
                break
        print("\033[1;1H")
