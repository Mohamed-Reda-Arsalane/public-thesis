
from Testcases import extract_data
import random


# split list into 2 lists


def splitlist(list):
    list1 = []
    list2 = []
    for i in list:
        list1.append(i[0])
        list2.append(i[1])
    return list1, list2

# merge and shuffle 2 lists


def merge_shuffle(list1, list2):
    list = []
    for i in range(len(list1)):
        list.append(list1[i])
        list.append(list2[i])
    random.shuffle(list)
    return list

# write list to file


def writefile(list, file):
    f = open(file, "w")
    for i in list:
        f.write(str(i)+"\n")
    f.close()

# read lists in each line from file and return list of lists of each list in line


def readfile(file):
    f = open(file, "r")
    result = []
    for i in f:
        list = []
        line = i[1:-3].split(", [")
        # print(line)
        list.append(int(line[0]))
        temp = []
        # print(list)
        for j in line[1].split(", "):
            temp.append(float(j))
        # print(temp)
        list.append(temp)
        # print("test")
        result.append(list)
    f.close()
    return result


file = 'fcomparaison.xlsx'
file1 = "C:\\Users\\moham\\Downloads\\data_malicious_extracted (1).csv"
file2 = "C:\\Users\\moham\Downloads\\data_clean_extracted (1).csv"
malw = extract_data(file1, 1)
writefile(malw, "malfeatures.txt")
begi = extract_data(file2, 0)
writefile(begi, "begfeatures.txt")

#mal = splitlist(readfile("malfeatures.txt"))
#beg = splitlist(readfile("begfeatures.txt"))


#features = merge_shuffle(mal[1], beg[1])
#labels = merge_shuffle(mal[0], beg[0])

# print(labels)
