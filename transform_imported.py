# To add a new cell, type '#%%'
# To add a new markdown cell, type '#%% [markdown]'
#%%
import pandas as pd

#%%
df = pd.read_csv('.\\export\\movies.csv')
df.sample(5)

def clean_column(df, label):
    df[label]= df[label].str.replace("(", "")
    df[label]= df[label].str.replace(")", "")
    df[label]= df[label].str.replace("'", "")
    df[label]= df[label].str.replace(",", "")
    return df[label]

#%%
cols_to_clean = [ 'studio', 'gross', 'num_theaters', 'opening', 'open']
for col in cols_to_clean:
    df[col] = clean_column(df, col)

df.head(20)

#%%
