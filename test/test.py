import string
import numpy as np
import pandas as pd
import nltk
from math import log


variables_count = 0
casing_ratio = 0
int_count = 0
str_count = 0
macro_keyword = 0
max_operation_count = 0
avg_operation_count = 0
ent = 0.0

typedict = {
    "Long": 0,
    "Word.Paragraph": 0,
    "Byte": 0,
    "Integer": 0
}
variablestypes = []
variables = []
types = []
lower = 1
upper = 0
operation_count = []


with open('checktest.txt') as f:
    content = f.read().replace(' _\n', '').replace('_\n', '')
    contents = content.split("\n")
    contents = [line.lstrip() for line in contents]
    print(contents)


for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    if os.path.isfile(f):
        print()
        print(f.split("\\")[1])
        print(extract(f))
        print("------------------------------------------------------------------")

directory = 'dataset'


def test():
    test = concatenate("test1")
    test = test.replace('\\r', '').replace('_\\n', '')
    test = test.split("\\n")
    for i in test:
        i = i.lstrip()
        if i.strip() != "":
            print(i)


def extract_from_file(string):
    variables_count = 0
    casing_ratio = 0
    int_count = 0
    str_count = 0
    macro_keyword = 0
    max_operation_count = 0
    avg_operation_count = 0
    ent = 0.0
    typedict = {}
    variablestypes = []
    variables = []
    types = []
    comments = []
    strings = []
    lower = 0
    upper = 0
    operation_count = []
    strings = []
    string_text = ""
    with open(string+".txt") as f:
        content = f.read().replace(' _\n', '').replace('_\n', '')
        contents = content.split("\n")
        contents = [line.lstrip() for line in contents]

    for line in contents:
        if "\"" in line:
            i = line.split("\"")
            for j in range(0, len(i)):
                if j % 2 != 0:
                    strings.append(i[j])
                    string_text += " " + i[j]
    string_text = string_text.split()
    for i in contents:
        inline_comment = False
        # need to check all keywords
        if "AutoOpen" in i or "AutoClose" in i or "Document_open" in i or "DocumentOpen" in i or "DocumentClose" in i:
            macro_keyword = 1
        # check if inline comement
        for j in i.split():
            if j.startswith("'") and j not in string_text:
                inline_comment = True
        if i.startswith("'") or inline_comment:
            comments.append(i.split("'")[-1])

    variable_line = [line for line in contents if line.startswith("Dim")]
    for i in variable_line:
        word_list = i.split()
        word_list = [word.replace(',', '') for word in word_list]
        if len(word_list) == 2:
            variablestypes.append(word_list[1].replace(
                '()', '') + ":" + "Undefined")
            variables.append(word.replace('()', ''))
            types.append("Undefined")
            types = list(set(types))
        else:
            if word_list[-3] == "As":
                del word_list[-3]
            del word_list[-2]
            del word_list[0]
            for word in word_list:
                if word != word_list[-1]:
                    variablestypes.append(word.replace(
                        '()', '') + ":" + word_list[-1])
                    variables.append(word.replace('()', ''))
                    types.append(word_list[-1])
                    types = list(set(types))
    for t in types:
        typedict[t] = 0
    for i in variablestypes:
        for t in types:
            if i.split(":")[-1] == t:
                typedict[t] += 1

    for i in variables:
        for j in i:
            if j.islower():
                lower += 1
            else:
                upper += 1

    for i in typedict:
        if i == "Long" or i == "Integer":
            int_count += typedict[i]
        elif i == "String" or i == "Word.Paragraph":
            str_count += typedict[i]
    variables_count = len(variables)
    if variables_count != 0:
        int_count = int_count / variables_count
        str_count = str_count/variables_count
    else:
        int_count = -1
        str_count = -1
    if lower != 0:
        casing_ratio = upper/lower
    else:
        casing_ratio = 200

    ass_line = [line for line in contents if "=" in line and not (
        line.startswith("If") or line.startswith("Set")) and ("-" in line or "+" in line or "/" in line or "&" in line or "*" in line or "^" in line)]

    count = 0

    for i in ass_line:
        count = 0
        for j in i:
            # need to check previous and next char
            if j == "-" or j == "+" or j == "/" or j == "&" or j == "*" or j == "^":
                count += 1
        operation_count.append(count)
    if len(operation_count) > 0:
        max_operation_count = max(operation_count)
        avg_operation_count = sum(operation_count) / len(operation_count)
    else:
        max_operation_count = -1
        avg_operation_count = -1

    stList = list(content)
    alphabet = list(set(stList))
    freqList = []
    for symbol in alphabet:
        ctr = 0
        for sym in stList:
            if sym == symbol:
                ctr += 1
        freqList.append(float(ctr) / len(stList))
    for freq in freqList:
        ent = ent + freq * log(freq, 2)
    ent = -ent

    result = []
    print()
    # print()
    #print("Count of Variables", variables_count)
    #print("% of Integer Variables", int_count)
    #print("% of String Variables", str_count)
    #print("Casing Ratio in Variable Declarations:", casing_ratio)
    #print("Highest Number of Consecutive Mathematical Operations", max_operation_count)
    #print("Average Number of Consecutive Mathematical Operations", avg_operation_count)
    #print("Macro Keywords:", macro_keyword)
    #print('Shannon entropy:', ent)
    # print(comments)
    # print(strings)

    result.append(variables_count)
    result.append(int_count)
    result.append(str_count)
    result.append(casing_ratio)
    result.append(max_operation_count)
    result.append(avg_operation_count)
    result.append(macro_keyword)
    result.append(ent)

    return result
