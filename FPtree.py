import logging

# variables:
# name of the node, a count
# nodelink used to link similar items
# parent vaiable used to refer to the parent of the node in the tree
# node contains an empty dictionary for the children in the node


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


# for each cog, count how many different genomes it appears in AND parse according to COG
# TODO - add window ! and use for search for cog
def countOccurence(dictData, minSup, window, cog):
    counterTable = {}
    for item in dictData:
        genome = item[0]
        # if the cog is not in the list - PRUNE
        if not (cog in item):
            continue
        else:
            for cog in dictData[1:]:
                counterTable[cog].append(genome)

    for item in counterTable.key():
        if len(counterTable[item]) < minSup:
            del counterTable[item]

    return counterTable


# create FP-tree from dataset
def createTree(dataSet, minSup, window, currCog):  # currCog is what we are looking for in the current iteration
    logging.info("creating FP tree")
    headerTable = {}
    # go over dataSet twice
    headerTable = countOccurence(dataSet, minSup, window, currCog)
    # for trans in dataSet:  # first pass counts frequency of occurance
    #     for item in trans:
    #         headerTable[item] = headerTable.get(item, 0) + dataSet[trans]
    # for k in list(headerTable):  # remove items not meeting minSup
    #     if headerTable[k] < minSup:
    #         del (headerTable[k])
    freqItemSet = set(headerTable.keys())
    logging.info("freqItemSet : " + str(freqItemSet))
    print 'freqItemSet: ', freqItemSet
    if len(freqItemSet) == 0:
        logging.info("none of the items are frequent enough.")
        return None, None  # if no items meet min support -->get out
    for k in headerTable:
        headerTable[k] = [headerTable[k], None]  # reformat headerTable to use Node link
    logging.info("headerTable : " + str(headerTable))
    print 'headerTable: ', headerTable
    retTree = treeNode('Null Set', 1, None)  # create tree
    for tranSet, count in dataSet.items():  # go through dataset 2nd time
        localD = {}
        for item in tranSet:  # put transaction items in order
            if item in freqItemSet:
                localD[item] = headerTable[item][0] # counter !
        if len(localD) > 0:
            orderedItems = [v[0] for v in sorted(localD.items(), key=lambda p: p[1], reverse=True)]
            updateTree(orderedItems, retTree, headerTable, count)  # populate tree with ordered freq itemset
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
            condPats[frozenset(prefixPath[1:])] = treeNode.count
        treeNode = treeNode.nodeLink
    return condPats