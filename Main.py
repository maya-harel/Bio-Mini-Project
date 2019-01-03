import Constraints
import logging
import FPtree


# this function creates a list out of input data - a tuple for each line (genome number, list of cogs)
def parseInput(file):
    dictdata = []
    with open(file) as inputFile:
        for line in inputFile:
            currCogs = []
            cogsTemp = line.split('#')[-1]
            genomeNum = cogsTemp.split('\t')[0]
            for cog in cogsTemp.split('\t')[1:]:
                if cog == 'X' or cog == '\n':
                    continue
                currCogs.append(cog)
            dictdata.append((genomeNum, currCogs))
    return dictdata


def createInitSet(dataSet):
    retDict = {}
    for trans in dataSet:
        retDict[frozenset(trans)] = 1
    return retDict



def main():

    logging.basicConfig(filename='BioMiniProject.log', level=logging.INFO, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S')
    logging.info('Starting our program ! Yay !')

    simpDat = parseInput('C:/Users/User/PycharmProjects/BioMini/inputFiles/tempFile.txt')
    dat = createInitSet(simpDat) # TODO - do we need this function ? what does it do ?

    query = ['0392', '03923']
    query2 = ['0397', '0398', '0401']
    minSup = 3
    window = 3

    for cog in query:
        myFPtree, myHeaderTab = FPtree.createTree(dat, minSup, window, cog)
        # find sub tree for COG and this is the new data for the next iteration
        dat = FPtree.findPrefixPath(cog, myHeaderTab[cog])


    # myFPtree, myHeaderTab = FPtree.createTree(dat, 1)
    # # myFPtree.disp()
    # for item in myHeaderTab.values():
    #     condPats = FPtree.findPrefixPath(item, myHeaderTab[1])
    #     myFPtree, myHeaderTab = FPtree.createTree(condPats, 1)



if __name__ == "__main__":
    main()
