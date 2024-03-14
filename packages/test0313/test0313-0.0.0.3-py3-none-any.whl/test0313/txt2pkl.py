# %%
import pandas as pd
import pickle

# %%
def get_new_name(old_name):
    feature_dup = pd.DataFrame(data=old_name.groupby("column_name").cumcount(), columns=["dup_cnt"])
    feature_dup = feature_dup.reset_index()
    new_name = pd.merge(old_name.reset_index(), feature_dup, how='outer')
    new_name["column_name"] = new_name[["column_name", "dup_cnt"]
                                     ].apply(lambda x: x[0] + '_' + str(x[1]) if x[1] > 0 else x[0], axis=1)
    new_name = new_name.drop(["index"], axis=1)
    return new_name

def get_dataset():
    feature_name = pd.read_csv('/workspace/eda_library/UCI HAR Dataset/features.txt',
                             sep='\s+', header=None, names=["column_index", "column_name"])
    new_feature_name = get_new_name(feature_name)
    feature_name = new_feature_name.iloc[:, 1].values.tolist()
    
    X_train = pd.read_csv('/workspace/eda_library/UCI HAR Dataset/train/X_train.txt',
                        sep='\s+', names=feature_name)
    X_test = pd.read_csv('/workspace/eda_library/UCI HAR Dataset/test/X_test.txt',
                        sep='\s+', names=feature_name)
    y_train = pd.read_csv('/workspace/eda_library/UCI HAR Dataset/train/y_train.txt',
                        sep='\s+', header=None, names=["Activity"])
    y_test = pd.read_csv('/workspace/eda_library/UCI HAR Dataset/test/y_test.txt',
                        sep='\s+', header=None, names=["Activity"])
    
    return X_train, X_test, y_train, y_test

X_train, X_test, y_train, y_test = get_dataset()

# %%
X_train["Subject"] = pd.read_csv(
    '/workspace/eda_library/UCI HAR Dataset/train/subject_train.txt', header=None)

train = X_train
train["Activity"] = y_train
# train.sample()

# %%
X_test["Subject"] = pd.read_csv(
    '/workspace/eda_library/UCI HAR Dataset/test/subject_test.txt', header=None)

test = X_test
test["Activity"] = y_test
# test.sample()

# %%
columns = train.columns
columns = columns.str.replace("[()]", "")
columns = columns.str.replace("[-]", "")
columns = columns.str.replace("[,]", "")
train.columns = columns
test.columns = columns
test.columns

# %%

# train.to_csv('/workspace/eda_library/UCI HAR Dataset/train.csv', index=False)
# test.to_csv('/workspace/eda_library/UCI HAR Dataset/test.csv', index=False)

# with open('train.pkl', 'wb') as f:
#     pickle.dump(train, f)
# with open('test.pkl', 'wb') as f:
#     pickle.dump(test, f)

df = pd.merge(train, test, how='left')
with open('uci_har_dataset.pkl', 'wb') as f:
    pickle.dump(df, f)