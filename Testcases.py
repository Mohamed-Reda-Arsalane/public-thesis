from features import extract_testcases
from features import concatenate
from features import extract
from openpyxl import load_workbook
import numpy as np
import pandas as pd
from math import log
from tqdm import tqdm
import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)


# function that extarct all data from ExcelFile
def extract_dataa(file):
    book = load_workbook(file)
    sheet = book.active
    rows = sheet.rows
    col = sheet.columns
    headers = [cell.value for cell in next(rows)]
    testdict = {}
    # print(headers)
    data = []
    next(rows)
    for i in range(len(headers)):
        col1 = [cell.value for cell in next(col)]
        col1 = col1[1::]
        data.append(col1)
    return data, headers


# function to extract  data from csv using panda read_csv
def extractcsvpd(filename):
    data = pd.read_csv(filename)
    name = data['sha256'].tolist()
    code = data['vbaData'].tolist()
    results = []
    results.append(name)
    results.append(code)
    return results


# find indexs of all occurances of each testcases[0] in mydata[0]
def extractcodetest(testcases, mydata):
    indexs = []
    result = []
    c = 0
    for i in range(len(mydata[0])):
        c += 1
        for j in testcases[0]:
            if j == mydata[0][i]:
                temp = []
                indexs.append(i)
                temp.append(mydata[0][i])
                temp.append(mydata[1][i])
                result.append(temp)
    return result


# make function to return a dictionary with testdict[mydata[0][i]] = [mydata[1][i],mydata[2][i]...]
def maketestdict(mydata):
    dict = {}
    for i in range(len(mydata[0])):
        temp = []
        for j in range(1, len(mydata)):
            temp.append(mydata[j][i])
        dict[mydata[0][i]] = temp
    return dict


def makedict(testcode):
    dict = {}
    for i in range(len(testcode)):
        dict[testcode[i][0]] = extract_testcases(concatenate(testcode[i][1]))
    return dict


# compute the percentage of change of 2 values
def changepercent(a, b):
    if a == 0:
        return 0
    else:
        return (b - a) / a * 100


# compute the diffreence between each element of 2 list and return a list of diffreences
def Listdiff(list1, list2):
    diff = []
    for i in range(len(list1)):
        diff.append(changepercent(list1[i], list2[i]))
    return diff


# go throught 2 dictionaries and compute the diffrence bettwen each dict element if they have the same key
def computediffrence(firstdict, seconddict):
    diff = {}
    for key in firstdict:
        if key in seconddict:
            diff[key] = Listdiff(firstdict[key], seconddict[key])
    return diff

# go throught 2 dictionaries and compute the diffrence bettwen each dict element if they have the same key and store the average diffrences in list of dict


def diff(dict1, dict2):
    diff = []
    for key in dict1:
        if key in dict2:
            temp = Listdiff(dict1[key], dict2[key])
            diff.append(temp)
    return diff


def avg_list(list, headers):
    result = []
    printable = []
    for j in range(len(list[0])):
        temp = 0
        h = headers[j+1]
        for i in list:
            temp += i[j]
        strl = h+" : "+str(temp/len(list))
        printable.append(strl)
        result.append(round(temp/len(list), 2))
    return result, printable


def extractcode(testcases, label):
    result = []
    print(len(testcases[0]))
    for j in tqdm(range(10000)):
        temp = []
        # temp.append(testcases[0][j])
        temp.append(label)
        temp.append(extract(concatenate(testcases[1][j])))
        result.append(temp)
    return result


def extract_data(file, label):
    temp = extractcsvpd(file)
    result = extractcode(temp, label)
    return result


def selectfeatures(features, indexs):
    result = []
    length = len(features[0])
    for w in features:
        temp = []
        for i in range(1, len(w)+1):
            if i in indexs:
                temp.append(w[i-1])
        result.append(temp)
    return result


file = 'fcomparaison.xlsx'
file1 = "C:\\Users\\moham\\Downloads\\data_malicious_extracted (1).csv"
file2 = "C:\\Users\\moham\Downloads\\data_clean_extracted (1).csv"
file3 = "C:\\Users\\moham\\OneDrive\\Desktop\\malware\\testcases\\features_malicious.xlsx"
file4 = "C:\\Users\\moham\\OneDrive\\Desktop\\malware\\testcases\\features_clean.xlsx"
#mal = extract_data(file1, 0)
#beg = extract_data(file2, 1)
mal = [[1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4]]
indexes = [1, 3]
mal = selectfeatures(mal, indexes)

#testcase = extract_dataa(file3)
#testcases = testcase[0]
#headers = testcase[1]
#result = []
#labels1 = []
#
# for j in range(len(testcases[0])):
#    temp = []
#    for c in range(1, len(testcases)):
#        temp.append(testcases[c][j])
#    result.append(temp)
#
# for i in range(len(result)):
#    labels1.append(1)
#
#testcase = extract_dataa(file4)
#testcases = testcase[0]
#headers = testcase[1]
#result1 = []
#labels0 = []
# for j in range(len(testcases[0])):
#    temp = []
#    for c in range(1, len(testcases)):
#        temp.append(testcases[c][j])
#    result1.append(temp)
#
# for i in range(len(result1)):
#    labels0.append(1)

#hisdict = maketestdict(testcases)
#mydata = extractcsvpd(file1)
#testcode = extractcodetest(testcases, mydata)
#mydict = makedict(testcode)
#comparaison = diff(mydict, hisdict)
#print(avg_list(comparaison, headers)[0])
# print()
#print(avg_list(comparaison, headers)[1])
