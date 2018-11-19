import Constraints
import FPtree

def createInitSet(dataSet):
    retDict = {}
    for trans in dataSet:
        retDict[frozenset(trans)] = 1
    return retDict

def parseInput(pathOfInputFle):
    print "parsing input !"
    const = ""
    threshold = 0
    window = 0
    currConst = Constraints(const, threshold, window)

def parseData(pathOfData):
    print "parsing data !"

def main():
    print "Hello it is I"

    # example of dataset
    simpDat = [['r', 'z', 'h', 'j', 'p'],
               ['z', 'y', 'x', 'w', 'v', 'u', 't', 's'],
               ['z'],
               ['r', 'x', 'n', 'o', 's'],
               ['y', 'r', 'x', 'z', 'q', 't', 'p'],
               ['y', 'z', 'x', 'e', 'q', 's', 't', 'm']]

    # get input. parse into Constrain OBJ
    # create tree from dataset
    # mine tree according to constraints. create new tree. and thus forth

if __name__ == "__main__":
    main()
