import random
import time
import matplotlib.pyplot as plt

variationProbability = 90
muatationProbability = 75

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

    dict1 = {
        1: [3,5,2,4],
        2: [5,6,4,3,2,1],
        5: [8,9,6,65]
    }

    dict2 = {
        3: [3,4],
        4: [6,65,15]
    }

    dict3 = {
        30: [3,4],
        41: [5,9,1],
        21: [5,6,4,3,2,1],
        52: [8,9,6,65],
        6: [1,2,3,4,5]
    }

    dict4 = {
        51: [1,2],
        90: [9,8]
    }
    for b in range (10):
        test = {}
        for i in range (100):
            test[i] = [random.randint(2,50),random.randint(2,50)]



        # problemPlot(test,[2,4,23,25,34,38,41,44,48,55,56,64,68,71,74,79,85,95,99])
    solutionPLot(dict3,test,[2,4,23,25,34,38,41,44,48,55,56,64,68,71,74,79,85,95,99])
    bum = [dict1,dict2,dict3,dict4]
    # print (bum)
    # print (variation(bum))
    # print (bum)
    mutation(bum,[-1,-2,-3])
