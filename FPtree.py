import logging
from collections import defaultdict

# global cogsDict
# global inputData
# global dataSet

class treeNode:
    def __init__(self, nameValue, numOccur, parentNode):
        self.name = nameValue
        self.count = numOccur
        self.nodeLink = None
        self.parent = parentNode  # needs to be updated
        self.children = {}

    # increments the count variable with a given amount
    def inc(self, numOccur):
        self.count += numOccur

    # display tree in text. Useful for debugging
    def disp(self, ind=1):
        print ('  '*ind, self.name, ' ', self.count)
        for child in self.children.values():
            child.disp(ind+1)


# for each cog, count how many different genomes it appears in
def countOccurence(cogsDict, dataSet, minSup, prevCogList):
    headerTable = {} # key = cog, value = num of different genomes
    counterTable = defaultdict(set) # key = cog, value = list of genomes

    for item in cogsDict.keys():
        listOfCogs = item.split('-')
        genomeList = cogsDict[item]
        for cog in listOfCogs :
            for genome in genomeList:
                counterTable[cog].add(genome)

    for cog in counterTable.keys():
        if len(counterTable[cog]) >= minSup:
            headerTable[cog] = len(counterTable[cog])

    # for item, count in dataSet.items(): # item is a list of COGs
    #     if prevCogList != None :
    #         item = item + tuple(prevCogList)
    #         cogString = "-".join(sorted(item))
    #     else :
    #         cogString = "-".join(item)
    #
    #     if cogString not in cogsDict.keys() and prevCogList != None:
    #         # print "SHIT the string is not here " + cogString
    #         continue
    #     genomeList = cogsDict[cogString]
    #     for cog in item:
    #         for genome in genomeList:
    #             counterTable[cog].add(genome)
    #
    # for cog in counterTable.keys():
    #     if len(counterTable[cog]) >= minSup:
    #         headerTable[cog] = len(counterTable[cog])
    #     else :
    #         counterTable.pop(cog)

    # print "CURRENT HEADER TABLE " + str(headerTable)

    return headerTable


# create FP-tree from dataset
def createTree(dataSet, cogsDict):
    headerTable = {}
    # go over dataSet twice
    for cog in cogsDict.keys():
        headerTable[cog] = len(cogsDict[cog])

    freqItemSet = set(headerTable.keys())
    logging.info("freqItemSet : " + str(freqItemSet))
    print 'freqItemSet: ', freqItemSet
    if len(freqItemSet) == 0:
        logging.info("none of the items are frequent enough.")
        return None, None  # if no items meet min support -->get out
    for k in headerTable:
        headerTable[k] = [headerTable[k], None]  # reformat headerTable to use Node link
    retTree = treeNode('Null Set', 1, None)  # create tree
    for tranSet, count in dataSet.items():  # go through dataset 2nd time
        localD = {}
        for item in tranSet:  # put transaction items in order
            if item in freqItemSet:
                localD[item] = headerTable[item][0] # counter !
        if len(localD) > 0:
            orderedItems = [v[0] for v in sorted(localD.items(), key=lambda p: p[1], reverse=True)]
            updateTree(orderedItems, retTree, headerTable, count)  # populate tree with ordered freq itemset
    logging.info("headerTable : " + str(headerTable))
    print 'headerTable: ', headerTable
    return retTree, headerTable  # return tree and header table


def updateHeader(nodeToTest, targetNode):  # this version does not use recursion
    while (nodeToTest.nodeLink != None):  # Do not use recursion to traverse a linked list!
        nodeToTest = nodeToTest.nodeLink
    nodeToTest.nodeLink = targetNode


def updateTree(items, inTree, headerTable, count):
    if items[0] in inTree.children:  # check if orderedItems[0] in retTree.children
        inTree.children[items[0]].inc(count)  # increment count
    else:  # add items[0] to inTree.children
        inTree.children[items[0]] = treeNode(items[0], count, inTree)
        if headerTable[items[0]][1] == None:  # update header table
            headerTable[items[0]][1] = inTree.children[items[0]]
        else:
            updateHeader(headerTable[items[0]][1], inTree.children[items[0]])
    if len(items) > 1:  # call updateTree() with remaining ordered items
        updateTree(items[1::], inTree.children[items[0]], headerTable, count)


def ascendTree(leafNode, prefixPath):  # ascends from leaf node to root
    if leafNode.parent != None:
        prefixPath.append(leafNode.name)
        ascendTree(leafNode.parent, prefixPath)


def findPrefixPath(basePat, treeNode):  # treeNode comes from header table
    condPats = {}
    while treeNode != None:
        prefixPath = []
        ascendTree(treeNode, prefixPath)  # get the string for each leaf in linkedList for specific letter/item and add to list
        if len(prefixPath) > 1:
            condPats[frozenset(sorted(prefixPath[1:]))] = treeNode.count
        treeNode = treeNode.nodeLink
    return condPats