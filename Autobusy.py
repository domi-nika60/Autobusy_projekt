import math
import random 
import time 
import matplotlib.pyplot as plt
from random import randint 
 
 
variationProbability = 90
muatationProbability = 75

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
 
def countStopoverPenalty(threadDict, stopList): 
    # initialize stopover matrix 
    stopoverDict = dict() 
    for stop1 in stopList: 
        stopoverDict[stop1] = dict() 
        for stop2 in stopList: 
            stopoverDict[stop1][stop2] = 'x' 
     
    # write 0 to stopover matrix if there exists direct connection 
    for threadId in threadDict: 
        thread = threadDict[threadId] 
        for stop1 in thread: 
            for stop2 in thread: 
                stopoverDict[stop1][stop2] = 0 
 
    # perform algorithm counting stepovers 
    i = 0 
    while True: 
        find_X = False 
        for stop1 in stopList: 
            for stop2 in stopList: 
                if stopoverDict[stop1][stop2] == 'x': 
                    find_X = True 
                    for stop3 in stopList: 
                        if stopoverDict[stop1][stop3] != 'x' and stopoverDict[stop2][stop3] != 'x' and stopoverDict[stop1][stop3] + stopoverDict[stop2][stop3] <= i: 
                            stopoverDict[stop1][stop2] = i + 1 
                            break 
        i += 1 
        if i > 100 or not find_X: 
            break 
     
    # calculate matrix value 
    stopoverPenalty = 0 
    for stop1 in stopList: 
        for stop2 in stopList: 
            if stopoverDict[stop1][stop2] != 'x': 
                stopoverPenalty += stopoverDict[stop1][stop2] ** 2 
 
    return (stopoverDict, stopoverPenalty) 
 
def countDistancePenalty(distanceDict, threadDict): 
    distancePenalty = 0 
    for thread in threadDict: 
        thread = threadDict[thread] 
        for i in range(len(thread)-1): 
            distancePenalty += distanceDict[thread[i]][thread[i+1]] 
    return distancePenalty 
 
def countStandardDeviationPenalty(distanceDict, threadDict): 
    threadsLenght = [] 
    threadsLenghtSum = 0 
    for thread in threadDict: 
        thread = threadDict[thread] 
        threadLenght = 0 
        for i in range(len(thread)-1): 
            threadLenght += distanceDict[thread[i]][thread[i+1]] 
        threadsLenghtSum += threadLenght 
        threadsLenght.append(threadLenght) 
    mean = threadsLenghtSum / len(threadsLenght) 
    standardDeviationPenalty = 0 
    for threadLenght in threadsLenght: 
        standardDeviationPenalty += (mean - threadLenght) ** 2 
    standardDeviationPenalty = (standardDeviationPenalty / len(threadsLenght)) ** (1/2) 
    return standardDeviationPenalty
 
def createProbabilityDict(markDict, n): 
    """ 
    markDict - contains thread id's as keys and their assesment as value 
    n - it's function parameter that can take values between 1 and 2  
    Returns probabilityDict - thread id's as keys and their probability as value.  
    """
    length = len(markDict.keys()) 
    # create sorted dict - rank as key, id as value 
    sorted_list = sorted(markDict.items(), key=lambda x: x[1]) 
    sorted_dict = {} 

    for counter, value in enumerate(sorted_list): 
        sorted_dict[counter + 1] = value[0] 

    if n > 2 or n < 1: 
        return -1 
 
    n_min = 2 - n 
    ranked_dict = {} 
    sum = 0 
    for key in sorted_dict: 
        ranked_dict[sorted_dict[key]] = 1/length*(n-(n_min - n)*(key - 1)/(length - 1)) 
        sum += ranked_dict[sorted_dict[key]] 
 
    for key in ranked_dict: 
        ranked_dict[key] = ranked_dict[key]/sum 
 
    print(ranked_dict) 
    return ranked_dict 
 
 
