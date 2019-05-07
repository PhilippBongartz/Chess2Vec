#!/usr/bin/env python
# coding: latin1

import string
import random
import chess
import chess.pgn
import numpy as np
import copy

_name_="Chess2Vec"


# This is some code to turn chessgames into vectors, which can be used for machine learning projects.
# It utilises the chess-module. Game2Vectors(,) takes a path to the pgn and a game number with which to start
# and outputs position, move(as input), move (as output), Elo, Elo difference and Result as vectors. 
# The output format is a list for each game that contains these vectors for each position in the game.
# Positions with black to move are mirrored, so it is always white to move. 



# This extracts moves from a pgn string
def PGNparser(pgnstring):    
    ignore_rund=0
    ignore_schweif=0
    ignore_eckig=0

    # Jetzt schreibe ich den string um, dass nur noch Partiezüge drin sind.
    newpgn=''
    numbers=['0','1','2','3','4','5','6','7','8','9']
    pgnstring=pgnstring+'  '
    for x in range(len(pgnstring)-2):
        if pgnstring[x]=='(':   #Nebenvarianten
            ignore_rund+=1
        if pgnstring[x]=='{':       #Kommentare
            ignore_schweif+=1
        if pgnstring[x]=='[':       #Infos
            ignore_eckig+=1

        if pgnstring[x]==')':
            ignore_rund-=1
        if pgnstring[x]=='}':
            ignore_schweif-=1
        if pgnstring[x]==']':       #Infos
            ignore_eckig-=1
                   
        if not ignore_rund and not ignore_schweif and not ignore_eckig:  # Hier die Züge:
            # Erstmal eliminiere ich die Zugnummern.
            if pgnstring[x]=='.':
                newpgn+=' '
            elif pgnstring[x] in numbers and pgnstring[x+1]=='.':
                pass
            elif pgnstring[x] in numbers and pgnstring[x+1] in numbers and pgnstring[x+2]=='.':
                pass
            elif pgnstring[x] in numbers and pgnstring[x+1] in numbers and pgnstring[x+2] in numbers and pgnstring[x+3]=='.':
                pass
            elif pgnstring[x] not in [']',')','}']:
                newpgn+=pgnstring[x]
                    
    pgnliste=newpgn.split()
    if pgnliste[-1]=='0-1' or pgnliste[-1]=='1/2' or pgnliste[-1]=='1-0' or pgnliste[-1]=='1/2-1/2':
        pgnliste=pgnliste[:-1]
    #print pgnliste
    return pgnliste

def LongSAN(pgnliste):
    #board = chess.Bitboard()
    board = chess.Board()
    LongSANliste=[]
    #print pgnliste
    for zug in pgnliste:
        try:
            longzug=str(board.push_san(zug))
            LongSANliste.append(longzug)
        except ValueError as verr:
            print verr
            return LongSANliste 
    return LongSANliste 


