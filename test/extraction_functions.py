from codecs import backslashreplace_errors
import string
import numpy as np
import pandas as pd
from math import log
import os


def concatenate(foo):
    content = ""
    with open(foo+".txt") as f:
        test = f.read().split("{")
    for i in test:
        i = i.removeprefix("'code': '").rstrip(
        ).removesuffix("]").removesuffix("'}")
        i = i
        if i.strip() != "" and i != "[":
            content += i + "\\n"
    return content


def isword(test):
    words = []
    humanreadable = 0
    for i in test:
        for w in i.replace(",", "").split():  # what is a word
            if (w != "=" and w != ">=" and w != "<=" and w != "<>" and w != "\"\"" and w != "-" and w != "+"
                and w != "/" and w != "&" and w != "*" and w != "^" and w != "#" and w != "(" and w != ")"
                and w != "\\" and w != "[" and w != "]" and w != "\"" and w != "'" and w != "''"
                    and not w.isdecimal() and not w.isdigit()):
                words.append(w)
                print(w)
                if ishumanreadable(w):
                    humanreadable += 1
    return words


def ishumanreadable(word):
    length = len(word)
    if(len(word) < 15):
        alpha = 0
        vowels = 0
        arr = []
        repetition = True
        for ch in word:
            if ch.isalpha():
                alpha += 1
                if(ch == 'A' or ch == 'a' or ch == 'E' or ch == 'e' or ch == 'I'
                   or ch == 'i' or ch == 'O' or ch == 'o' or ch == 'U' or ch == 'u'):
                    vowels += 1
            arr.append(ch)
        for j in range(0, length-1):
            if 3*arr[j] in word:
                repetition = False
        if alpha/length > 0.7 and 0.2 < vowels/length < 0.6 and repetition:
            return True
        else:
            return False
    else:
        return False


def extract(fo):
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
    contents = []
    comments_count = 0
    char_count = 0
    words = []
    words_lenght = []
    avg_word_length = 0
    var_word_length = 0
    mathchar_count = 0
    mathchar_ratio = 0
    codechar_count = 0
    stringchar_count = 0
    stringchar_ratio = 0
    string_length = []
    avg_string_length = 0
    commentline_count = 0
    line_count = 0
    chars_inline = []
    char_inline = 0
    avgchar_inline = 0
    bigline = 0
    wordcount_comment = 0
    whitespace = 0
    backslash = 0
    humanreadable = 0
    comment_word = []
    count = 0
    test = fo.replace('\\r', '').replace('_\\n', '')
    stList = list(fo.replace('\\r', '').replace('\\n', '\n'))
    test = test.split("\\n")
    words = isword(test)
    for i in test:
        i = i.lstrip()
        if i.strip() != "":
            char_inline = 0
            i = i.replace("\\'", "'")
            contents.append(i)
            for j in i:
                char_count += 1
                char_inline += 1
                if j == ' ':
                    whitespace += 1
                if j == '\\':
                    whitespace += 1
                    backslash += 1
            chars_inline.append(char_inline)
            if char_inline >= 150:
                bigline += 1

    for i in words:
        countt = 0
        for w in i:
            if w != "=" and w != "-" and w != "." and w != "+" and w != "/" and w != "&" and w != "*" and w != "^" and w != "#" and w != "(" and w != ")" and w != "\\" and w != "[" and w != "]" and w != "\"" and w != "'":
                countt += 1
        words_lenght.append(countt)

    for line in contents:
        if "\"" in line:
            i = line.split("\"")
            for j in range(0, len(i)):
                if j % 2 != 0:
                    strings.append(i[j])
                    string_text += " " + i[j]

    for i in strings:
        string_length.append(len(i))

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

    for i in comments:
        for j in i:
            comments_count += 1
        for w in i.split():
            if w in words or "'"+w in words:
                wordcount_comment += 1
                comment_word.append(w)

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

