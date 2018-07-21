from fractions import Fraction
from math import *
pocket = 1000
class bet:
    def __init__(self,p,w,o,a,b,c):
        self.p=int(p)
        self.w=w
        self.o=o
        self.a=int(a)
        self.b=int(b)
        self.c=int(c)
        self.rate=(self.w/self.p)*100
    def __str__(self):
        return "[bet game:{:d},earn:{:f}%,pay:{:d},win:{:f},(a:{:d},b:{:d},c:{:d})]".format(self.o,self.rate,self.p,self.w,self.a,self.b,self.c)
def calc(p,a,b,c):
    d,e,f = (1/a,1/b,1/c)
    g = 1-(d+e+f)
    h = (d+e+f)
    if g < 0 :
        return 0.0,0.0,0.0,0.0,0.0;
    else:
        fpa = p*d/h
        fga = fpa*a
        fpb = p*e/h
        fgb = fpb*b
        fpc = p*f/h
        fgc = fpc*c
        p=round(fpa)+round(fpb)+round(fpc)
        mingain = min(round(fpa)*a,round(fpb)*b,round(fpc)*c)
        maxloss = max((fpa-round(fpa))*a,(fpb-round(fpb))*b,(fpc-round(fpc))*c,(round(fpa)-fpa)*a,(round(fpb)-fpb)*b,(round(fpc)-fpc)*c)
        return mingain-p,round(fpa),round(fpb),round(fpc),maxloss
def calc_pocket(p,a,b,c):
    cwin,betsize,beta,betb,betc,mloss = 0.0,0.0,0.0,0.0,0.0,p+1.0
    for x in range(3,p):
        win,abet,bbet,cbet,maxloss = calc(x,a,b,c)
        if cwin<win and mloss>maxloss:
            cwin,betsize,beta,betb,betc,mloss = win,(abet+bbet+cbet),abet,bbet,cbet,maxloss
    return cwin,betsize,beta,betb,betc,mloss
def multiple_game_naive(odds, p):
    bets=[]
    for j in range(0,len(odds)):
        cwin,betsize,a,b,c,_ = calc_pocket(p,float(odds[j][0]),float(odds[j][1]),float(odds[j][2]))
        if cwin>0:
            bets.append(bet(betsize,cwin,j,a,b,c))
    return bets
def multiple_game(odds, p):
    print "\nStrategy for {:d} games with ${:d}:\n".format(len(odds),p),odds
    print
    strategy=[]
    bets=multiple_game_naive(odds,p)
    bets=sorted(bets,key=lambda x:x.rate,reverse=True)
    pay,win,game,a,b,c = 0.0,0.0,0.0,0.0,0.0,0.0
    while p>0 and len(bets)>0:
        if p-bets[0].p>0:
            p=p-bets[0].p
            pay=pay+bets[0].p
            win=win+bets[0].w
            game=bets[0].o
            a=a+bets[0].a
            b=b+bets[0].b
            c=c+bets[0].c

        else:
            if pay>0:
                strategy.append(bet(pay,win,game,a,b,c))
            pay,win,game,a,b,c = 0.0,0.0,0.0,0.0,0.0,0.0
            bets.pop(0)
    print '\n'.join(str(x) for x in strategy)
    print "\nmake",len(strategy),"bets with $",p,"not used\n"
    earn=0.0
    pay=0
    for s in strategy:
        pay=pay+s.p
        earn=earn+s.w
    print "----------\nUse:${:d},Earn:${:.2f} ({:.1%})\n----------".format(pay,earn,earn/pay)
    return strategy
# array of odds , pocket money
multiple_game([\
[1.87,3.54,5.3],\
[3.32,3.46,2.4],\
[17.5,8.5,1.22],\
[1.4,5.7,9.7],\
], 1000)
#print '\n'.join(str(x) for x in multiple_game([[1.05,51,801],[1.35,8,14],], 1000))

while True:
    a = float(raw_input("\nBet A Odds: "))
    b = float(raw_input("Bet B Odds: "))
    c = float(raw_input("Bet C Odds: "))
    cwin,betsize,beta,betb,betc,mloss = calc_pocket(pocket,a,b,c)
    if cwin <= 0:
        print "----------\nNo Bet\n----------"
        continue
    print "\n----------\nMin Profit:\t",cwin,"(",'{:.1%}'.format(cwin/betsize),")"
    print "Bet Size:\t",betsize
    print "----------\nBet A:\t",beta,"(",beta*a,")"
    print "Bet B:\t",betb,"(",betb*b,")"
    print "Bet C:\t",betc,"(",betc*c,")"
