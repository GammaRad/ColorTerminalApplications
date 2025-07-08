from msvcrt import kbhit, getch
from time import sleep as s                            
print("\033[2J" + "\033[H" + '\033[?25l')
w, h,c = 30, 24,0                            
c1= '\033[48;5;8m \033[0m'                            
c2= '\033[48;5;15m \033[0m'                            
c3= '\033[48;5;232m \033[0m'                            
c4= '\033[48;5;1m \033[0m'                              
c5= '\033[48;5;2m \033[0m'                            
c6= '\033[48;5;3m \033[0m'                             
c7= '\033[48;5;18m \033[0m'                              
c8= '\033[48;5;5m \033[0m'                             
c9= '\033[48;5;6m \033[0m'                              
c10= '\033[48;5;7m \033[0m'                             
c11= '\033[48;5;9m \033[0m'                             
c12 = '\033[48;5;10m \033[0m'                             
c13  = '\033[48;5;11m \033[0m'                            
c14 = '\033[48;5;12m \033[0m'                              
c15= '\033[48;5;13m \033[0m'                            
c16= '\033[48;5;14m \033[0m' 
c17='\033[48;2;230;211;151m \033[0m' 
c18='\033[48;2;151;194;230m \033[0m' 

continousDraw = False
continousErase = False
if input('Wanna load from saved? ') == 'y': 
    try:
        with open("PixelArtSavedData.txt") as f:gameArray = eval(f.read())
    except FileNotFoundError:
        print("The file that this program saves its data to locally is not found. This message will stay for 7 seconds and then proceed with the program")
        s(7)
        gameArray = [[c1 for _ in range(w)] for _ in range(h)]
else:gameArray = [[c1 for _ in range(w)] for _ in range(h)]
CursorXpos, CursorYpos = 10, 10      
gameArray[CursorYpos][CursorXpos] = c2
print("\033[H" + '\n'.join(''.join(gameArray[y][x] * 2 for x in range(w))for y in range(h)))                                        
paintColor = c3    
ColorList = [c3,c4,c5,c6,c7,c8,c9,c10, c11, c12,c13,c14,c15,c16,c17,c18]                        
while True:
    if kbhit() and (key := getch().decode()) in ['w', 'a', 's', 'd', '.', '/','c','q','l','k']:
        PrevCursorXpos, PrevCursorYpos = CursorXpos, CursorYpos
        if key in ['w', 'a', 's', 'd']:
            if key == 'w': CursorYpos = max(0, CursorYpos - 1)
            elif key == 's': CursorYpos = min(h - 1, CursorYpos + 1)
            elif key == 'a': CursorXpos = max(0, CursorXpos - 1)
            elif key == 'd': CursorXpos = min(w - 1, CursorXpos + 1)
            if gameArray[PrevCursorYpos][PrevCursorXpos] == c2:gameArray[PrevCursorYpos][PrevCursorXpos] = c1
            if gameArray[CursorYpos][CursorXpos] == c1:gameArray[CursorYpos][CursorXpos] = c2
        if key == 'l':continousDraw = not continousDraw
        elif key == 'k':continousErase = not continousErase
        elif key == 'c':                            
            c+=1
            paintColor = ColorList[c%len(ColorList)]
        elif key=='q':break
        elif key == '/' or continousDraw==True:
            gameArray[CursorYpos][CursorXpos] = paintColor
        elif key == '.' or continousErase==True:
            gameArray[CursorYpos][CursorXpos] = c2
        print("\033[H" + '\n'.join(''.join(gameArray[y][x] * 2 for x in range(w))for y in range(h)))    
        print(f'Current Color {paintColor*5},c')
        print(f'continousDraw:{continousDraw},l')
        print(f'continousErase:{continousErase},k') 
outArr = [[0 for _ in range(w)] for _ in range(h)]   
if input('Do you want to save?') == 'y':
    with open("PixelArtSavedData.txt", "w") as f:
        f.write(repr(gameArray))
