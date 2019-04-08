import pandas as pd
import numpy as np
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression

FILE_NAME = "senate_profile.csv"

def accuracy(output, answers):
    right = 0
    print("Predicted, Actual, Result")
    for i in range(len(answers)):
        if (output[i] == answers[i]):
            right += 1
            print(output[i], answers[i], "Right")
        else:
            print(output[i], answers[i], "Wrong")
    return(float(right/len(answers)))

senate = pd.read_csv(FILE_NAME)
train_data = np.asarray(senate.loc[:70, 'Count':'Average Compound'])
train_labels = np.asarray(senate.loc[:70, 'Winner'])
test_data = np.asarray(senate.loc[71:, 'Count':'Average Compound'])
test_labels = np.asarray(senate.loc[71:, 'Winner'])

gnb = GaussianNB()
gnb.fit(train_data, train_labels)
output = gnb.predict(test_data)
probs = gnb.predict_proba(test_data)
print(senate.loc[71:, 'Search Term':'Winner'])
print(output)
print(probs)
print(accuracy(output, test_labels))