def LoadGamesGenerator(pgnpath):
    Game='x'
    WhiteElo=0
    BlackElo=0
    WhiteName='x'
    BlackName='x'
    Result='x'
    Date='x'
    gamestring=''

    with open(pgnpath,'r') as f:
        for line in f:
            #print line
            if len(line)>0:
                fine=line.replace('\n','')
                mine=fine.replace('\r','')

                if line[:7]=="[Event " or line[:7]=="[Event:":
                    #print line
                    #print gamestring
                    gamestring=''

                if line[0]!='[' and len(line)>3:
                    gamestring+=mine+' '
    
                if line[:9]=="[WhiteElo":
                    liste=line.split('"')
                    elonp=np.zeros((1, 1))
                    elonp[0]=float(liste[1])
                    WhiteElo=elonp
                if line[:6]=="[Date ":
                    Date=line[7:11]

                if line[:9]=="[BlackElo":   
                    liste=line.split('"')
                    elonp=np.zeros((1, 1))
                    elonp[0]=float(liste[1])
                    BlackElo=elonp
                    # print BlackElo[gamecount]

                if line[:len("[White ")]=="[White ":
                    liste=line.split('"')
                    WhiteName=liste[1]

                if line[:len("[Black ")]=="[Black ":
                    liste=line.split('"')
                    BlackName=liste[1]


                gine=mine.replace(' ','')

                if gine[-3:]=="1-0" or gine[-3:]=="0-1" or gine[-3:]=="1/2":
                    Game=gamestring
                    gamestring=''
                    Result=gine[-3:]
                    yield Game,WhiteElo,BlackElo,WhiteName,BlackName,Result,Date
                    Game='x'
                    WhiteElo=0
                    BlackElo=0
                    WhiteName='x'
                    BlackName='x'
                    Result='x'
                    Date='x'

                if gamestring[-4:]=='1-0 ':
                    Game=gamestring[:-4]
                    gamestring=''
                    Result='1-0'
                    yield Game,WhiteElo,BlackElo,WhiteName,BlackName,Result,Date
                    Game='x'
                    WhiteElo=0
                    BlackElo=0
                    WhiteName='x'
                    BlackName='x'
                    Result='x'
                    Date='x'

                if gamestring[-4:]=='0-1 ':
                    Game=gamestring[:-4]
                    gamestring=''
                    Result='0-1'
                    yield Game,WhiteElo,BlackElo,WhiteName,BlackName,Result,Date
                    Game='x'
                    WhiteElo=0
                    BlackElo=0
                    WhiteName='x'
                    BlackName='x'
                    Result='x'
                    Date='x'

                if gamestring[-8:]=='1/2-1/2 ':
                    Game=gamestring[:-8]
                    gamestring=''
                    Result='1/2'
                    yield Game,WhiteElo,BlackElo,WhiteName,BlackName,Result,Date
                    Game='x'
                    WhiteElo=0
                    BlackElo=0
                    WhiteName='x'
                    BlackName='x'
                    Result='x'
                    Date='x'

# Dann Game2Vektoren-Funktionen schreiben
Anfangsstellung=[]
def Anfangstellungdefinator():
    global Anfangsstellung
    for x in range(8):
        Anfangsstellung.append([])
        for y in range(8):
            Anfangsstellung[-1].append('0')

    for x in range(8):
        Anfangsstellung[x][1]='P'  
        Anfangsstellung[x][6]='p'      

    Anfangsstellung[0][0]='R'
    Anfangsstellung[1][0]='N'
    Anfangsstellung[2][0]='B'
    Anfangsstellung[3][0]='Q'
    Anfangsstellung[4][0]='K'
    Anfangsstellung[5][0]='B'
    Anfangsstellung[6][0]='N'
    Anfangsstellung[7][0]='R'

    Anfangsstellung[0][7]='r'
    Anfangsstellung[1][7]='n'
    Anfangsstellung[2][7]='b'
    Anfangsstellung[3][7]='q'
    Anfangsstellung[4][7]='k'
    Anfangsstellung[5][7]='b'
    Anfangsstellung[6][7]='n'
    Anfangsstellung[7][7]='r'
Anfangstellungdefinator()

def Stellungsprint(Stellung):
    for x in range(8):
        for y in range(8):
            print Stellung[y][7-x],
        print    
    print 

