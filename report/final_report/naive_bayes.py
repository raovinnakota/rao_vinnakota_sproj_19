import pandas as pd
import numpy as np
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression

FILE_NAME = "senate_profile.csv"
FILE_2 = 'house_profile.csv'

def score(output, answers):
    true_pos = 0
    true_neg = 0
    false_pos = 0
    false_neg = 0
    print("Predicted, Actual, Result")
    for i in range(len(answers)):
        if (output[i] == 0 and answers[i] == 0):
            true_neg += 1
        if (output[i] == 1 and answers[i] == 1):
            true_pos += 1
        if (output[i] == 1 and answers[i] == 0):
            false_pos += 1
        if (output[i] == 0 and answers[i] == 1):
            false_neg += 1
    return(true_pos, true_neg, false_pos, false_neg)

senate = pd.read_csv(FILE_NAME)
house = pd.read_csv(FILE_2)
house = house.drop(columns=['Unnamed: 9', 'Unnamed: 10'])
house = house.dropna()
senate = pd.concat([house,senate])
senate = senate.sample(frac=1).reset_index(drop=True)
senate = senate.replace('Dem', 0)
senate = senate.replace('Rep', 1)
senate = senate.replace('Ind', 2)
senate = senate.replace('Misc', 2)
#test_data = senate.sample(frac=1).reset_undex(drop=True)
test_delim = int(0.75 * senate.shape[0])
train_data = np.asarray(senate.loc[:test_delim, 'Count':'Party'])
train_labels = np.asarray(senate.loc[:test_delim, 'Winner'])
test_data = np.asarray(senate.loc[test_delim:, 'Count':'Party'])
test_labels = np.asarray(senate.loc[test_delim:, 'Winner'])

gnb = GaussianNB()
gnb.fit(train_data, train_labels)
output = gnb.predict(test_data)
print(output)
print(test_labels)
probs = gnb.predict_proba(test_data)
true_pos, true_neg, false_pos, false_neg = score(output, test_labels)
print(score(output, test_labels))
print("Accuracy", gnb.score(test_data, test_labels))
