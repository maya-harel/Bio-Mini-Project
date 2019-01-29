import logging
import FPtree
import sys


def removeVal(val, list):
    return [a for a in list if not (a == val)]


# this function creates a list out of input data - a tuple for each line (genome number, list of cogs)
def parseInput(file, window):
    dictdata = []
    with open(file) as inputFile:
        for line in inputFile:
            cogsTemp = line.split('#')[-1]
            genomeNum = cogsTemp.split('\t')[0]
            cogList = cogsTemp.split('\t')[1:]
            if len(cogList) <= window:
                tempCogs = removeVal('X', cogList)
                tempCogs = removeVal('\n', tempCogs)
                dictdata.append((genomeNum, tempCogs))
            else :
                for i in range(0, len(cogList)-window+1):
                    tempCogs = removeVal('X', cogList[i:i+window])
                    tempCogs = removeVal('\n', tempCogs)
                    dictdata.append((genomeNum, tempCogs))

    # with open('testDataParsing.txt', 'w+') as testFile :
    #     testFile.write(str(dictdata))

    return dictdata


def createInitSet(dataSet):
    retDict = {}
    for item in dataSet:
        trans = item[1]
        retDict[frozenset(trans)] = 1
    return retDict


def main():

    logging.basicConfig(filename='BioMiniProject.log', level=logging.INFO, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S')
    logging.info('##################### Starting our program #####################')

    constraint = ['1744', '3845', '4603', '1079']
    minSup = 105
    window = 7

    filePath = sys.argv[1]
    genomeDat = parseInput(filePath, window)
    dat = createInitSet(genomeDat)

    myHeaderTab = {}
    for cog in constraint:
        # logging.info('# current COG : ' + str(cog))
        myFPtree, myHeaderTab = FPtree.createTree(genomeDat, dat, minSup)
        # find sub tree for COG and this is the new data for the next iteration

        with open('testHeaderTable.txt', 'w+') as file:
            file.write(str(myHeaderTab))

        if cog in myHeaderTab.keys():
            logging.info('# getting sub tree for current COG : ' + str(cog) + ' with frequency of ' + str(myHeaderTab[cog][0]))
            dat = FPtree.findPrefixPath(cog, myHeaderTab[cog][1])
        else :
            print 'Huston we have a problem'
            return

    print "RESULTS " #TODO - what are the results !?!?


if __name__ == "__main__":
    main()
