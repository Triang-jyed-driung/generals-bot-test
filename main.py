
import generals
import random
import showui
from showui import GUI
from copy import deepcopy
import sys


def isenemy(yp,xp):
    z = info['tile_grid'][yp][xp]
    return  (z>-1 and z!=info['player_index'])

def accessible(yp,xp):
    z = info['tile_grid'][yp][xp]
    return ((z == -3 or z >=-1) and z!=info['player_index']
        and ( (yp,xp) not in info['cities']) )

def incoord(yp,xp):
    return 0 <= yp < info['rows'] and 0 <= xp < info['cols']

def ismine(yp,xp):
    return info['tile_grid'][yp][xp] == info['player_index']

def takable(y0,x0,dy,dx):
    return ( incoord(y0+dy,x0+dx) 
    and info['tile_grid'][y0][x0] == info['player_index'] 
    and (info['tile_grid'][y0+dy][x0+dx] == info['player_index']
    or (info['tile_grid'][y0+dy][x0+dx] >= -2 
    and info['army_grid'][y0][x0] > info['army_grid'][y0+dy][x0+dx]+1)))

def bfs(q):
    global table
    table=[[1000]*info['cols'] for _ in range(info['rows'])]
    for y,x in q: table[y][x]=0
    while(len(q)>0):
        y1,x1=q.pop(0)
        for dy,dx in P:
            if (0 <= y1+dy < info['rows'] and 0 <= x1+dx < info['cols']):
                z=info['tile_grid'][y1+dy][x1+dx]
                if(z!=-2 and z!=-4
                    and ( (y1+dy, x1+dx) not in info['cities'] or info['tile_grid'][y1+dy][x1+dx]>=0)
                    and table[y1+dy][x1+dx] >table[y1][x1]+1):
                    table[y1+dy][x1+dx] = table[y1][x1]+1
                    q.append( (y1+dy,x1+dx) )
    return table

def collect1(time,q):
    movesteps=[]
    while time>0:
        bfs(deepcopy(q))
        xp=-1
        yp=-1
        armymax=1
        for x0 in range(0,info['cols']):
            for y0 in range(0,info['rows']):
                if (ismine(y0,x0) and (info['army_grid'][y0][x0] > armymax) and (y0,x0 not in q) and (table[y0][x0] <= time) and table[y0][x0]>0):
                    yp,xp,armymax  =  y0,x0,info['army_grid'][y0][x0]
        if(xp==-1): break
        time-=table[yp][xp]
        steptemp=[]
        while table[yp][xp]>0:
            success=False
            for dy,dx in P:
                if incoord(yp+dy,xp+dx) and table[yp+dy][xp+dx] < table[yp][xp]:
                    steptemp.append( (yp,xp,yp+dy,xp+dx) )
                    q.append((yp,xp))
                    xp+=dx
                    yp+=dy
                    success=True
                    break
            if not success:
                print("no")
                break
        movesteps+=steptemp[::-1]
    return movesteps
    
    
def attackdirect():
    pass
def expanddirect():
    pass
def expandindirect():
    pass

roundnum=1
iscommand=False
if len(sys.argv)==2:
    roundnum=int(sys.argv[1])
    iscommand=True

P = [(0, 1), (1, 0), (0, -1), (-1, 0)]
xlast = -2
ylast = -2
move_queue=[]
info=[]
table=[]
ui=None

for oneround in range(0,roundnum):
    g = generals.Generals('SkdijtajO', 'Jordanform', 'ffa', region='std1')
    try:
        steps=[]
        for info in g.get_updates():
            tr=info["turn"]
            print(tr)
            if not iscommand:
                if(tr==1): ui=GUI(info)
                elif tr %5 == 0: ui.updateinfo(info)

            if(tr<=14): continue
            if(tr%50==1 and steps==[]):
                #print(info)
                steps=collect1(22,[info['generals'][info['player_index']]])
                #print(steps)
            #if(mode==2):
            if(len(steps)>0):
                move=steps.pop()
                g.move(move[0],move[1],move[2],move[3])
                continue
            maxscore=-1
            y00,x00,yd0,xd0 = (0,)*4
            for x0 in range(0,info['cols']):
                for y0 in range(0,info['rows']):
                    p=info['tile_grid'][y0][x0]
                    p1=info['army_grid'][y0][x0]
                    for dy,dx in P:
                        if ( 0 <= y0+dy < info['rows'] and 0 <= x0+dx < info['cols']):
                            q=info['tile_grid'][y0+dy][x0+dx]
                            q1=info['army_grid'][y0+dy][x0+dx]
                            if(p == info['player_index']
                            and q != info['player_index']
                            and q >= -1 and p1 > q1 +1):
                                if info['army_grid'][y0+dy][x0+dx]==1: p1+=2
                                if( (y0+dy,x0+dx) in info['generals']): p1+=10000
                                if(p1>maxscore):
                                    y00, x00, yd0, xd0 = y0, x0, y0+dy, x0+dx
                                    maxscore=p1
                                
            if(maxscore>=1): 
                g.move(y00, x00, yd0, xd0)
                xlast,ylast = x00,y00
            else:
                #print("else")
                smax = 0
                xm,ym = -1,-1
                q=[]
                for x0 in range(0,info['cols']):
                    for y0 in range(0,info['rows']):
                        if (accessible(y0,x0)):
                            q.append( (y0,x0) )
                bfs(q)
                #print(table)
                maxq=-100
                
                for x0 in range(0,info['cols']):
                    for y0 in range(0,info['rows']):
                        if ismine(y0,x0):
                            if info['army_grid'][y0][x0] > 1 and info['army_grid'][y0][x0]-table[y0][x0] > maxq:
                                xm = x0
                                ym = y0
                                maxq = info['army_grid'][y0][x0]-table[y0][x0]
                for dy,dx in P:
                    if (incoord(ym+dy,xm+dx)
                        and table[ym+dy][xm+dx] < table[ym][xm]):
                        g.move(ym,xm,ym+dy,xm+dx)
                        ylast,xlast = ym,xm
                        break
                
            
    except KeyError:
        try:
            g.close()
            print(info['replay_url'])
        except NameError:pass