# found out that malicious code uses mathematical operation even inside declared string "" so I didn't add if not in Strings
    ass_line = [line for line in contents if "=" in line and not (
        line.startswith("If") or line.startswith("Set"))
        and ("-" in line or "+" in line or "/" in line or "&" in line or "*" in line or "^" in line)]

    for i in ass_line:
        count = 0
        for j in i:
            # need to check previous and next char
            if j == "-" or j == "+" or j == "/" or j == "&" or j == "*" or j == "^":
                count += 1
                # need to know if operator is used as string operator to get appearance frequency of string operators
                mathchar_count += 1
        operation_count.append(count)
    if len(operation_count) > 0:
        max_operation_count = max(operation_count)
        avg_operation_count = sum(operation_count) / len(operation_count)
    else:
        max_operation_count = -1
        avg_operation_count = -1

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

    avg_string_length = sum(string_length) / len(string_length)
    string_text = string_text.split()

    humanreadable = humanreadable/len(words)
    wordcount = len(words)
    avg_word_length = sum(words_lenght) / len(words_lenght)
    var_word_length = np.var(words_lenght)

    whitespace = whitespace/char_count
    backslash = backslash/char_count
    line_count = len(contents)
    avgchar_inline = sum(chars_inline) / len(chars_inline)
    bigline = bigline/line_count

    codechar_count = char_count - comments_count
    mathchar_ratio = mathchar_count/codechar_count
    stringchar_ratio = sum(string_length)/char_count
    commentline_count = len(comments)
    stringcount = len(strings)
    avg_commentline = commentline_count/line_count
    # print(comments)
    # print(comment_word)
    # print(words)
    # print(commentline_count)
    result = []
    print()
    print()

    print("Number of Variables", variables_count)
    print("Number of Integer Variables", int(int_count*variables_count))
    print("Number of String Variables", int(str_count*variables_count))
    print("% of Integer Variables", int_count)
    print("% of String Variables", str_count)
    print("Casing Ratio in Variable Declarations:", casing_ratio)
    print("Number of Mathematical Operations", mathchar_count)
    print("Highest Number of Consecutive Mathematical Operations", max_operation_count)
    print("Average Number of Consecutive Mathematical Operations", avg_operation_count)
    print("Frequency of Mathematical Operations", mathchar_ratio)
    print("Number of words", wordcount)
    print("Average length of words", avg_word_length)
    print("Variance length of words", var_word_length)
    print("Number of words in comments", wordcount_comment)
    print("Number of words not in comments", len(words)-wordcount_comment)
    print("% of words in comments", wordcount_comment/len(words))
    print("% of words not in comments",
          (len(words)-wordcount_comment)/len(words))
    print("Number of char", char_count)
    print("Number of char in code except comments", codechar_count)
    print("% of chars in code except comments", codechar_count/char_count)
    print("Number of line", line_count)
    print("% of lines > 150 chars", bigline)
    print("avg number of char per line", avgchar_inline)
    print("Number of comment", commentline_count)
    print("avg. comments per line", avg_commentline)
    print("Number of chars in comments", comments_count)
    print("% of chars in comments", comments_count/char_count)
    print("Number of string", stringcount)
    print("Number of char in string", sum(string_length))
    print("% of chars belonging to string", stringchar_ratio)
    print("Average length of string", avg_string_length)
    print("Macro Keywords:", macro_keyword)
    print('Shannon entropy:', ent)
    print("% whitespace", whitespace)
    print("% backlash", backslash)
    print("Number of human readable words", humanreadable*len(words))
    print("% of human readable words", humanreadable)

    result.append(variables_count)
    result.append(int(int_count*variables_count))
    result.append(int(str_count*variables_count))
    result.append(int_count)
    result.append(str_count)
    result.append(casing_ratio)
    result.append(mathchar_count)
    result.append(max_operation_count)
    result.append(avg_operation_count)
    result.append(mathchar_ratio)
    result.append(wordcount)
    result.append(avg_word_length)
    result.append(var_word_length)
    result.append(char_count)
    result.append(codechar_count)
    result.append(codechar_count/char_count)
    result.append(commentline_count)
    result.append(comments_count)
    result.append(comments_count/char_count)
    result.append(stringcount)
    result.append(sum(string_length))
    result.append(stringchar_ratio)
    result.append(avg_string_length)
    result.append(macro_keyword)
    result.append(ent)
    result.append(avgchar_inline)
    result.append(line_count)
    result.append(bigline)
    return result


# print(extract(concatenate("test1")))
# print(extract(concatenate("test2")))
# print(extract(concatenate("daba")))
print(extract(concatenate("begin1")))
# print(extract(concatenate("dataset/malware")))
#print("    Dim BQzKAH, QMwyBX, RxJLJDb As Long".lstrip())