def variation(dictsList): 
    newChildPopulation = [] 
    while len(dictsList) > 1: 
        mother = random.choice(dictsList) 
        dictsList.remove(mother) 
        father = random.choice(dictsList) 
        dictsList.remove(father) 
 
        variationType = random.randint(0,100) 
 
        if(variationType < variationProbability): 
 
            child_1 ={} 
            child_2 = {} 
            for keyF, valF in zip(list(father.keys()), list(father.values())): 
                for keyM, valM in zip(list(mother.keys()), list(mother.values())): 
                    if(valF[0] == valM[0] and valF[-1] == valM[-1]): 
                        child_1[keyF] = valF 
                        child_2[keyM] = valM 
                        del father[keyF] 
                        del mother[keyM] 
            mergedDict = mother.copy() 
            mergedDict.update(father) 
 
            while len(mergedDict) > 0: 
                thread = random.choice(list(mergedDict.keys())) 
                child = random.choice([child_1,child_2]) 
                child[thread] = mergedDict[thread] 
                del mergedDict[thread] 
         
        else: 
 
            child_1 = {} 
            child_2 = {} 
            for keyF, valF in zip(list(father.keys()), list(father.values())): 
                for keyM, valM in zip(list(mother.keys()), list(mother.values())): 
                    if(valF[0] == valM[0] and valF[-1] == valM[-1]): 
                        randF = random.randint(1,len(valF)-1) 
                        randM = random.randint(1,len(valM)-1) 
                        child_1[keyF] = list(valF[:randF] + valM[randM:]) 
                        child_2[keyM] = list(valM[:randM] + valF[randF:]) 
                        del father[keyF] 
                        del mother[keyM] 
            mergedDict = mother.copy() 
            mergedDict.update(father) 
             
            if((len(mergedDict) % 2) == 1): 
                thread = random.choice(list(mergedDict.keys())) 
                child = random.choice([child_1,child_2]) 
                child[thread] = mergedDict[thread] 
                del mergedDict[thread] 
             
            while len(mergedDict) > 1: 
                temp = mergedDict.copy() 
                thread_1 = random.choice(list(temp.keys())) 
                del temp[thread_1] 
                thread_2 = random.choice(list(temp.keys())) 
                cut_1 = random.randint(1,len(mergedDict[thread_1])-1) 
                cut_2 = random.randint(1,len(mergedDict[thread_2])-1) 
                child_1[thread_1] = list(mergedDict[thread_1][:cut_1] + mergedDict[thread_2][cut_2:]) 
                child_2[thread_2] = list(mergedDict[thread_2][:cut_2] + mergedDict[thread_1][cut_1:]) 
                del mergedDict[thread_1] 
                del mergedDict[thread_2] 
        newChildPopulation.append(child_1) 
        newChildPopulation.append(child_2) 
    return newChildPopulation 
 
def mutation(dictsList, stationsListIds): 
    mutated = random.choice(dictsList) 
    print(dictsList) 
    muattedThread = random.choice(list(mutated.keys())) 
    mutationType = random.randint(0,100) 
    if(mutationType < muatationProbability): 
        if(mutationType > muatationProbability/3): 
            for x in range (random.randint(1,5)): 
                mutated[muattedThread].insert(random.randint(1,len(mutated[muattedThread])-1),random.choice(stationsListIds)) 
        else: 
            exchangeList = [] 
            for x in range (random.randint(1,5)): 
                exchangeList.append(random.choice(stationsListIds))             
            mutated[muattedThread][random.randint(1,len(mutated[muattedThread])-1):random.randint(1,len(mutated[muattedThread])-1)] = exchangeList 
    else: 
        del mutated[muattedThread] 
        # tu se wygenerujemy nową niteczkę YOLO 
        # mutated[muattedThread] = nowa nitka 
    print(dictsList) 
    return dictsList 
 
def problemPlot(points, loopsListIds): 
    for key, coordinate in zip(list(points.keys()), list(points.values())): 
        if (key in loopsListIds): 
            plt.scatter(coordinate[0],coordinate[1], s=50, c = 'red', zorder = 2) 
        else: 
            plt.scatter(coordinate[0],coordinate[1], s=20, c = 'blue', zorder = 2) 
    plt.show() 
 
def solutionPLot(solutionDict,points,loopsListIds): 
    for line in (list(solutionDict.values())): 
        color = "#{:06x}".format(random.randint(0, 0xFFFFFF)) 
        for station in range (len(line)-1): 
            plt.plot([list(points[line[station]])[0],list(points[line[station + 1]])[0]],[list(points[line[station]])[1],list(points[line[station + 1]])[1]], color, zorder = 1) 
    problemPlot(points,loopsListIds) 
             
 
if __name__ == "__main__": 
 
    ## Przykładowe zastosowanie powyższych funkcji: 
    dc = GenerateBusStops(50, 1000, 1500, 5)
    print(dc) 
    print("")
    dd = GenerateDistanceDict(dc)
    print(dd) 
    print("")
    li = ChooseTerminals(dd, 0.9) 
    print(li)
    print("")
    dl = GenerateLines(li) 
    print(dl)
    print("")
    dt = GenerateThreads(dl, dc) 
    print(dt)
    print("")
    # m = AmountOfMissedBusStops(dt, dc, dl) 
    # print(m)
    # csp = countStopoverPenalty(dt,dc.keys()) 
    # print(csp)
    # cdp = countDistancePenalty(dd, dt) 
    # print(cdp)
    # csdp = countStandardDeviationPenalty(dd, dt) 
    # print(csdp) 

    problemPlot(dc,li)
    solutionPLot(dt,dc,li)