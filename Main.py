import logging
import FPtree
import sys
import testingThings
from collections import defaultdict


def removeVal(val, list):
    return [a for a in list if not (a == val)]


# this function creates a list out of input data - a tuple for each line (genome number, list of cogs)
def parseInput(file, window):
    inputData = defaultdict(set) # key = tuple(window), value = set of genomes
    cogsDict = defaultdict(set)

    with open(file) as inputFile:
        for line in inputFile:
            lineTemp = line.split('#')[-1]
            genomeNum = lineTemp.split('\t')[0]
            cogList = lineTemp.split('\t')[1:]
            cogList = removeVal('\n', cogList)
            for cog in cogList:
                cogsDict[cog].add(genomeNum)

    with open(file) as inputFile:
        for line in inputFile:
            lineTemp = line.split('#')[-1]
            genomeNum = lineTemp.split('\t')[0]
            cogList = lineTemp.split('\t')[1:]
            cogList = removeVal('\n', cogList)
            cogList = removeVal('', cogList)
            if len(cogList) <= window:
                cogList = removeVal('X', cogList)
                cogList = list(set(cogList))
                cogList = sorted(cogList, reverse=True, key=lambda cog: len(cogsDict[cog]))
                inputData[frozenset(cogList)].add(genomeNum)
            else :
                for i in range(0, len(cogList) - window):
                    cogList = removeVal('X', cogList[i:i+window-1])
                    cogList = list(set(cogList))
                    cogList = sorted(cogList, reverse=True, key=lambda cog: len(cogsDict[cog]))
                    inputData[frozenset(cogList)].add(genomeNum)

    # print "INPUT DATA : "
    # for item in inputData.items():
    #     print str(item)
    return inputData

    # data = [] # windows of cogs
    # cogsDict = defaultdict(set) # key = cog window, value = genome list
    # with open(file) as inputFile:
    #     for line in inputFile:
    #         cogsTemp = line.split('#')[-1]
    #         genomeNum = cogsTemp.split('\t')[0]
    #         cogList = cogsTemp.split('\t')[1:]
    #         cogList = removeVal('\n', cogList)
    #         if len(cogList) <= window:
    #             tempCogs = removeVal('X', cogList)
    #             # sortedCogs = sorted(tempCogs)
    #             data.append(sorted(tempCogs, reverse=True)) # add to data
    #             cogString = "-".join(sorted(tempCogs, reverse=True))
    #             cogsDict[cogString].add(genomeNum) # add to cog dictionary
    #         else :
    #             for i in range(0, len(cogList)-window):
    #                 tempCogs = removeVal('X', cogList[i:i+window-1])
    #                 # sortedCogs = sorted(tempCogs)
    #                 data.append(sorted(tempCogs, reverse=True))  # add to data
    #                 cogString = "-".join(sorted(tempCogs, reverse=True))
    #                 cogsDict[cogString].add(genomeNum)  # add to cog dictionary
    #
    # # remove infrequent windows
    # for item in data :
    #     str = "-".join(item)
    #     if len(cogsDict[str]) < minSup:
    #         data.remove(item)
    #
    # # remove infrequent items
    # freqCogs = FPtree.countOccurence(cogsDict, data, minSup, None)
    # for item in data:
    #     for cog in item:
    #         if freqCogs[cog] < minSup:
    #             data.remove(item)
    #
    # return data, cogsDict

def countAndPrune(inputData, minSup): #dict - key= tuple(window), value = set of genomes
    data = []
    cogsDict = defaultdict(set)
    newInputData = defaultdict(set)
    for trans, list in inputData.items(): # trans is a tuple of a window
        for cog in trans:
            # cogsDict[cog].add(inputData[trans])
            for genome in list:
                genomeSet = cogsDict[cog]
                genomeSet.add(genome)
                cogsDict[cog].update(genomeSet)

    for cog in cogsDict.keys():
        if len(cogsDict[cog]) < minSup:
            del(cogsDict[cog])
            # cogsDict.pop(cog)

    for trans in inputData.keys():
        newTrans = []
        for cog in trans:
            if cog in cogsDict.keys():
                newTrans.append(cog)
        newTrans = sorted(newTrans, reverse=True, key=lambda cog: len(cogsDict[cog]))
        newInputData[frozenset(newTrans)] = inputData[trans]
        data.append(newTrans)

    # dataSet = createInitSet(data)

    return data, cogsDict, newInputData # list of lists, cog dictionary, new inputData

def createInitSet(dataSet):
    retDict = {}
    for trans in dataSet:
        retDict[frozenset(trans)] = 1
    return retDict


def updateData(dataSet, inputData, currentCog, minSup):
    # recive pruned data set. update input data according to it. create and return new COGSdict
    newInputData = defaultdict(set)
    cogsDict = defaultdict(list)

    # for trans in dataSet.keys():
    #     prevWindow = list(trans).append(currentCog)
    #     genomeList = inputData[tuple(prevWindow)]
    #     newInputData[trans] = genomeList
    #     for cog in trans:
    #         for genome in genomeList:
    #             if genome not in cogsDict[cog]:
    #                 cogsDict[cog].append(genome)

    #update DATA
    for trans in inputData.keys():
        if currentCog in trans:
            newTrans = frozenset(cog for cog in trans if cog != currentCog)
            if newTrans in dataSet.keys():
                newInputData[newTrans] = inputData[trans]

    dataSet, cogsDict, newData = countAndPrune(newInputData, minSup)

    return cogsDict, newInputData


def sortConst(constraint, cogsDict):
    return sorted(constraint, reverse=False, key=lambda cog: len(cogsDict[cog]))


def main():

    # testingThings.main()
    # return

    logging.basicConfig(filename='BioMiniProject.log', level=logging.INFO, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S') #TODO
    logging.info('##################### Starting our program #####################')

    constraint = ['1744', '3845', '4603', '1079']
    #constraint = ['b']
    minSup = 100
    window = 7

    filePath = sys.argv[1] #'C:/Users/User/PycharmProjects/BioMini/newFliteredData.txt'
    inputData = parseInput(filePath, window) # window + list of genome

    data, cogsDict, inputData = countAndPrune(inputData, minSup)
    dataSet = createInitSet(data)
    constraint = sortConst(constraint, cogsDict)

    remainingCogs = constraint
    for currentCog in constraint:
        myFPtree, myHeaderTab = FPtree.createTree(dataSet, cogsDict)
        print "HEADER TABLE : " + str(myHeaderTab.keys())
        print '# looking for sub tree for current COG : ' + str(currentCog)
        try :
            # print '# found it ! with frequency of ' + str(myHeaderTab[currentCog][0])
            dataSet = FPtree.findPrefixPath(currentCog, myHeaderTab[currentCog][1])
            cogsDict, inputData = updateData(dataSet, inputData, currentCog, minSup)
            print "NEW SUB DATA " + str(dataSet)
        except Exception :
            # dataSet = {}
            print "Oh no, the cog is not here !"
            sys.exit(1)
        remainingCogs.remove(currentCog)
        # myFPtree, myHeaderTab = FPtree.createTree(dataSet, cogsDict)


    print "RESULTS " + str(dataSet)


if __name__ == "__main__":
    main()
