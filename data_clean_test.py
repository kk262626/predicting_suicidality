# %% [markdown]
# # Study 3 Data Preparation
# ### Predictors from Wave 7, self-harm, suicidal ideation and attempts from Wave 8

# %%
import pip
import pyreadstat
import pandas as pd
import numpy as np
pd.options.display.max_rows = 20
from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"

# %%
#Importing the necessary data files
df8=pd.read_csv('~/OneDrive - UNSW/Documents/lsac-data/w78pmn.csv')
lsac8, meta=pyreadstat.read_sas7bdat('~/OneDrive - UNSW/Documents/lsac-data/lsacgrk18.sas7bdat')

# %%
#Extract SITB outcomes from Wave 8 to link to Wave 7 data
sitbs=lsac8[['hicid', 'jhs54b', 'jhs54c', 'jhs54d', 'jhs54g']]
#Outcome was coded as 1 Yes 2 No; recode to 0 No 1 Yes
sitbs=sitbs.rename(columns={'jhs54b':'sh', 'jhs54c':'si', 'jhs54d':'sp' 'jhs54g':'nssi'})
for column in sitbs[1::]:
    sitbs[column].value_counts(dropna=False)
sitbs=sitbs.replace({2:0})
#Creating a dataframe with all SITBs 
df_all=pd.merge(df8, sitbs, how='inner', on='hicid')

# %%
pd.crosstab(index=df_all['nssi'], columns=df_all['att'], dropna=False, margins=True)
pd.crosstab(index=df_all['nssi'], columns=df_all['sh'], dropna=False, margins=True)

# %%
df_all

# %%
df_all=pd.read_csv('df_all.csv')
#Create cross-tabs of outcomes
pd.crosstab(index=df_all['sh'], columns=df_all['si'], dropna=False, margins=True)
pd.crosstab(index=df_all['att'], columns=df_all['sh'], dropna=False, margins=True)
pd.crosstab(index=df_all['att'], columns=df_all['si'], dropna=False, margins=True)
df_all['sitbs']=0
for column in df_all[['att', 'sh', 'si']]:
    df_all['sitbs']=np.where(df_all[column]==1, 1, df_all['sitbs'])
#Dropping any participant which refused to answer any sitb-related questions
df_all=df_all.drop(df_all[df_all.sh<0].index)
df_all=df_all.drop(df_all[df_all.si<0].index)
for column in df_all[['att', 'sh', 'si', 'sitbs']]:
    df_all[column].value_counts()

# %%
#Dropping features with less than 5% of positive responses to reduce the number of redundant features
pd.set_option('display.max_rows', 2000)
df_all2=df_all.select_dtypes(include=['int64'])
dropcols=list(df_all2.columns[df_all2.mean(axis=0)<0.05])

# %%
df_all.columns.get_loc("A01")
df_all.columns.get_loc("hos")

# %%
df_all3=df_all.iloc[:, 1331:1400]
droppbs=df_all3.columns[df_all3.mean(axis=0)<0.05]

# %%
df_all3.shape
droppbs
droppbs.shape

# %%
#Creating the final dataset with redundant features dropped
#s for small
df_alls=df_all.drop(dropcols, axis=1)
df_alls=df_alls.drop(droppbs, axis=1)

# %%
df_alls

# %%
df_alls=pd.read_csv('df_alls.csv')
df_alls=df_alls.drop(columns=['Unnamed: 0', 'hicid'])
Xfull=df_alls.drop(columns=['att','sh', 'si', 'nssi', 'sitbs'])
yfull_all=df_alls[['sh', 'att', 'si', 'nssi', 'sitbs']]

# %%
#Split the data and only perform model development on the 70% training data from here onwards
from sklearn.model_selection import train_test_split
X, X_hold, y, y_hold=train_test_split(Xfull, yfull_all, test_size=0.30, random_state=26, stratify=yfull_all)
X.to_csv('X.csv', index=False)
X_hold.to_csv('X_hold.csv', index=False)
y.to_csv('y.csv', index=False)
y_hold.to_csv('y_hold.csv', index=False)

# %%
#Preparing the outcome datasets for all four models
y_sitbs=y.drop(columns=['sh', 'att', 'si', 'nssi'])
y_sh=y.drop(columns=['att', 'si', 'nssi', 'sitbs'])
y_att=y.drop(columns=['sh', 'si', 'nssi', 'sitbs'])
y_si=y.drop(columns=['sh', 'att', 'nssi', 'sitbs'])
y_sitbs_hold=y_hold.drop(columns=['sh', 'att', 'si', 'nssi'])
y_sh_hold=y_hold.drop(columns=['att', 'si', 'nssi', 'sitbs'])
y_att_hold=y_hold.drop(columns=['sh', 'si', 'nssi', 'sitbs'])
y_si_hold=y_hold.drop(columns=['sh', 'att', 'nssi', 'sitbs'])
y_sitbs.to_csv('y_sitbs.csv', index=False)
y_sitbs_hold.to_csv('y_sitbs_hold.csv', index=False)
y_sh.to_csv('y_sh.csv', index=False)
y_sh_hold.to_csv('y_sh_hold.csv', index=False)
y_att.to_csv('y_att.csv', index=False)
y_att_hold.to_csv('y_att_hold.csv', index=False)
y_si.to_csv('y_si.csv', index=False)
y_si_hold.to_csv('y_si_hold.csv', index=False)