# Das hier spuckt Stellung,Zug-Paare aus:
def Stellungsgenerator(gamestring):
    #print "Stellungsgenerator!"
    #print gamestring
    linedict={'a':0,'b':1,'c':2,'d':3,'e':4,'f':5,'g':6,'h':7}
    Stellung=copy.deepcopy(Anfangsstellung)
    pgnliste=PGNparser(gamestring)
    pgnliste=pgnliste[:len(pgnliste)-1]

    RochadeRechte=[1,1,1,1] #w kurz, w lang, s kurz, s lang
    EnPassant=[0,0,0,0,0,0,0,0]

    whosmove=1
    for move in LongSAN(pgnliste):

        yield (Stellung,EnPassant,RochadeRechte, move[:4],whosmove)
        whosmove=(whosmove+1)%2
        
        EnPassant=[0,0,0,0,0,0,0,0]
        if (move[1]=='2' and move[3]=='4') and Stellung[linedict[move[0]]][int(move[1])-1]=='P':
            EnPassant[linedict[move[2]]]=1
        if (move[1]=='7' and move[3]=='5') and Stellung[linedict[move[0]]][int(move[1])-1]=='p':   
            EnPassant[linedict[move[2]]]=1 

        # Hier wird der nächste Zug ausgeführt: Dummerweise Rochade und vor allem EnPassant ...
        if move=='e1g1' and RochadeRechte[0]: # ohne Rochaderecht könnten das auch andere Figuren sein.
            Stellung[5][0]=Stellung[7][0]
            Stellung[7][0]='0'       
            RochadeRechte[0]=0
            RochadeRechte[1]=0
        if move=='e8g8' and RochadeRechte[2]:    
            Stellung[5][7]=Stellung[7][7]
            Stellung[7][7]='0'
            RochadeRechte[2]=0
            RochadeRechte[3]=0            
        if move=='e1c1' and RochadeRechte[1]:
            Stellung[3][0]=Stellung[0][0]
            Stellung[0][0]='0'
            RochadeRechte[0]=0
            RochadeRechte[1]=0            
        if move=='e8c8' and RochadeRechte[3]:
            Stellung[3][7]=Stellung[0][7]
            Stellung[0][7]='0'   
            RochadeRechte[2]=0
            RochadeRechte[3]=0  


        # Hier die Turmzüge, die Rochaderechte zerstören:
        if move[:2]=='h1':
            RochadeRechte[0]=0         
        if move[:2]=='a1':
            RochadeRechte[1]=0 
        if move[:2]=='h8':
            RochadeRechte[2]=0         
        if move[:2]=='a8':
            RochadeRechte[3]=0  

        # EnPassant: e4d3       
        if move[1]=='4' and move[3]=='3' and Stellung[linedict[move[0]]][int(move[1])-1]=='p':  # black pawn moves from row 4 to 3
            if Stellung[linedict[move[2]]][int(move[1])-1]=='P' and Stellung[linedict[move[2]]][int(move[3])-1]=='0':  # above endsquare white pawn and at endsquare no pawn.
                #print "EnPassant!"
                Stellung[linedict[move[2]]][int(move[1])-1]='0'

        if move[1]=='5' and move[3]=='6' and Stellung[linedict[move[0]]][int(move[1])-1]=='P': 
            if Stellung[linedict[move[2]]][int(move[1])-1]=='p' and Stellung[linedict[move[2]]][int(move[3])-1]=='0':
                #print "EnPassant!"
                Stellung[linedict[move[2]]][int(move[1])-1]='0'

        # Hier wird der Move ausgeführt:
        Stellung[linedict[move[2]]][int(move[3])-1]=Stellung[linedict[move[0]]][int(move[1])-1]
        Stellung[linedict[move[0]]][int(move[1])-1]='0'

        # Hier die Umwandlungen:
        if len(move)==5:
            #print move
            if move[4]=="q":    # queen
                if int(move[3])==1:    # Black
                    Stellung[linedict[move[2]]][int(move[3])-1]='q'
                else:    # White
                    Stellung[linedict[move[2]]][int(move[3])-1]='Q'    
            if move[4]=="r":    # rook
                if int(move[3])==1:    # Black
                    Stellung[linedict[move[2]]][int(move[3])-1]='r'
                else:    # White
                    Stellung[linedict[move[2]]][int(move[3])-1]='R'    
            if move[4]=="n":    # knight
                if int(move[3])==1:    # Black
                    Stellung[linedict[move[2]]][int(move[3])-1]='n'
                else:    # White
                    Stellung[linedict[move[2]]][int(move[3])-1]='N'    
            if move[4]=="b":    # bishop
                if int(move[3])==1:    # Black
                    Stellung[linedict[move[2]]][int(move[3])-1]='b'
                else:    # White
                    Stellung[linedict[move[2]]][int(move[3])-1]='B'  
            # for x in range(8):
            #     for y in range(8):
            #         print Stellung[y][7-x],
            #     print    
                                          

def Spiegelung(StellungIn,EnPassant,RochadeRechte, move):
    Whitening={'p':'P','k':'K','q':'Q','r':'R','n':'N','b':'B', 'P':'p','R':'r','N':'n','B':'b','Q':'q','K':'k','0':'0'}
    EnPassant=EnPassant[::-1]
    Stellung=copy.deepcopy(StellungIn)
    for x in range(8):
        Stellung[x]=Stellung[x][::-1]
    #Stellung=Stellung[::-1]
    for x in range(8):
        for y in range(8):
            Stellung[y][7-x]=Whitening[Stellung[y][7-x]]

    RochadeRechte=[RochadeRechte[2]]+[RochadeRechte[3]]+[RochadeRechte[0]]+[RochadeRechte[1]]

    Mover={'1':'8','2':'7','3':'6','4':'5','5':'4','6':'3','7':'2','8':'1',}
    move=move[0]+Mover[move[1]]+move[2]+Mover[move[3]]

    return (Stellung,EnPassant,RochadeRechte, move)


