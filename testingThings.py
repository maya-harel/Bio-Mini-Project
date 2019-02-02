import sys

def main():

    constraints = ['1744', '3845', '4603', '1079']
    file = 'C:/Users/User/PycharmProjects/BioMini/inputFiles/cog_words_bac.txt'
    with open(file) as inputFile:
        with open('newFliteredData.txt', 'w+') as newData:
            for line in inputFile:
                lineTemp = line.split('#')[-1]
                genomeNum = lineTemp.split('\t')[0]
                cogList = lineTemp.split('\t')[1:]
                for cog in constraints:
                    if cog not in cogList:
                        break
                    else :
                        newData.write(line)


if __name__ == "__main__":
    main()