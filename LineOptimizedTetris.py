from random import randint as R;from time import sleep as S;from msvcrt import kbhit as H,getch as G
SX=[[0,1,0,1],[0,1,2,1],[0,1,1,2],[0,0,0,1],[0,1,1,2],[0,1,1,1],[0,0,0,0]];SY=[[0,0,1,1],[0,0,0,1],[0,0,1,1],[0,1,2,2],[0,0,1,1],[0,0,1,2],[0,1,2,3]]
CD={'R':9,'G':46,'Y':226,'B':26,'O':208};TL=['O','T','Z','L','S','J','I'];BG=f'\033[48;2;1;1;1m \033[0m';SH=f'\033[48;5;240m \033[0m';GR=1
class B:
 def __init__(s,c,t):s.c=CD[c];s.t=TL.index(t);s.p=[]
 def sp(s,y,x):
  for i in range(4):ny,nx=y+SY[s.t][i],x+SX[s.t][i];s.p.append([ny, nx])
  for y, x in s.p:GA[y][x]=f'\033[48;5;{s.c}m \033[0m'
 def fc(s,d):o={'d':(0,1),'r':(1,0),'l':(-1,0),'R':(2,0),'L':(-2,0)}.get(d);return[[y+o[1],x+o[0]]for y,x in s.p if[y+o[1],x+o[0]]not in s.p]
 def mv(s,d):
  if d in'dlrRL':
   oy,ox,f=(0,-2,s.fc(d))if d=='L'else(0,2,s.fc(d))if d=='R'else(1,0,s.fc(d))if d=='d'else(0,-1,s.fc(d)) if d=='l' else(0,1,s.fc(d))
   for y,x in f:
    if y>=20 or x<0 or x>=14 or GA[y][x]!=BG:return s.mv('l')if d=='L'else s.mv('r')if d=='R'else 0
   for y,x in s.p:GA[y][x]=BG
   s.p=[[y+oy,x+ox]for y,x in s.p]
   for y,x in s.p:GA[y][x]=f'\033[48;5;{s.c}m \033[0m'
   return 1
  else:
   if TL[s.t]=='O' or len(s.p)<2: return 0
   py,px=s.p[1]
   np=[[py+x-px,px-y+py]if d=='c'else[py-x+px,px+y-py]for y,x in s.p]
   for ny,nx in np:
     if [ny,nx] not in s.p and (ny<0 or ny>=20 or nx<0 or nx>=14 or GA[ny][nx]!=BG): return 0
   for y,x in s.p: GA[y][x]=BG
   s.p=np
   for y,x in s.p: GA[y][x]=f'\033[48;5;{s.c}m \033[0m'
   return 1
def sh(b:B):
  s=[p[:]for p in b.p]
  while 1:
    if any(y>=20 or x<0 or x>=14 or(GA[y][x]!=BG and[y,x]not in b.p)for y,x in ([[y+1,x]for y,x in s])):return s
    s=[[y+1,x]for y,x in s]
def pr(z):print("\033[H\033[?25l");tmp=[[c for c in r]for r in GA];[(lambda y,x:tmp[y].__setitem__(x,SH))(y,x)for y,x in sh(blk)if[y,x]not in blk.p];[print(''.join(c*2 for c in r))for r in tmp];print(f'Score: {SC}'if not z else f'Final Score: {SC}')
while GR:
 print("\033[2J\033[H\033[?25l");GA=[[BG]*14 for _ in range(20)];SC=0;blk=B(list(CD)[R(0,len(CD)-1)],TL[R(0,len(TL)-1)]);blk.sp(0, 4)
 while True and GR:
  if any(GA[0][i]!=BG and [0,i] not in blk.p for i in range(14)):break
  S(.11)
  if not blk.mv('d'):[(GA.__setitem__(i,[BG]*14),[GA.__setitem__(r,GA[r-1][:])for r in range(i,0,-1)],GA.__setitem__(0,[BG]*14),SC:=SC+9)for i in range(20)if all(c!=BG for c in GA[i])];blk=B(list(CD)[R(0,len(CD)-1)],TL[R(0,len(TL)-1)]);blk.sp(0, 4);SC+=1
  pr(0)
  if H():
   k=G().decode();m={'a':'l','d':'r','c':'R','z':'L','m':'cc','n':'c'}.get(k);blk.mv(m)if m else(GR:=k!='q')
   if k=='r':break
 if GR:pr(1);print("Restarting...");S(1)
print("Program Ended")

