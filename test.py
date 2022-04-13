from sklearn import datasets
from sklearn import metrics
from sklearn import svm
from Testcases import extract_data
import random
from sklearn.model_selection import train_test_split
import numpy as np
from tqdm import tqdm
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import RFE, SelectFromModel
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import MinMaxScaler
from sklearn.feature_selection import VarianceThreshold
from sklearn.feature_selection import RFECV
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
from Testcases import extract_dataa


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


def feature_plot(classifier, feature_names, top_features=15):
    coef = classifier.coef_.ravel()
    top_positive_coefficients = np.argsort(coef)[-top_features:]
    top_negative_coefficients = np.argsort(coef)[:top_features]
    top_coefficients = np.hstack(
        [top_negative_coefficients, top_positive_coefficients])
    plt.figure(figsize=(18, 7))
    colors = ['green' if c < 0 else 'blue' for c in coef[top_coefficients]]
    plt.bar(np.arange(2 * top_features), coef[top_coefficients], color=colors)
    feature_names = np.array(feature_names)
    plt.xticks(np.arange(1 + 2 * top_features),
               feature_names[top_coefficients], rotation=45, ha='right')
    plt.show()


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

testcase = extract_dataa(file3)
testcases = testcase[0]
headers = testcase[1]
result = []
labels1 = []

for j in range(len(testcases[0])):
    temp = []
    for c in range(1, len(testcases)):
        temp.append(testcases[c][j])
    result.append(temp)

for i in range(len(result)):
    labels1.append(1)

testcase = extract_dataa(file4)
testcases = testcase[0]
headers = testcase[1]
result1 = []
labels0 = []
for j in range(len(testcases[0])):
    temp = []
    for c in range(1, len(testcases)):
        temp.append(testcases[c][j])
    result1.append(temp)

for i in range(len(result1)):
    labels0.append(0)

features = merge_shuffle(result, result1)
labels = merge_shuffle(labels1, labels0)
features = np.array(features)
try:
    features.head()
except:
    print("error")
print(features.shape)


X_train, X_test, y_train, y_test = train_test_split(
    features, labels, test_size=0.3, random_state=109)

scaler = MinMaxScaler()
scaler.fit(X_train)
X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)
print(X_train.shape)


#m = RFECV(RandomForestClassifier(), scoring='accuracy')
#m.fit(X_train, y_train)
print(X_train.shape)
#print(m.score(X_train, y_train))
#y_pred = m.predict(X_test)
#print("Accuracy RFECV: ", metrics.accuracy_score(y_test, y_pred))
#conf_mat = confusion_matrix(y_test, y_pred)
# print(conf_mat)
#print(classification_report(y_test, y_pred))

# rf_w = RandomForestClassifier(n_estimators=1000)
# print("traning...")
# rf_w.fit(X_train, y_train)
# y_pred_rf_w = rf_w.predict(X_test)
# print(metrics.accuracy_score(y_test, y_pred_rf_w))
# conf_mat = confusion_matrix(y_test, y_pred_rf_w)
# print(conf_mat)
weights = {0: 1.0, 1: 1.0}
clf = svm.SVC(class_weight=weights)
print("traning...")
clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)
print("Accuracy linear SVM : ", metrics.accuracy_score(y_test, y_pred))
conf_mat = confusion_matrix(y_test, y_pred)
print(conf_mat)
print(classification_report(y_test, y_pred))
#feature_plot(clf, inf)

# get the importance of the resulting features.
# importances = rf_w.feature_importances_
# print(importances)
# create a data frame for visualization.
# final_df = pd.DataFrame(
#    {"Features": indexes, "Importances": importances})
# final_df.set_index('Importances')
#
# sort in ascending order to better visualization.
# final_df = final_df.sort_values('Importances')
#
# plot the feature importances in bars.
# plt.figure(figsize=(10, 3))
# plt.xticks(rotation=45)
# sns.barplot(x="Features", y="Importances", data=final_df)
# plt.show()
# plt.savefig('/temp.png')
#
# With feature selection check auuracy with Random Forest
# The following example shows how to retrieve the 7 most informative features
# model_tree = RandomForestClassifier(n_estimators=100, random_state=42)
#
# use RFE to eleminate the less importance features
# sel_rfe_tree = RFE(estimator=model_tree, n_features_to_select=10, step=1)
# X_train_rfe_tree = sel_rfe_tree.fit_transform(X_train, y_train)
# print(sel_rfe_tree.get_support())
# temp = []
# for i in range(len(sel_rfe_tree.get_support())):
# print(i+1, sel_rfe_tree.get_support()[i])
#
#
# print(sel_rfe_tree.ranking_)
# Reduce X to the selected features and then predict using the predict
# y_pred_rf = sel_rfe_tree.predict(X_test)
# print(metrics.accuracy_score(y_test, y_pred_rf))
# conf_mat = confusion_matrix(y_test, y_pred_rf)
# print(conf_mat)


# clf1 = RandomForestClassifier(n_estimators=100)
# clf1.fit(X_train, y_train)
#
# y_pred = clf1.predict(X_test)
#
# print("Accuracy RF : ", metrics.accuracy_score(y_test, y_pred))


# sum += float(metrics.accuracy_score(y_test, y_pred))

# print("sum: ", sum)
# print("average: ", sum/10)
