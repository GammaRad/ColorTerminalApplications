from sympy.parsing.sympy_parser import (parse_expr, standard_transformations ,implicit_multiplication_application,convert_xor, function_exponentiation)
from sympy import evalf
from msvcrt import kbhit, getch
cursorXpos = 1
cursorYpos = 2 
MathExpression = ''
PromptIndex = 17  
PromptLevel=15
AnswerIndex = 17
PalleteList = ['\033[48;2;227;9;9m','\033[48;2;0;0;0m','\033[38;2;235;231;14m']
screenArray =[
    [f'{PalleteList[1]} {PalleteList[2]}','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_',' ',],
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
    ['|',' ',' ',' ',' ',' ',' ',' ','|',' ',' ',' ',' ',' ',' ',' ','|','A','N','S','W','E','R',':',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|',],
    ['|',' ',' ','t','a','n',' ',' ','|',' ',' ','l','o','g',' ',' ','|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|',],   
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
screenArrayLength = len(screenArray)
screenArrayWidth = len(screenArray[0])

def updateScreenArray(moveCursorToTop):
    screenBufferList=[]
    print('\033[?25l',end='')
    if moveCursorToTop == True:print(f"\033[{screenArrayLength+1}F\n", end="") #do +2 instead of +1 if the last print statement at the end of this function is uncommented
    a = 0
    while a < screenArrayLength:
        for idx, element in enumerate(screenArray[a]):
            if a == cursorYpos and idx == cursorXpos:screenBufferList.append(f'{PalleteList[0]} {PalleteList[2]}'+PalleteList[1])
            else:screenBufferList.append(element)
        screenBufferList.append('\n')
        a += 1
    for i in screenBufferList:
        print(i,end='')
    #print('\033[K'+MathExpression)


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
    if cursorYpos > 2 and cursorYpos < 6:
        if cursorXpos > 0 and cursorXpos < 4: return '0'
        elif cursorXpos > 4 and cursorXpos < 8: return '1'
        elif cursorXpos > 8 and cursorXpos < 12: return '2'
        elif cursorXpos > 12 and cursorXpos < 16: return '3'
        elif cursorXpos > 16 and cursorXpos < 20: return '4'
        elif cursorXpos > 20 and cursorXpos < 24: return '5'
        elif cursorXpos > 24 and cursorXpos < 28: return '6'
        elif cursorXpos > 28 and cursorXpos < 32: return '7'
        elif cursorXpos > 32 and cursorXpos < 36: return '8'
        elif cursorXpos > 36 and cursorXpos < 40: return '9'
    elif cursorYpos > 5 and cursorYpos < 10:
        if cursorXpos > 0 and cursorXpos < 8: return '('
        elif cursorXpos > 8 and cursorXpos < 16: return ')'
        elif cursorXpos > 16 and cursorXpos < 24: return '^'
        elif cursorXpos > 24 and cursorXpos < 32: return '.'
        elif cursorXpos > 32 and cursorXpos < 40: return 'del'
    elif cursorYpos > 9 and cursorYpos < 14:
        if cursorXpos > 0 and cursorXpos < 8: return '+'
        elif cursorXpos > 8 and cursorXpos < 16: return '-'
        elif cursorXpos > 16 and cursorXpos < 24: return 'ˣ'
        elif cursorXpos > 24 and cursorXpos < 32: return '÷'
        elif cursorXpos > 32 and cursorXpos < 40: return 'Eval'
    elif cursorYpos > 13 and cursorYpos < 18:
        if cursorXpos > 0 and cursorXpos < 8: return 'sin'
        elif cursorXpos > 8 and cursorXpos < 16: return 'cos'
        elif cursorXpos > 16 and cursorXpos < 47: return 'clear'
    elif cursorYpos > 17 and cursorYpos < 22:
        if cursorXpos > 0 and cursorXpos < 8: return 'tan'
        elif cursorXpos > 8 and cursorXpos < 16: return 'log'
        elif cursorXpos > 16 and cursorXpos < 47: return 'PrevAnswer'
    elif cursorYpos > 21 and cursorYpos < 26:
        if cursorXpos > 0 and cursorXpos < 8: return 'sinh'
        elif cursorXpos > 8 and cursorXpos < 16: return 'cosh'
        elif cursorXpos > 16 and cursorXpos < 24: return 'tanh'
        elif cursorXpos > 24 and cursorXpos < 32: return '^(1÷'
        elif cursorXpos > 32 and cursorXpos < 40: return 'abs'
    elif cursorYpos > 25 and cursorYpos < 30:
        if cursorXpos > 0 and cursorXpos < 8: return 'e'
        elif cursorXpos > 8 and cursorXpos < 16: return 'π'
        elif cursorXpos > 16 and cursorXpos < 24: return 'a'
        elif cursorXpos > 24 and cursorXpos < 32: return '!'
        elif cursorXpos > 32 and cursorXpos < 40: return 'i'
    return 'NotInBox'

print('\033[2J')
print('\033[0;0H')
print("Use Parentheses for operation precedence.")
print("Use 'a' to type inverse trig functions. Eg: asin,atan,acosh")
print("The ! operator is the factorial operator exteneded to the reals excluding neagtive integers (Pi function)")
print("The log function is in base e (natural log)")
print("WASD to move cursor. Enter or q to select button. Eval:e Del:x Off:o")
updateScreenArray(False)
CursorUp=lambda y:y-1 if y>1 else y
CursorDown=lambda y:y+1 if y < screenArrayLength - 1 else y
CursorLeft=lambda x:x-1 if x>1 else x
CursorRight=lambda x:x+1 if x<screenArrayWidth-1 else x
while True:
    if kbhit():
        key = getch().decode()
        if key == 'w':
           cursorYpos = CursorUp(cursorYpos)
        elif key == 'a':
           cursorXpos=CursorLeft(cursorXpos)
        elif key == 's':
           cursorYpos=CursorDown(cursorYpos)
        elif key == 'd':
           cursorXpos= CursorRight(cursorXpos)
        elif key =='o':break
        elif key == '\r' or key == 'q' or key=='e' or key =='x':
            character = getCharacter()
            if character=='NotInBox':continue
            if character == 'del' or key=='x':
                if PromptIndex>17:
                    MathExpression = MathExpression[:-1]
                    screenArray[PromptLevel][PromptIndex - 1] = f'{PalleteList[1]} '
                    PromptIndex -=1
                elif PromptIndex==17:
                    if PromptLevel>15:
                        PromptLevel-=1
                        PromptIndex = 39
                        MathExpression = MathExpression[:-1]
                        screenArray[PromptLevel][PromptIndex - 1] = f'{PalleteList[1]} '

            elif character == 'Eval' or key=='e':
                try:
                    if MathExpression=='ERROR':continue
                    answer = evaluate_expression(MathExpression).replace('I', 'i').replace('*',"")
                    answerList = list(answer)
                    for i in range(17, screenArrayWidth-1):screenArray[20][i] = ' '
                    AnswerIndex = 17
                    for char in answerList:
                        if AnswerIndex < len(screenArray[20]):
                            screenArray[20][AnswerIndex] = char
                            AnswerIndex += 1
                    MathExpression = ''
                    for j in range(15,18):
                        for i in range(17, screenArrayWidth-1):screenArray[j][i] = ' '
                        PromptIndex = 17
                        PromptLevel=15
                except Exception:pass
            elif character == 'PrevAnswer':
                for char in answerList:
                    if PromptIndex < screenArrayWidth - 2: 
                        screenArray[PromptLevel][PromptIndex] = PalleteList[1] + PalleteList[2] + char
                        MathExpression += char
                        PromptIndex += 1
                    elif PromptLevel <18:
                        PromptLevel+=1
                        PromptIndex=17
                        screenArray[PromptLevel][PromptIndex] = PalleteList[1] + PalleteList[2] + char
                        MathExpression += char
            elif character=='clear':
                for j in range(15,18):
                    for i in range(17, screenArrayWidth-1):screenArray[j][i] = ' '
                    PromptIndex = 17
                    PromptLevel=15
                MathExpression=''
            elif len(character) >= 3:
                PromptList = list(character)
                for element in PromptList:
                    if PromptIndex < screenArrayWidth - 2: 
                        screenArray[PromptLevel][PromptIndex] = PalleteList[1] + PalleteList[2] + element
                        MathExpression += element
                        PromptIndex += 1
                    elif PromptLevel <18:
                        PromptLevel+=1
                        PromptIndex=17
                        screenArray[PromptLevel][PromptIndex] = PalleteList[1] + PalleteList[2] + element
                        MathExpression += element
            elif (key=='\r' or key =='q') and character != 'NotInBox' :
                MathExpression+=character
                if PromptIndex < screenArrayWidth - 2: 
                    screenArray[PromptLevel][PromptIndex] = PalleteList[1] + PalleteList[2] + character
                    PromptIndex += 1
                elif PromptLevel <18:
                    PromptLevel+=1
                    PromptIndex=17
                    screenArray[PromptLevel][PromptIndex] = PalleteList[1] + PalleteList[2] + character
                    PromptIndex+=1
        updateScreenArray(True)
