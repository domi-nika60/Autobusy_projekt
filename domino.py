


threadDict = {'1': ['a', 'd', 'g'],
              '2': ['c', 'b'],
              '3': ['b', 'd', 'e', 'f']}
stopList = ['a', 'b', 'c', 'd', 'e', 'f', 'g']

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
                        if stopoverDict[stop1][stop3] != 'x' and \
                           stopoverDict[stop2][stop3] != 'x' and \
                           stopoverDict[stop1][stop3] + stopoverDict[stop2][stop3] <= i:
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

def countMissedStops(threadDict, stopList):
    locatedStops = 0
    for stop in stopList:
        for thread in threadDict:
            if stop in thread:
                locatedStops += 1
                break
    missedStops = len(stopList) - locatedStops
    return missedStops


def createProbabilityDict(markDict, n):
    """
    markDict - contains thread id's as keys and their assesment as value
    n - it's function parameter that can take values between 1 and 2 
    Returns probabilityDict - thread id's as keys and their probability as value. 
    """
    length = len(markDict.keys())

    # create sorted dict - rank as key, id as value
    sorted_list = sorted(my_dict.items(), key=lambda x: x[1])
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
    

    
my_dict = {
    'a': 12,
    'b': 23,
    'c': 2,
    'd': 13
}

createProbabilityDict(my_dict, 1.5)
