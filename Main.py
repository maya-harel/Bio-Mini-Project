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
    with open(file) as inputFile:
        for line in inputFile:
            lineTemp = line.split('#')[-1]
            genomeNum = lineTemp.split('\t')[0]
            cogList = lineTemp.split('\t')[1:]
            cogList = removeVal('\n', cogList)
            if len(cogList) <= window:
                cogList = removeVal('X', cogList)
                inputData[tuple(cogList)].add(genomeNum)
            else :
                for i in range(0, len(cogList) - window):
                    cogList = removeVal('X', cogList[i:i+window-1])
                    inputData[tuple(cogList)].add(genomeNum)

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
    for trans in inputData.keys(): # trans is a tuple of a window
        for cog in trans:
            # cogsDict[cog].add(inputData[trans])
            for genome in inputData[trans]:
                genomeSet = cogsDict[cog]
                genomeSet.add(genome)
                cogsDict[cog].update(genomeSet)

    for cog in cogsDict.keys():
        if len(cogsDict[cog]) < minSup:

            cogsDict.pop(cog)

    for trans in inputData.keys():
        newTrans = set()
        for cog in trans:
            if cog in cogsDict.keys():
                newTrans.add(cog)
        newTrans = sorted(newTrans, reverse=True, key=lambda cog: len(cogsDict[cog]))
        newInputData[tuple(newTrans)] = inputData[trans]
        data.append(list(newTrans))

    dataSet = createInitSet(data)

    return dataSet, cogsDict, newInputData # list of lists, cog dictionary, new inputData

def createInitSet(dataSet):
    retDict = {}
    for trans in dataSet:
        retDict[frozenset(trans)] = 1
    return retDict


def updateData(dataSet, inputData, currentCog, minSup):
    # recive pruned data set. update input data according to it. create and return new COGSdict
    newInputData = defaultdict(set)

    # update DATA
    for trans in inputData.keys():
        if currentCog in trans:
            newTrans = frozenset(cog for cog in trans if cog != currentCog)
            # if newTrans in dataSet.keys():
            newInputData[newTrans] = inputData[trans]

    dataSet, cogsDict, newData = countAndPrune(newInputData, minSup)

    return cogsDict, newInputData


def sortConst(constraint, cogsDict):
    return sorted(constraint, reverse=True, key=lambda cog: len(cogsDict[cog]))


def main():

    testingThings.main()

    return

    logging.basicConfig(filename='BioMiniProject.log', level=logging.INFO, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S') #TODO
    logging.info('##################### Starting our program #####################')

    constraint = ['1744', '3845', '4603', '1079']
    minSup = 1
    window = 7

    filePath = sys.argv[1]
    inputData = parseInput(filePath, window) # window + list of genome

    dataSet, cogsDict, inputData = countAndPrune(inputData, minSup)

    # myFPtree, myHeaderTab = FPtree.createTree(dataSet, cogsDict)
    constraint = sortConst(constraint, cogsDict)

    for currentCog in constraint:
        print 'iter ' + str(currentCog) + ' cogs are ' + str(cogsDict)
        myFPtree, myHeaderTab = FPtree.createTree(dataSet, cogsDict)
        print '# looking for sub tree for current COG : ' + str(currentCog)
        try :
            # print '# found it ! with frequency of ' + str(myHeaderTab[currentCog][0])
            dataSet = FPtree.findPrefixPath(currentCog, myHeaderTab[currentCog][1])
            cogsDict, inputData = updateData(dataSet, inputData, currentCog, minSup)
            print "NEW SUB DATA " + str(dataSet)
        except Exception :
            dataSet = {}
            print "Oh no, the cog is not here !"
            sys.exit(1)

        # myFPtree, myHeaderTab = FPtree.createTree(dataSet, cogsDict)

    # for cog in constraint:
    #     print "current iteration - COG : " + str(cog)
    #     myFPtree, myHeaderTab = FPtree.createTree(cogsDict, dataSet, minSup, cog)
    #     # find sub tree for COG and this is the new data for the next iteration
    #
    #     # with open('testHeaderTable.txt', 'w+') as file:
    #     #     file.write(str(myHeaderTab))
    #
    #     # if cog in myHeaderTab.keys():
    #     logging.info('# getting sub tree for current COG : ' + str(cog) + ' with frequency of ' + str(myHeaderTab[cog][0]))
    #     print '# getting sub tree for current COG : ' + str(cog) + ' with frequency of ' + str(myHeaderTab[cog][0])
    #     dataSet = FPtree.findPrefixPath(cog, myHeaderTab[cog][1])
    #     # else :
    #     #     print 'Huston we have a problem'
    #     #     return

    print "RESULTS " + str(dataSet)


if __name__ == "__main__":
    main()
