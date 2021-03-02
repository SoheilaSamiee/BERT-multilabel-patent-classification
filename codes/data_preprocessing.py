# Data preprocessing and splitting
import pandas as pd
import numpy as np

file_path = '../data/all_patents_ipg210105.csv'
#file_path = '../data/tmp/all_patents_ipg210105_3.csv'

dataframe = pd.read_csv(file_path)
dataframe.describe()

# ----------------------------------------------
#        reformatting the dataframe
# ----------------------------------------------
updated_df = pd.DataFrame()
updated_df['label'] = dataframe['sections']
updated_df['application_type_abstract'] = dataframe['application_type']+' '+dataframe['abstract']
updated_df['publication_title_claims'] = dataframe['publication_title']#+' '+dataframe['claims']
#updated_df['description'] = dataframe['descriptions']
# Labels will be reformated in the main code based on classes saved in "data/classes.txt"


# -----------------------------------------------
#        train-val-test split
# -----------------------------------------------
seed = 42
total_len = len(updated_df)
test_ratio = 0.1
val_ratio = 0.1
train_ratio = .8

def train_validate_test_split(df, train_percent=.6, validate_percent=.2, seed=None):
    np.random.seed(seed)
    perm = np.random.permutation(df.index)
    m = len(df.index)
    train_end = int(train_percent * m)
    validate_end = int(validate_percent * m) + train_end
    train = df.iloc[perm[:train_end]]
    validate = df.iloc[perm[train_end:validate_end]]
    test = df.iloc[perm[validate_end:]]
    return train, validate, test

train_set, val_set, test_set = train_validate_test_split(updated_df, train_ratio, val_ratio, seed = 42)


#path = '../data/type_abstrct'
train_set.to_csv('../data/train.csv', index=False)
test_set.to_csv('../data/test.csv', index=False)
val_set.to_csv('../data/val.csv', index=False)