def Stellung2Vektor(Stellung,EnPassant,RochadeRechte):
    Vektor=np.zeros((780, 1))   # 64 Felder * 6 Figuren * 2 Farben + 4 Rochaderechte + 8 EnPassents    
    index=0
    for F in ['K','Q','R','N','B','P']:
        for x in range(8):
            for y in range(8):
                if F==Stellung[x][y]:
                    Vektor[index]=1.0
                index+=1
    for F in ['k','q','r','n','b','p']:
        for x in range(8):
            for y in range(8):
                if F==Stellung[x][y]:
                    Vektor[index]=1.0
                index+=1
    for x in range(8):
        if EnPassant[x]:
            Vektor[index]=1.0
        index+=1    
    for x in range(4):
        if RochadeRechte[x]:
            Vektor[index]=1.0
        index+=1     
    return Vektor

def Vektor2Stellung(Vektor):
    Stellung=[]
    for x in range(8):
        Stellung.append([])
        for y in range(8):
            Stellung[-1].append('0')
    EnPassant=[0,0,0,0,0,0,0,0] 
    RochadeRechte=[0,0,0,0]       

    index=0
    for F in ['K','Q','R','N','B','P']:
        for x in range(8):
            for y in range(8):
                if Vektor[index]==1.0:
                    Stellung[x][y]=F
                index+=1
    for F in ['k','q','r','n','b','p']:
        for x in range(8):
            for y in range(8):
                if Vektor[index]==1.0:
                    Stellung[x][y]=F
                index+=1
    for x in range(8):
        if Vektor[index]==1.0:
            EnPassant[x]=1
        index+=1    
    for x in range(4):
        if Vektor[index]==1.0:
            RochadeRechte[x]=1
        index+=1     
    return (Stellung,EnPassant,RochadeRechte)

A20={'a':0,'b':1,'c':2,'d':3,'e':4,'f':5,'g':6,'h':7}
def Move2Inputvektor(move):
    vektor=np.zeros((128, 1))
    vektor[A20[move[0]]*8 + int(move[1])-1]=1.0
    vektor[64+A20[move[2]]*8+int(move[3])-1]=1.0
    return vektor

def Move2Outputvektor(move):
    vektor=np.zeros((64**2, 1))
    vektor[A20[move[0]] + (int(move[1])-1)*8 + A20[move[2]]*8*8 + (int(move[3])-1)*8*8*8]=1.0
    return vektor



# Hier alle Vektoren: Position, MoveInput, MoveOutput, Elo, Elodiff, Result, ...
def Game2Vectors(pgnpath,startgame):
    gamecount=0
    for Game,WhiteElo,BlackElo,WhiteName,BlackName,Result,Date in LoadGamesGenerator(pgnpath):
        gamecount+=1
        if gamecount>startgame:
            Gamevektoren=[]
            for (Stellung,EnPassant,RochadeRechte, move,whosmove) in Stellungsgenerator(Game):
                if whosmove==0: # if black to move the position is mirrored
                    (Stellung,EnPassant,RochadeRechte, move)=Spiegelung(Stellung,EnPassant,RochadeRechte, move)
                #Position:
                Positionvektor=Stellung2Vektor(Stellung,EnPassant,RochadeRechte)
                #Result:
                Resultvektor=np.zeros((3,1))
                if whosmove==1:
                    if Result=="1-0":
                        Resultvektor[0]=1.0
                    if Result=="0-1":
                        Resultvektor[1]=1.0
                    if Result=="1/2":
                        Resultvektor[2]=1.0
                if whosmove==0:
                    if Result=="0-1":
                        Resultvektor[0]=1.0
                    if Result=="1-0":
                        Resultvektor[1]=1.0
                    if Result=="1/2":
                        Resultvektor[2]=1.0
                #Moveinput:
                Moveinput=Move2Inputvektor(move)
                #Moveoutput:
                Moveoutput=Move2Outputvektor(move)
                #Elo:
                Elovector=np.array([BlackElo,WhiteElo][whosmove])
                #Elodiff:
                Elodiffvector=np.array([BlackElo,WhiteElo][whosmove]-[WhiteElo,BlackElo][whosmove])

                Gamevektoren.append((Positionvektor,Moveinput,Moveoutput,Elovector,Elodiffvector,Resultvektor))
            yield Gamevektoren