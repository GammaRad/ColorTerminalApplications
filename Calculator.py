from sympy.parsing.sympy_parser import (parse_expr, standard_transformations ,implicit_multiplication_application,convert_xor, function_exponentiation)
from sympy import evalf
from msvcrt import kbhit, getch

PalleteList = ['\033[48;2;227;9;9m','\033[48;2;0;0;0m','\033[38;2;235;231;14m']
screenArray =[
    [' ','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_',' ',],
    ['|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','C','A','L','C','U','L','A','T','O','R',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|',],
    ['|','~','~','~','~','~','~','~','~','~','~','~','~','~','~','~','~','~','~','~','~','~','~','~','~','~','~','~','~','~','~','~','~','~','~','~','~','~','~','~','|',],
    ['|',' ',' ',' ','|',' ',' ',' ','|',' ',' ',' ','|',' ',' ',' ','|',' ',' ',' ','|',' ',' ',' ','|',' ',' ',' ','|',' ',' ',' ','|',' ',' ',' ','|',' ',' ',' ','|',],
    ['|',' ','0',' ','|',' ','1',' ','|',' ','2',' ','|',' ','3',' ','|',' ','4',' ','|',' ','5',' ','|',' ','6',' ','|',' ','7',' ','|',' ','8',' ','|',' ','9',' ','|',],
    ['|','_','_','_','|','_','_','_','|','_','_','_','|','_','_','_','|','_','_','_','|','_','_','_','|','_','_','_','|','_','_','_','|','_','_','_','|','_','_','_','|',],
    ['|',' ',' ',' ',' ',' ',' ',' ','|',' ',' ',' ',' ',' ',' ',' ','|',' ',' ',' ',' ',' ',' ',' ','|',' ',' ',' ',' ',' ',' ',' ','|',' ',' ',' ',' ',' ',' ',' ','|',],
    ['|',' ',' ',' ','(',' ',' ',' ','|',' ',' ',' ',')',' ',' ',' ','|',' ',' ',' ','^',' ',' ',' ','|',' ',' ',' ','.',' ',' ',' ','|',' ',' ','d','e','l',' ',' ','|',],
    ['|',' ',' ',' ',' ',' ',' ',' ','|',' ',' ',' ',' ',' ',' ',' ','|',' ',' ',' ',' ',' ',' ',' ','|',' ',' ',' ',' ',' ',' ',' ','|',' ',' ',' ',' ',' ',' ',' ','|',],
    ['|','_','_','_','_','_','_','_','|','_','_','_','_','_','_','_','|','_','_','_','_','_','_','_','|','_','_','_','_','_','_','_','|','_','_','_','_','_','_','_','|',],
    ['|',' ',' ',' ',' ',' ',' ',' ','|',' ',' ',' ',' ',' ',' ',' ','|',' ',' ',' ',' ',' ',' ',' ','|',' ',' ',' ',' ',' ',' ',' ','|',' ',' ',' ',' ',' ',' ',' ','|',],
    ['|',' ',' ',' ','+',' ',' ',' ','|',' ',' ',' ','_',' ',' ',' ','|',' ',' ',' ','ˣ',' ',' ',' ','|',' ',' ',' ','÷',' ',' ',' ','|',' ','E','v','a','l',' ',' ','|',],
    ['|',' ',' ',' ',' ',' ',' ',' ','|',' ',' ',' ',' ',' ',' ',' ','|',' ',' ',' ',' ',' ',' ',' ','|',' ',' ',' ',' ',' ',' ',' ','|',' ',' ',' ',' ',' ',' ',' ','|',],
    ['|','_','_','_','_','_','_','_','|','_','_','_','_','_','_','_','|','_','_','_','_','_','_','_','|','_','_','_','_','_','_','_','|','_','_','_','_','_','_','_','|',],
    ['|',' ',' ',' ',' ',' ',' ',' ','|',' ',' ',' ',' ',' ',' ',' ','|','P','R','O','M','P','T',':',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|',],
    ['|',' ',' ','s','i','n',' ',' ','|',' ',' ','c','o','s',' ',' ','|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|',],
    ['|',' ',' ',' ',' ',' ',' ',' ','|',' ',' ',' ',' ',' ',' ',' ','|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|',],
    ['|','_','_','_','_','_','_','_','|','_','_','_','_','_','_','_','|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|',],
    ['|',' ',' ',' ',' ',' ',' ',' ','|',' ',' ',' ',' ',' ',' ',' ','|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|',],
    ['|',' ',' ','t','a','n',' ',' ','|',' ',' ','l','o','g',' ',' ','|','A','N','S','W','E','R',':',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|',],   
    ['|',' ',' ',' ',' ',' ',' ',' ','|',' ',' ',' ',' ',' ',' ',' ','|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|',],
    ['|','_','_','_','_','_','_','_','|','_','_','_','_','_','_','_','|','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','|',],
    ['|',' ',' ',' ',' ',' ',' ',' ','|',' ',' ',' ',' ',' ',' ',' ','|',' ',' ',' ',' ',' ',' ',' ','|',' ',' ',' ',' ',' ',' ',' ','|',' ',' ',' ',' ',' ',' ',' ','|',],
    ['|',' ','s','i','n','h',' ',' ','|',' ','c','o','s','h',' ',' ','|',' ','t','a','n','h',' ',' ','|',' ','^','(','1','÷',' ',' ','|',' ',' ','a','b','s',' ',' ','|',],
    ['|',' ',' ',' ',' ',' ',' ',' ','|',' ',' ',' ',' ',' ',' ',' ','|',' ',' ',' ',' ',' ',' ',' ','|','n','t','h','r','o','o','t','|',' ',' ',' ',' ',' ',' ',' ','|',],
    ['|','_','_','_','_','_','_','_','|','_','_','_','_','_','_','_','|','_','_','_','_','_','_','_','|','_','_','_','_','_','_','_','|','_','_','_','_','_','_','_','|',],
    ['|',' ',' ',' ',' ',' ',' ',' ','|',' ',' ',' ',' ',' ',' ',' ','|',' ',' ',' ',' ',' ',' ',' ','|',' ',' ',' ',' ',' ',' ',' ','|',' ',' ',' ',' ',' ',' ',' ','|',],
    ['|',' ',' ',' ','e',' ',' ',' ','|',' ',' ',' ','π',' ',' ',' ','|',' ',' ',' ','a',' ',' ',' ','|',' ',' ',' ','!',' ',' ',' ','|',' ',' ',' ','i',' ',' ',' ','|',],
    ['|',' ',' ',' ',' ',' '," ",' ','|',' ',' ','p','i',' ',' ',' ','|','i','n','v','e','r','s','e','|',' ',' ',' ',' ',' ',' ',' ','|','c','o','m','p','l','e','x','|',],
    ['|','_','_','_','_','_','_','_','|','_','_','_','_','_','_','_','|','_','_','_','_','_','_','_','|','_','_','_','_','_','_','_','|','_','_','_','_','_','_','_','|',],
] 
numLParens=0
numRParens=0
cursorXpos = 1
cursorYpos = 2 
MathExpression = ''
PromptIndex = 17  
PromptLevel=15
AnswerIndex = 17
screenArrayLength = len(screenArray)
screenArrayWidth = len(screenArray[0])
button_map = {
    (2, 6): [(0, 4, '0'), (4, 8, '1'), (8, 12, '2'), (12, 16, '3'),(16, 20, '4'), (20, 24, '5'), (24, 28, '6'), (28, 32, '7'),(32, 36, '8'), (36, 40, '9')],
    (5, 10): [(0, 8, '('), (8, 16, ')'), (16, 24, '^'),(24, 32, '.'), (32, 40, 'del')],
    (9, 14): [(0, 8, '+'), (8, 16, '-'), (16, 24, 'ˣ'),(24, 32, '÷'), (32, 40, 'Eval')],
    (13, 18): [(0, 8, 'sin('), (8, 16, 'cos('),],
    (13,19):[ (16, 47, 'clear')],
    (17, 22): [(0, 8, 'tan('), (8, 16, 'log('),],
    (18,22):[ (16, 47, 'PrevAnswer')],
    (21, 26): [(0, 8, 'sinh('), (8, 16, 'cosh('), (16, 24, 'tanh('),(24, 32, '^(1÷'), (32, 40, 'abs(')],
    (25, 30): [(0, 8, 'e'), (8, 16, 'π'), (16, 24, 'a'),(24, 32, '!'), (32, 40, 'i')]}

def updateScreenArray(moveCursorToTop):
    screenBufferList=[]
    print('\033[?25l',end='')
    if moveCursorToTop == True:print(f"\033[{screenArrayLength+1}F\n", end="") #do +2 instead of +1 if the last print statement at the end of this function is uncommented
    a = 0
    while a < screenArrayLength:
        for idx, element in enumerate(screenArray[a]):
            if a == cursorYpos and idx == cursorXpos:screenBufferList.append(f'{PalleteList[0]} {PalleteList[2]}\033[0m')
            else:screenBufferList.append(element)
        screenBufferList.append('\n')
        a += 1
    for i in screenBufferList:
        print(i,end='')

    #print('\033[K')

def evaluate_expression(expr):
    expr = expr.replace('÷', '/')
    expr = expr.replace('ˣ', '*')
    expr = expr.replace('e', '2.71828182845904523536028747')
    expr = expr.replace('π', '3.14159265358979323846264338')
    try:
        _=list(expr).index('I')
        expr = expr.replace('i', 'I')
    except ValueError:
        pass
    transformations = standard_transformations + (implicit_multiplication_application,convert_xor,function_exponentiation)
    try:
        parsed = parse_expr(expr, transformations=transformations, evaluate=True)
        result = parsed.evalf()
        exponent = 0
        if 'e' in str(result):
            try:exponent= int(str(result).split('e')[1])
            except ValueError:pass
        
        return str(result) if exponent >-10 else '0'
    except Exception as e:pass

def getCharacter():
    for (ymin, ymax), entries in button_map.items():
        if ymin < cursorYpos < ymax:
            for xmin, xmax, char in entries:
                if xmin < cursorXpos < xmax:
                    return char
    return 'NotInBox'

print('\033[2J')
print('\033[0;0H')
print("Use 'a' to type inverse trig functions. Eg: asin=inverse sin,atan=inverse tangent,acosh=inverse hyperbolic cosine")
print("The ! operator is the factorial operator exteneded to the reals excluding neagtive integers (Pi function)")
print("The log function is in base e (natural log)")
print("WASD to move cursor. Enter or q to select button.")
print("Eval:e Del:x Off:o Append Needed Parentheses: ` (un shifted ~ key)")
print("Selecting the answer will append the answer into the prompt")
print("Selecting the prompt will clear the prompt")
CursorUp=lambda y:y-1 if y>1 else y
CursorDown=lambda y:y+1 if y < screenArrayLength - 1 else y
CursorLeft=lambda x:x-1 if x>1 else x
CursorRight=lambda x:x+1 if x<screenArrayWidth-1 else x
for i in range(screenArrayLength):
    for j in range(screenArrayWidth):
        screenArray[i][j]=f"{PalleteList[1]}{PalleteList[2]}{screenArray[i][j]}\033[0m"

updateScreenArray(False)

while True:
    if kbhit():
        numLParens=0
        numRParens=0
        for char in MathExpression:
            if char=='(':numLParens+=1
            elif char==')':numRParens+=1
        key = getch().decode()
        if key == 'w':
            if cursorYpos==1:cursorYpos=screenArrayLength-1
            else: cursorYpos = CursorUp(cursorYpos)
        elif key == 'a':
           if cursorXpos ==1:cursorXpos=39
           else:cursorXpos=CursorLeft(cursorXpos)
        elif key == 's':
           if cursorYpos==screenArrayLength-1:cursorYpos=1
           else:cursorYpos=CursorDown(cursorYpos)
        elif key == 'd':
           if cursorXpos==39:cursorXpos=1
           else:cursorXpos= CursorRight(cursorXpos)
        elif key =='o':break
        elif key == '\r' or key == 'q' or key=='e' or key =='x' or key=='`':
            character = getCharacter()
            if character=='NotInBox' and key!='`':continue
            if character == 'del' or key=='x':
                if PromptIndex>17:
                    MathExpression = MathExpression[:-1]
                    screenArray[PromptLevel][PromptIndex - 1] = f"{PalleteList[1]}{PalleteList[2]} \033[0m"
                    PromptIndex -=1
                elif PromptIndex==17:
                    if PromptLevel>15:
                        PromptLevel-=1
                        PromptIndex = 39
                        MathExpression = MathExpression[:-1]
                        screenArray[PromptLevel][PromptIndex - 1] =f"{PalleteList[1]}{PalleteList[2]} \033[0m"
            elif character == 'Eval' or key=='e':
                try:
                    if MathExpression=='ERROR':continue
                    answer = evaluate_expression(MathExpression).replace('I', 'i').replace('*',"")
                    answerList = list(answer)
                    for i in range(17, screenArrayWidth-1):screenArray[20][i] = f"{PalleteList[1]}{PalleteList[2]} \033[0m"
                    AnswerIndex = 17
                    for char in answerList:
                        if AnswerIndex < len(screenArray[20]):
                            screenArray[20][AnswerIndex] =PalleteList[1] + PalleteList[2] + char+'\033[0m'
                            AnswerIndex += 1
                    MathExpression = ''
                    for j in range(15,19):
                        for i in range(17, screenArrayWidth-1):screenArray[j][i] = f"{PalleteList[1]}{PalleteList[2]} \033[0m"
                        PromptIndex = 17
                        PromptLevel=15
                except Exception:pass
            elif character == 'PrevAnswer':
                for char in answerList:
                    if PromptIndex < screenArrayWidth - 2: 
                        screenArray[PromptLevel][PromptIndex] = PalleteList[1] + PalleteList[2] + char +'\033[0m'
                        MathExpression += char
                        PromptIndex += 1
                    elif PromptLevel <18:
                        PromptLevel+=1
                        PromptIndex=17
                        screenArray[PromptLevel][PromptIndex] = PalleteList[1] + PalleteList[2] + char+'\033[0m'
                        MathExpression += char
            elif character=='clear':
                for j in range(15,19):
                    for i in range(17, screenArrayWidth-1):screenArray[j][i] = f"{PalleteList[1]}{PalleteList[2]} \033[0m"
                    PromptIndex = 17
                    PromptLevel=15
                MathExpression=''
            elif (len(character) >= 3) or key=='`':
                if key=='`':character=')'*(numLParens-numRParens)
                PromptList = list(character)
                for element in PromptList:
                    if PromptIndex < screenArrayWidth - 2: 
                        screenArray[PromptLevel][PromptIndex] = PalleteList[1] + PalleteList[2] + element+'\033[0m'
                        MathExpression += element
                        PromptIndex += 1
                    elif PromptLevel <18:
                        PromptLevel+=1
                        PromptIndex=17
                        screenArray[PromptLevel][PromptIndex] = PalleteList[1] + PalleteList[2] + element+'\033[0m'
                        PromptIndex+=1
                        MathExpression += element
                
            elif (key=='\r' or key =='q') and character != 'NotInBox' :
                MathExpression+=character
                if PromptIndex < screenArrayWidth - 2: 
                    screenArray[PromptLevel][PromptIndex] = PalleteList[1] + PalleteList[2] + character+'\033[0m'
                    PromptIndex += 1
                elif PromptLevel <18:
                    PromptLevel+=1
                    PromptIndex=17
                    screenArray[PromptLevel][PromptIndex] = PalleteList[1] + PalleteList[2] + character +'\033[0m'
                    PromptIndex+=1
        updateScreenArray(True)


print('\033[?25h\033[0m')#Show Cursor+Reset ANSI formatting
