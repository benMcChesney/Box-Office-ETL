# To add a new cell, type '#%%'
# To add a new markdown cell, type '#%% [markdown]'
#%%
import pandas as pd
import numpy as np

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
print('substitution step')
cols_to_clean = [ 'studio', 'gross', 'num_theaters', 'opening', 'open']
for col in cols_to_clean:
    df[col] = clean_column(df, col)
df['gross'] = df['gross'].str.replace("$", "")
#df['opening'] = df['opening'].str.replace("$", "")

src_studio = ['Col.', 'Par.', 'WB', 'Uni.' , 'BV']
target_studio = [ 'Columbia', 'Paramount', 'Warner Bros.', 'Universal', 'Buena Vista']
for i in range(0,len(src_studio)):
    df[ 'studio' ] =  df[ 'studio' ].str.replace( src_studio[i] , target_studio[i] )
#df['studio'] = df['studio']
# add in full studio names
#df = df.replace(r'^\s*$', np.nan, regex=True)
#df = df.replace(r'^\s*$', np.nan, regex=True)

df['num_theaters'] = df['num_theaters'].replace("N/A", 0)
df['close'] = df['close'].replace("-", np.nan)
df['opening'].fillna('01/01')
df.sample(50)

#%%
df.info()

print('casting columns..')
df['studio'] = df['studio'].astype(str)
df['gross'] = df['gross'].astype(int)
df['num_theaters'] = df['num_theaters'].astype(int)
df['opening'] = df['opening'].astype(str)
#df['opening_dt'] = df['opening'].str.cat(f"/{df['year']}") 
df['title'] = df['title'].astype(str)
df.info()

#%%
