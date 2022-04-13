from sklearn import metrics
from sklearn import svm
from Testcases import extract_data
import random
from sklearn.model_selection import train_test_split
import numpy as np
from tqdm import tqdm
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import RFE, SelectFromModel, RFECV
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix
from sklearn.preprocessing import MinMaxScaler
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
    # random.shuffle(list)
    return list


def readfile(file):
    f = open(file, "r")
    result = []
    c = 0
    for i in f:
        if c <= 10000:
            # print(c)
            c += 1
            # print(c)
            list = []
            line = i[1:-3].split(", [")
            # print(line)
            list.append(int(line[0]))
            temp = []
            # print(list)
            for j in line[1].split(", "):
                if "." not in j:
                    temp.append(int(j))
                else:
                    temp.append(float(j))
            # print(temp)
            list.append(temp)
            # print("test")
            result.append(list)
    f.close()
    return result


def selectfeatures(features, indexs):
    result = []
    length = len(features[0])
    for w in features:
        for i in w:
            for j in length:
                if j in indexs:
                    result.append(i[j])
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
mal = splitlist(readfile("malfeatures.txt"))
print(len(mal[0]))
beg = splitlist(readfile("begfeatures.txt"))
bol = True
features = merge_shuffle(mal[1], beg[1])
labels = merge_shuffle(mal[0], beg[0])

# for i in range(3):
# print(labels[i])
# print(features[i])


indexes = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27,
           28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54]
#features = selectfeatures(features, indexes)
features = np.array(features)
print(features.shape)

X_train, X_test, y_train, y_test = train_test_split(
    features, labels, test_size=0.3, random_state=109)
print(X_train.shape)

#scaler = MinMaxScaler()
# scaler.fit(X_train)
#X_train = scaler.transform(X_train)
#X_test = scaler.transform(X_test)
# for i in range(3):
# print(X_train[i])

print("traning...")
rf_w = RandomForestClassifier(random_state=100, n_estimators=100)
rf_w.fit(X_train, y_train)
y_pred_rf_w = rf_w.predict(X_test)
print(metrics.accuracy_score(y_test, y_pred_rf_w))
conf_mat = confusion_matrix(y_test, y_pred_rf_w)
print(conf_mat)
importances = rf_w.feature_importances_
final_df = pd.DataFrame(
    {"Features": indexes, "Importances": importances})
final_df.set_index('Importances')
final_df = final_df.sort_values('Importances')
plt.figure(figsize=(10, 3))
plt.xticks(rotation=45)
sns.barplot(x="Features", y="Importances", data=final_df)
# plt.show()


model_tree = RandomForestClassifier(n_estimators=100, random_state=42)
print("RFECV")
sel_rfe_tree = RFECV(estimator=model_tree, step=1)
print("traning...")
X_train_rfe_tree = sel_rfe_tree.fit_transform(X_train, y_train)
print("Training Samples: ", X_train_rfe_tree.shape)
# print(sel_rfe_tree.get_support())
# print(sel_rfe_tree.grid_scores_)
# print(X_train_rfe_tree.shape)
# print(sel_rfe_tree.ranking_)
y_pred_rf = sel_rfe_tree.predict(X_test)
print("Accuracy Random Forest with RFECV : ",
      metrics.accuracy_score(y_test, y_pred_rf))
conf_mat = confusion_matrix(y_test, y_pred_rf)
print("Confusion Matrix:")
print(conf_mat)
#print(classification_report(y_test, y_pred_rf))
