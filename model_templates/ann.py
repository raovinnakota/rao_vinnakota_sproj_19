import pandas as pd

FILE_NAME = "senate_profile.csv"

senate = pd.read_csv(FILE_NAME)
train_data = senate.loc[:80, 'Count':'Average Compound']
train_labels = senate.loc[:80, 'Winner']
test_data = senate.loc[81:, 'Count':'Average Compound']
test_labels = senate.loc[81:, 'Winner']
