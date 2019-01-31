import logging
import FPtree
import sys
from collections import defaultdict


def removeVal(val, list):
    return [a for a in list if not (a == val)]


# this function creates a list out of input data - a tuple for each line (genome number, list of cogs)
def parseInput(file, window):
    data = [] # windows of cogs
    counter = 0
    cogsDict = defaultdict(set) # key = cog window, value = genome list
    with open(file) as inputFile:
        for line in inputFile:
            cogsTemp = line.split('#')[-1]
            genomeNum = cogsTemp.split('\t')[0]
            cogList = cogsTemp.split('\t')[1:]
            cogList = removeVal('\n', cogList)
            if len(cogList) <= window:
                tempCogs = removeVal('X', cogList)
                # sortedCogs = sorted(tempCogs)
                data.append(sorted(tempCogs)) # add to data
                cogString = "-".join(sorted(tempCogs))
                cogsDict[cogString].add(genomeNum) # add to cog dictionary
            else :
                for i in range(0, len(cogList)-window):
                    tempCogs = removeVal('X', cogList[i:i+window-1])
                    # sortedCogs = sorted(tempCogs)
                    data.append(sorted(tempCogs))  # add to data
                    cogString = "-".join(sorted(tempCogs))
                    cogsDict[cogString].add(genomeNum)  # add to cog dictionary


    # with open('testDataParsing.txt', 'w+') as file:
    #     file.write(str(data))
    #
    # with open('testCOGdict.txt', 'w+') as file:
    #     file.write(str(cogsDict))

    return data, cogsDict


def createInitSet(dataSet):
    retDict = {}
    for trans in dataSet:
        retDict[tuple(trans)] = 1
    return retDict


def main():

    logging.basicConfig(filename='BioMiniProject.log', level=logging.INFO, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S') #TODO
    logging.info('##################### Starting our program #####################')

    constraint = sorted(['1744', '3845', '4603', '1079'])
    minSup = 35
    window = 7

    filePath = sys.argv[1]
    data, cogsDict = parseInput(filePath, window)
    dataSet = createInitSet(data)

    prevCogList = []
    myFPtree, myHeaderTab = FPtree.createTree(cogsDict, dataSet, minSup, None)
    for cog in constraint:
        try :
            print '# getting sub tree for current COG : ' + str(cog) + ' with frequency of ' + str(myHeaderTab[cog][0])
            dataSet = FPtree.findPrefixPath(cog, myHeaderTab[cog][1])
            print "NEW SUB DATA " + str(dataSet)
            prevCogList.append(cog)
        except Exception :
            dataSet = []
            "Oh no, the cog is not here !"

        myFPtree, myHeaderTab = FPtree.createTree(cogsDict, dataSet, minSup, prevCogList)

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
