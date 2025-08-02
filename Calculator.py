from sympy.parsing.sympy_parser import (parse_expr, standard_transformations ,implicit_multiplication_application,convert_xor) #used for actually evaluating the math expression
from msvcrt import kbhit, getch #used for getting live user input
screenArray =[
    [' ','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_',' ','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_',' '],
    ['|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','C','A','L','C','U','L','A','T','O','R',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|',' ',' ',' ',' ',' ',' ','A','N','S','W','E','R',' ','L','O','G',' ',' ',' ',' ',' ',' ',' ','|'],
    ['|','~','~','~','~','~','~','~','~','~','~','~','~','~','~','~','~','~','~','~','~','~','~','~','~','~','~','~','~','~','~','~','~','~','~','~','~','~','~','~','|','~','~','~','~','~','~','~','~','~','~','~','~','~','~','~','~','~','~','~','~','~','~','~','|'],
    ['|',' ',' ',' ','|',' ',' ',' ','|',' ',' ',' ','|',' ',' ',' ','|',' ',' ',' ','|',' ',' ',' ','|',' ',' ',' ','|',' ',' ',' ','|',' ',' ',' ','|',' ',' ',' ','|','A','N','S','W','E','R',':',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|'],
    ['|',' ','0',' ','|',' ','1',' ','|',' ','2',' ','|',' ','3',' ','|',' ','4',' ','|',' ','5',' ','|',' ','6',' ','|',' ','7',' ','|',' ','8',' ','|',' ','9',' ','|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|'],
    ['|','_','_','_','|','_','_','_','|','_','_','_','|','_','_','_','|','_','_','_','|','_','_','_','|','_','_','_','|','_','_','_','|','_','_','_','|','_','_','_','|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|'],
    ['|',' ',' ',' ',' ',' ',' ',' ','|',' ',' ',' ',' ',' ',' ',' ','|',' ',' ',' ',' ',' ',' ',' ','|',' ',' ',' ',' ',' ',' ',' ','|',' ',' ',' ',' ',' ',' ',' ','|','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','|'],
    ['|',' ',' ',' ','(',' ',' ',' ','|',' ',' ',' ',')',' ',' ',' ','|',' ',' ',' ','^',' ',' ',' ','|',' ',' ',' ','.',' ',' ',' ','|',' ',' ','d','e','l',' ',' ','|','A','N','S','W','E','R',':',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|'],
    ['|',' ',' ',' ',' ',' ',' ',' ','|',' ',' ',' ',' ',' ',' ',' ','|',' ',' ',' ',' ',' ',' ',' ','|',' ',' ',' ',' ',' ',' ',' ','|',' ',' ',' ',' ',' ',' ',' ','|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|'],
    ['|','_','_','_','_','_','_','_','|','_','_','_','_','_','_','_','|','_','_','_','_','_','_','_','|','_','_','_','_','_','_','_','|','_','_','_','_','_','_','_','|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|'],
    ['|',' ',' ',' ',' ',' ',' ',' ','|',' ',' ',' ',' ',' ',' ',' ','|',' ',' ',' ',' ',' ',' ',' ','|',' ',' ',' ',' ',' ',' ',' ','|',' ',' ',' ',' ',' ',' ',' ','|','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','|'],
    ['|',' ',' ',' ','+',' ',' ',' ','|',' ',' ',' ','_',' ',' ',' ','|',' ',' ',' ','ˣ',' ',' ',' ','|',' ',' ',' ','÷',' ',' ',' ','|',' ','E','v','a','l',' ',' ','|','A','N','S','W','E','R',':',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|'],
    ['|',' ',' ',' ',' ',' ',' ',' ','|',' ',' ',' ',' ',' ',' ',' ','|',' ',' ',' ',' ',' ',' ',' ','|',' ',' ',' ',' ',' ',' ',' ','|',' ',' ',' ',' ',' ',' ',' ','|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|'],
    ['|','_','_','_','_','_','_','_','|','_','_','_','_','_','_','_','|','_','_','_','_','_','_','_','|','_','_','_','_','_','_','_','|','_','_','_','_','_','_','_','|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|'],
    ['|',' ',' ',' ',' ',' ',' ',' ','|',' ',' ',' ',' ',' ',' ',' ','|','P','R','O','M','P','T',':',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','|'],
    ['|',' ',' ','s','i','n',' ',' ','|',' ',' ','c','o','s',' ',' ','|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|','A','N','S','W','E','R',':',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|'],
    ['|',' ',' ',' ',' ',' ',' ',' ','|',' ',' ',' ',' ',' ',' ',' ','|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|'],
    ['|','_','_','_','_','_','_','_','|','_','_','_','_','_','_','_','|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|'],
    ['|',' ',' ',' ',' ',' ',' ',' ','|',' ',' ',' ',' ',' ',' ',' ','|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','|'],
    ['|',' ',' ','t','a','n',' ',' ','|',' ',' ','l','o','g',' ',' ','|','A','N','S','W','E','R',':',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|','A','N','S','W','E','R',':',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|'],   
    ['|',' ',' ',' ',' ',' ',' ',' ','|',' ',' ',' ',' ',' ',' ',' ','|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|'],
    ['|','_','_','_','_','_','_','_','|','_','_','_','_','_','_','_','|','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|'],
    ['|',' ',' ',' ',' ',' ',' ',' ','|',' ',' ',' ',' ',' ',' ',' ','|',' ',' ',' ',' ',' ',' ',' ','|',' ',' ',' ',' ',' ',' ',' ','|',' ',' ',' ',' ',' ',' ',' ','|','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','|'],
    ['|',' ','s','i','n','h',' ',' ','|',' ','c','o','s','h',' ',' ','|',' ','t','a','n','h',' ',' ','|',' ','^','(','1','÷',' ',' ','|',' ',' ','a','b','s',' ',' ','|','A','N','S','W','E','R',':',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|'],
    ['|',' ',' ',' ',' ',' ',' ',' ','|',' ',' ',' ',' ',' ',' ',' ','|',' ',' ',' ',' ',' ',' ',' ','|','n','t','h','r','o','o','t','|',' ',' ',' ',' ',' ',' ',' ','|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|'],
    ['|','_','_','_','_','_','_','_','|','_','_','_','_','_','_','_','|','_','_','_','_','_','_','_','|','_','_','_','_','_','_','_','|','_','_','_','_','_','_','_','|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|'],
    ['|',' ',' ',' ',' ',' ',' ',' ','|',' ',' ',' ',' ',' ',' ',' ','|',' ',' ',' ',' ',' ',' ',' ','|',' ',' ',' ',' ',' ',' ',' ','|',' ',' ',' ',' ',' ',' ',' ','|','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','|'],
    ['|',' ',' ',' ','e',' ',' ',' ','|',' ',' ',' ','π',' ',' ',' ','|',' ',' ',' ','a',' ',' ',' ','|',' ',' ',' ','!',' ',' ',' ','|',' ',' ',' ','i',' ',' ',' ','|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|'],
    ['|',' ',' ',' ',' ',' '," ",' ','|',' ',' ','p','i',' ',' ',' ','|','i','n','v','e','r','s','e','|',' ',' ',' ',' ',' ',' ',' ','|','c','o','m','p','l','e','x','|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|'],
    ['|','_','_','_','_','_','_','_','|','_','_','_','_','_','_','_','|','_','_','_','_','_','_','_','|','_','_','_','_','_','_','_','|','_','_','_','_','_','_','_','|','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','|'],
] 
PalleteList = ['\033[48;2;227;9;9m','\033[48;2;0;0;0m','\033[38;2;235;231;14m','\033[38;2;140;140;140m'] 
numLParens=0
numRParens=0
cursorXpos = 1
cursorYpos = 2 
MathExpression = ''
PromptIndex = 17  
PromptLevel=15
NeededParensIndex=18
NeededParensLevel=15
AnswerIndex = 17
screenArrayLength = len(screenArray)
screenArrayWidth = len(screenArray[0])
answerList=[]
CursorUp=lambda y:y-1 if y>1 else y
CursorDown=lambda y:y+1 if y < screenArrayLength - 1 else y
CursorLeft=lambda x,n:x-n if x-n>0 else x
CursorRight=lambda x,n:x+n if x+n<screenArrayWidth-1 else x
currentParensDiff=0
aStreak=0
dStreak=0
answerLog=[]
button_map = {
    (2, 6): [(0, 4, '0'), (4, 8, '1'), (8, 12, '2'), (12, 16, '3'),(16, 20, '4'), (20, 24, '5'), (24, 28, '6'), (28, 32, '7'),(32, 36, '8'), (36, 40, '9')],
    (5, 10): [(0, 8, '('), (8, 16, ')'), (16, 24, '^'),(24, 32, '.'), (32, 40, 'del')],
    (9, 14): [(0, 8, '+'), (8, 16, '-'), (16, 24, 'ˣ'),(24, 32, '÷'), (32, 40, 'Eval')],
    (13, 18): [(0, 8, 'sin('), (8, 16, 'cos('),],
    (13,19):[ (16, 40, 'clear')],
    (17, 22): [(0, 8, 'tan('), (8, 16, 'log('),],
    (18,22):[ (16, 40, 'PrevAnswer')],
    (21, 26): [(0, 8, 'sinh('), (8, 16, 'cosh('), (16, 24, 'tanh('),(24, 32, '^(1÷'), (32, 40, 'abs(')],
    (25, 30): [(0, 8, 'e'), (8, 16, 'π'), (16, 24, 'a'),(24, 32, '!'), (32, 40, 'i')],
    (2,7):[ (40, 64, 'PrevAnswer0')],
    (6,11):[ (40, 64, 'PrevAnswer1')],
    (10,15):[ (40, 64, 'PrevAnswer2')],
    (14,19):[ (40, 64, 'PrevAnswer3')],
    (18,23):[ (40, 64, 'PrevAnswer4')],
    (22,27):[ (40, 64, 'PrevAnswer5')],
}


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
    #print('\033[K',answerLog)

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
    transformations = standard_transformations + (implicit_multiplication_application,convert_xor)
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
print("WASD to move cursor. Enter or q to select button.")
print("Eval:e Del:x Off:o Append Suggestion Parentheses:f")
print("Selecting the answer will append the answer into the prompt")
print("Selecting the prompt will clear the prompt")
print("Use 'a' to type inverse trig functions. Eg: asin=arcsin,atan=arctan,acosh=arccosh")
print("The ! operator is the factorial operator exteneded to the reals excluding neagtive integers (Pi function)")
print("The log function is in base e (natural log)")
print("Note, please write kˣe or kˣπ to multiply those constants.")

for i in range(screenArrayLength):
    for j in range(screenArrayWidth):
        screenArray[i][j]=f"{PalleteList[1]}{PalleteList[2]}{screenArray[i][j]}\033[0m"

PanelString='Last Updated:August 1st2025 @ 20h:12m:15s EST'
u=27
v=41
for char in PanelString:
    if v<screenArrayWidth-1:
        screenArray[u][v]=PalleteList[1] + PalleteList[2] + char +'\033[0m'
        v+=1
    elif v==64:
        u+=1
        v = 41
        if u==29:break
        screenArray[u][v]=PalleteList[1] + PalleteList[2] + char +'\033[0m'
        v+=1

updateScreenArray(False)

while True:
    if kbhit():
        key = getch().decode()
        if key in ['w','a','s','d','f','x','e','o','\r','q']:
            numLParens=0
            numRParens=0
            for char in MathExpression:
                if char=='(':numLParens+=1
                elif char==')':numRParens+=1
            currentParensDiff=numLParens-numRParens
            if key == 'w':
                aStreak,dStreak=0,0
                if cursorYpos==1:cursorYpos=screenArrayLength-1
                else: cursorYpos = CursorUp(cursorYpos)
            elif key == 'a':
                n=1
                dStreak=0
                if aStreak>=9:n=2
                aStreak+=1
                if cursorXpos-n<1:cursorXpos=screenArrayWidth-2
                else:cursorXpos=CursorLeft(cursorXpos,n)
            elif key == 's':
                aStreak,dStreak=0,0
                if cursorYpos==screenArrayLength-1:cursorYpos=1
                else:cursorYpos=CursorDown(cursorYpos)
            elif key == 'd':
                n=1
                aStreak=0
                if dStreak>=9:n=2
                dStreak+=1
                if cursorXpos+n>=screenArrayWidth-1:cursorXpos=1
                else:cursorXpos= CursorRight(cursorXpos,n)
            elif key =='o':break
            elif key == '\r' or key == 'q' or key=='e' or key =='x' or key=='f':
                aStreak,dStreak=0,0
                character = getCharacter()
                if character=='NotInBox' and key!='f':continue
                if character == 'del' or key=='x' and key !='f' and key!='e':
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
                        answer = evaluate_expression(MathExpression).replace('I', 'i')
                        answerList = list(answer)
                        answerLog.insert(0,answer)
                        if len(answerLog)==7:answerLog.pop()
                        for i in range(len(answerLog)):
                            LogYval=list(button_map.keys())[i+9][0]+2
                            LogXval = 41
                            for p in range(0,2):
                                for k in range(41, 64):screenArray[LogYval+p][k] = f"{PalleteList[1]}{PalleteList[2]} \033[0m"
                            for char in answerLog[i]:
                                if LogXval<screenArrayWidth-1:
                                    screenArray[LogYval][LogXval]=PalleteList[1] + PalleteList[2] + char +'\033[0m'
                                    LogXval+=1
                                elif LogXval==64:
                                    LogYval+=1
                                    LogXval = 41
                                    screenArray[LogYval][LogXval]=PalleteList[1] + PalleteList[2] + char +'\033[0m'
                                    LogXval+=1

                        for i in range(17, 40):screenArray[20][i] = f"{PalleteList[1]}{PalleteList[2]} \033[0m"
                        AnswerIndex = 17
                        for char in answerList:
                            if AnswerIndex < 39:
                                screenArray[20][AnswerIndex] =PalleteList[1] + PalleteList[2] + char+'\033[0m'
                                AnswerIndex += 1
                        MathExpression = ''
                        for j in range(15,19):
                            for i in range(17, 40):screenArray[j][i] = f"{PalleteList[1]}{PalleteList[2]} \033[0m"
                            PromptIndex = 17
                            PromptLevel=15
                    except Exception as e:pass
                elif character.count('PrevAnswer')!=0 and key != 'f' :
                    if (18<cursorYpos<22) and (16<cursorXpos<40): answerList=answerList
                    else:
                        try:answerList=answerLog[int(character[-1])]
                        except IndexError:continue
                    for char in answerList:
                        if PromptIndex < 39: 
                            screenArray[PromptLevel][PromptIndex] = PalleteList[1] + PalleteList[2] + char +'\033[0m'
                            MathExpression += char
                            PromptIndex += 1
                        elif PromptLevel <18:
                            PromptLevel+=1
                            PromptIndex=17
                            screenArray[PromptLevel][PromptIndex] = PalleteList[1] + PalleteList[2] + char+'\033[0m'
                            PromptIndex+=1
                            MathExpression += char
                elif character=='clear' and key!='f':
                    for j in range(15,19):
                        for i in range(17, 40):screenArray[j][i] = f"{PalleteList[1]}{PalleteList[2]} \033[0m"
                        PromptIndex = 17
                        PromptLevel=15
                    MathExpression=''
                elif (len(character) >= 3) or key=='f':
                    if key=='f':character=')'*(currentParensDiff)
                    PromptList = list(character)
                    for element in PromptList:
                        if PromptIndex < 39: 
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
                    if PromptIndex < 39: 
                        screenArray[PromptLevel][PromptIndex] = PalleteList[1] + PalleteList[2] + character+'\033[0m'
                        PromptIndex += 1
                    elif PromptLevel <18:
                        PromptLevel+=1
                        PromptIndex=17
                        screenArray[PromptLevel][PromptIndex] = PalleteList[1] + PalleteList[2] + character +'\033[0m'
                        PromptIndex+=1
            for level in range(15, 19):
                for index in range(17, 40):
                    if screenArray[level][index] == PalleteList[1] + PalleteList[3] + ')' + '\033[0m':
                        screenArray[level][index] = f"{PalleteList[1]}{PalleteList[2]} \033[0m"
            numLParens=0
            numRParens=0
            for char in MathExpression:
                if char=='(':numLParens+=1
                elif char==')':numRParens+=1
            currentParensDiff=numLParens-numRParens
            if currentParensDiff !=0:
                originalPromptIndex = PromptIndex
                originalPromptLevel = PromptLevel
                tempPromptIndex = PromptIndex
                tempPromptLevel = PromptLevel
                for _ in range(currentParensDiff):
                    if tempPromptIndex < 39:
                        screenArray[tempPromptLevel][tempPromptIndex] = PalleteList[1] + PalleteList[3] + ')' + '\033[0m'
                        tempPromptIndex += 1
                    elif tempPromptLevel < 18:
                        tempPromptLevel += 1
                        tempPromptIndex = 17
                        screenArray[tempPromptLevel][tempPromptIndex] = PalleteList[1] + PalleteList[3] + ')' + '\033[0m'
                        tempPromptIndex += 1
                updateScreenArray(True)
                PromptIndex = originalPromptIndex
                PromptLevel = originalPromptLevel
            else:updateScreenArray(True)

print('\033[?25h\033[0m')#Show Cursor+Reset ANSI formatting

