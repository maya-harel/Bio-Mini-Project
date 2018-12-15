import Constraints
import logging
import FPtree


def createInitSet(dataSet):
    retDict = {}
    for trans in dataSet:
        retDict[frozenset(trans)] = 1
    return retDict


def parseInput(pathOfInputFle):
    logging.info("parsing input")
    const = ""
    threshold = 0
    window = 0
    currConst = Constraints(const, threshold, window)


def main():

    logging.basicConfig(filename='BioMiniProject.log', level=logging.INFO, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S')
    logging.info('Starting our program ! Yay !')

    # for testing
    simpDat = [['r', 'z', 'h', 'j', 'p'],
               ['z', 'y', 'x', 'w', 'v', 'u', 't', 's'],
               ['z'],
               ['r', 'x', 'n', 'o', 's'],
               ['y', 'r', 'x', 'z', 'q', 't', 'p'],
               ['y', 'z', 'x', 'e', 'q', 's', 't', 'm']]

    dat = createInitSet(simpDat)
    myFPtree, myHeaderTab = FPtree.createTree(dat, 1)
    # myFPtree.disp()
    for item in myHeaderTab.keys():
        condPats = FPtree.findPrefixPath(item, myHeaderTab[item][1])
        myFPtree, myHeaderTab = FPtree.createTree(condPats, 1)

    '''
        what is the stop condition ? need to put the code into some sort of loop
        integrate constraints - how to grow constraints between iterations ?
        how to parse end results 
    '''


if __name__ == "__main__":
    main()
