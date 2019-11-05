#!/usr/bin/env python
# -*- coding: utf-8 -*-

from random import randint
import math


def GenerateBusStops(amount, max_x, max_y, dist):
    DictCoordinate = {}
    new = 1;
    i_x = randint (0, max_x)
    i_y = randint (0, max_y)
    DictCoordinate[1]=[i_x, i_y]
    while len(DictCoordinate)<amount :
        i_x = randint (0, max_x)
        i_y = randint (0, max_y)
        while not CheckDistance(DictCoordinate, i_x, i_y, dist):
            i_x = randint (0, max_x)
            i_y = randint (0, max_y)
        new = new +1     
        DictCoordinate[new]=[i_x, i_y]
    return DictCoordinate

def CheckDistance (DictCoordinate, x, y, dist):
    for i in range (1, len(DictCoordinate.keys())+1): 
        if math.fabs(DictCoordinate[i][0] - x) <dist or math.fabs(DictCoordinate[i][1] - y) <dist:
            return False
    return True

def PointsDistance (A, B):
    p_dist = math.sqrt(pow(B[0]-A[0], 2)+pow(B[1]-A[1], 2))
    return p_dist

def GenerateDistanceDict(DictCoordinate):
    DictDistance = {}
    for i in range (1, len(DictCoordinate.keys())+1):
        dict_of_others = {}
        for other in range (1, len(DictCoordinate.keys())+1):
            dist_i_to_oth = PointsDistance (DictCoordinate[i], DictCoordinate[other])
            dict_of_others[other] = dist_i_to_oth
        DictDistance[i] = dict_of_others
    return DictDistance

def ChooseTerminals(DictDistance, rate): 
    LoopsId = []
    pair = randint (1, int(len(DictDistance.keys())*rate))
    maxx = int()
    while len(LoopsId) < pair:
        maxx = 0
        for i in range (1, len(DictDistance.keys())+1):
            for j in range (1, len(DictDistance[i].keys())+1):
                if DictDistance[i][j] > maxx and i not in LoopsId and j not in LoopsId:
                    maxx = DictDistance[i][j]
                    i_temp = i
                    j_temp = j
        if i_temp not in LoopsId:
            LoopsId.append(i_temp)
        if j_temp not in LoopsId:
            LoopsId.append(j_temp)
    return LoopsId

def GenerateLines(LoopsId):         
     DictLines = {}
     PossibPairs = [] #lista możliwych połączen miedzy pętlami
     for i in range (len(LoopsId)):     #generuje liste ze wszystkimi możliwymi połączeniami
         for j in range (i+1, len(LoopsId)):
             pair = [LoopsId[i], LoopsId[j]]
             PossibPairs.append(pair)
     #losuje ile ma być nitek:
     n = len(LoopsId)
     numOfThreads = randint(1, n*(n-1)/2 )
     for i in range (1, numOfThreads+1):    #losuje z możliwych par tyle ile liczba nitek, przyporządkowuje im od razu id w dict-cie:
         line = randint(0, len(PossibPairs)-1) 
         DictLines[i]=PossibPairs[line]
         PossibPairs.remove(PossibPairs[line])
     return DictLines


def GenerateThreads (DictLines, DictCoordinate): 
    DictThreads ={}
    for i in range (1, len(DictLines.keys())+1):
        BusStopsAmount_i = randint(1, len(DictCoordinate.keys())-2)
        helpfulList = []
        for p in range (1, len(DictCoordinate.keys())+1): 
            helpfulList.append(p)
        helpfulList.remove(DictLines[i][0]) 
        helpfulList.remove(DictLines[i][1])
        ListBus_i = [DictLines[i][0]]  
        for j in range (0, BusStopsAmount_i):
            BusStop_j = randint(0, len(helpfulList)-1) 
            ListBus_i.append(helpfulList[BusStop_j])
            helpfulList.remove(helpfulList[BusStop_j])
            
        ListBus_i.append(DictLines[i][1]) 
        DictThreads[i] = ListBus_i
    return DictThreads

def AmountOfMissedBusStops (DictThreads, DictCoordinate, DictLines): 
    missed = 0
    for bst in range (1, len(DictCoordinate.keys())+1):  # przechodze po wszystkich przytankach 
        for thr in range (0, len(DictLines.keys())):     # przechodze po wszyskich nitakch
            if bst in DictThreads[thr+1]:
                missed = missed +1
                break
            else:
                continue
    missed = len(DictCoordinate.keys())-missed
    return missed


## Przykładowe zastosowanie powyższych funkcji:
dc = GenerateBusStops(100, 1000, 1500, 3)
dd = GenerateDistanceDict(dc)
li = ChooseTerminals(dd, 0.9)
dl = GenerateLines(li)
dt = GenerateThreads(dl, dc)
m = AmountOfMissedBusStops(dt, dc, dl)
