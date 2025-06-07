#                                                                        VERSION 1:
from msvcrt import kbhit, getch;dx, dy, food, snake,definition,pixel,h,w,_ = 1, 0, [2, 2], [[9, 9]],2,'\033[48;5;{}m \033[0m',10,20,print("\033[2J")    #function import & variable declaration 
while True:                                                                                                                                             #initiate game 
    if kbhit() and (b := {'w': (0, -1), 's': (0, 1), 'a': (-1, 0), 'd': (1, 0)}.get(getch().decode())) and b and (dx, dy) != (-b[0], -b[1]): dx, dy = b #user input & direction updating
    if (head:=[snake[0][0] + dx, snake[0][1] + dy]) in snake or not 0 <= head[0] < w or not 0 <= head[1] < h: break                                     #collision detection
    from random import randint; snake, food = ([head] + snake, [randint(0, w-1), randint(0, h-1)]) if head == food else ([head] + snake[:-1], food)     #function import & snake movement & food generation
    print("\033[H"+'\n'.join(''.join(pixel.format(10 if [x,y] in snake else 1 if [x,y] == food else 8)*definition for x in range(w)) for y in range(h))) #screen print
    from time import sleep; sleep(0.08 if abs(dy) else 0.04)         


'''                VERSION 2:
from random import randint 
from msvcrt import kbhit, getch
from time import sleep 
dx, dy, food, snake,definition,pixel,GameHeight,GameWidth = 1, 0, [1, 1], [[9, 9]],2,'\033[48;5;{}m \033[0m',10,20
print("\033[2J") 
while True:
    if kbhit(): 
        b = {'w': (0, -1), 's': (0, 1), 'a': (-1, 0), 'd': (1, 0)}.get(getch().decode())  
        if b and (dx, dy) != (-b[0], -b[1]): dx, dy = b 
    head = [snake[0][0] + dx, snake[0][1] + dy] 
    if head in snake or not 0 <= head[0] < GameWidth or not 0 <= head[1] < GameHeight: break 
    snake.insert(0, head) 
    if head == food: food = [randint(0,GameWidth-1), randint(0,GameHeight-1)] 
    else: snake.pop(-1)
    print("\033[H" + '\n'.join(''.join(pixel.format(10 if [x, y] in snake else 1 if [x, y] == food else 8) * definition for x in range(GameWidth)) for y in range(GameHeight)))
    sleep(0.08 if abs(dy) else 0.04)
'''