# %%
X=pd.read_csv('X.csv')
#Imputing the training set
# explicitly require this experimental feature
from sklearn.experimental import enable_iterative_imputer  
# now you can import normally from sklearn.impute
from sklearn.impute import IterativeImputer
imputer=IterativeImputer(random_state=26)
imputer.fit(X)
Xi=X
Xi[:]=imputer.transform(Xi)

# %%
#Imputing the holdout set
X_hold=pd.read_csv('X_hold.csv')
from sklearn.experimental import enable_iterative_imputer  
# now you can import normally from sklearn.impute
from sklearn.impute import IterativeImputer
imputer=IterativeImputer(random_state=26)
imputer.fit(X_hold)
Xi_hold=X_hold
Xi_hold[:]=imputer.transform(Xi_hold)

# %%
#Scaling the training dataset
from sklearn import preprocessing
scaler=preprocessing.StandardScaler()
#Storing the numerical columns in a list
nums=['perapp',	'peravoid',	'mastavoid',	'mastapp',	'peerpos',	'peermoral',	'peerpostot',	'hb16c12',	'hb16c12a',	'hb15c10',	'hb15c10a',	'hb26c2',	'hb26c2a',	'hb28c3',	'hb27c2',	'hb16c15b',	'hb31c2',	'hb16c15d',	'se27c1',	're23c1',	'hb16c10',	'calcharm',	'he17c2b2',	'he06c2b2',	'he06c3b2',	'tvweek',	'egweek',	'aanga',	'banga',	'aarga',	'barga',	'pw09a',	'pw09b',	'pw09c',	'pw09a',	'pw09b',	'aextra',	'aagree',	'aconsc',	'aneuro',	'aopen',	'cextra',	'cagree',	'cconsc',	'cneuro',	'copen',	'bextra',	'bagree',	'bconsc',	'bneuro',	'bopen',	'bodyfat',	'cbmi',	'chu9d',	'hb15c13',	'acons',	'bcons',	'bcopar',	'smfq',	'fp06c3',	'fp06c4',	'cfout',	'agambf',	'chshipc',	'ahendb',	'bhendb',	'fn13c10',	'airc',	'birc',	'bk6s',	'atotss',	'fd04c',	'pw04c2',	'noldsib',	'npeople',	'nsasib',	'nsib',	'nyngsib',	'oral',	'asupport',	'bsupport',	'beffic',	'sc11c3c',	'sc11b3c',	'pedsef',	'pedsphy',	'pedspse',	'pedspsd',	'pedspsc',	'pedste',	'pedstd',	'pedstc',	'pedssof',	'pedsscd',	'pedsscc',	'pedsphyb',	'cnfp16',	'fp02c2a',	'hs53a1a',	'apgsi',	'pssm',	'cresl',	'fn13p',	'acondb',	'ccondb',	'bcondb',	'bpsoc',	'aemot',	'cemot',	'bemot',	'ahypr',	'chypr',	'bhypr',	'apeer',	'cpeer',	'bpeer',	'apsoc',	'cpsoc',	'csdqtb',	'bsdqtb',	'cnfsad2',	'sle',	'hb14c2',	'hb13c2b',	'hb13c1b',	'ho06c5',	'numcond',	'hinci',	'hs23c3', 'A01',	'A02',	'A03',	'A04',	'A06',	'A07',	'A09',	'A10',	'A11',	'B01',	'B02',	'B03',	'C01',	'C02',	'C03',	'C07',	'C08',	'C09',	'C10',	'D01',	'D05',	'D06',	'D07',	'D10',	'D11',	'G02',	'G03',	'G04',	'H01',	'H02',	'H03',	'H04',	'J01',	'J02',	'J04',	'J05',	'L01',	'L02',	'L04',	'M01',	'M03',	'M04',	'N02',	'N03',	'N04B',	'N05A',	'N05B',	'N05C',	'N06A',	'N06B',	'N07B',	'P02',	'P03',	'R01',	'R03',	'R05',	'R07',	'S01',	'S02',	'S03',	'V01',	'V06',	'benefit',	'mhcp',	'psychol',	'psychia',	'gp',	'mbs',	'hos',	'y9test',	'y9gram',	'y9num',	'y9read',	'y9spel',	'y9write']
Xicols=Xi.columns.values.tolist()
nums2=list(set(Xicols) & set(nums))
numfs=Xi[nums2]
Xi[nums2]=scaler.fit_transform(numfs.values)
Xi.to_csv('Xi.csv')

# %%
#Scaling the holdout dataset
from sklearn import preprocessing
scaler=preprocessing.StandardScaler()
#Storing the numerical columns in a list
numhs=Xi_hold[nums2]
Xi_hold[nums2]=scaler.fit_transform(numhs.values)
Xi_hold
Xi_hold.to_csv('Xi_hold.csv')


