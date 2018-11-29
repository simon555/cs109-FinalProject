
# coding: utf-8

# # Data Cleaning and EDA for Numeric Columns

# **Basic imports**

# In[1]:

get_ipython().magic('matplotlib inline')
import numpy as np
import numpy.random as nd
import pandas as pd
import math
import matplotlib.pyplot as plt

import os
import seaborn as sns
sns.set(style="darkgrid")

from sklearn.linear_model import LogisticRegressionCV
from sklearn.model_selection import cross_val_score
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.preprocessing import Imputer
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from IPython.display import display

from scipy import stats

from collections import Counter

pd.set_option('display.max_columns', None)


# **Additional Imports**

# In[2]:

from IPython.display import display, HTML


# **Load the data**

# In[3]:

inputFile='../../data/smallData/tmp/AcceptedLoans.csv'
data=pd.read_csv(inputFile)
data.head()


# **Check Data Types**

# In[4]:

types = data.dtypes
types.unique()


# **Get Numeric Columns**

# In[5]:

num_cols = types[(types == 'float64') | (types == 'int64') ]
num_cols


# In[6]:

numeric_data = data[num_cols.index]
non_numeric_data = data.drop(num_cols.index, axis = 1)


# In[7]:

len(numeric_data.columns)


# ## CLEAN THE NUMERIC FEATURES

# First we look at summary statistics and missing values.

# In[8]:

numeric_data.describe()


# Observations:
# - some columns are entirely missing or have one entry
# - some columns contain a single value
# - some columns have large outliers

# **Missing Values**

# We'll need to consider missing values in general, but for now, we'll drop all columns that are entirely missing or have one entry.

# In[9]:

col_before = len(numeric_data.columns)
col_not_missing = numeric_data.isna().sum() < (len(numeric_data) - 1)
numeric_data = numeric_data.loc[:,col_not_missing]
col_after = len(numeric_data.columns)

print("columns dropped:", col_before-col_after)


# **Columns that Contain Single Value**

# Are there any columns remaining with a single value?

# In[10]:

numeric_data.loc[:,numeric_data.nunique() == 1]


# In[11]:

numeric_data.nunique()[numeric_data.nunique() == 1]


# These columns should be dropped

# In[12]:

numeric_data = numeric_data.drop(numeric_data.nunique()[numeric_data.nunique() == 1].index, axis = 1)


# **Large Outliers**

# We are looking for outliers that may indicate incorrect data. We will use a Z-score to identify outliers. However, since our dataset is large, we should expect to see quite a bit of deviation from the mean. To set the z-score threshold, we find the maximum value of 103496 draws from a standard normal across 1000 simulations.

# In[13]:

threshold = np.max(np.max(np.random.normal(size = (103496*1000))))
threshold


# In[14]:

outliers = np.abs(stats.zscore(numeric_data)) > threshold


# Which column has outliers?

# In[15]:

outlier_cols = numeric_data.columns[outliers.sum(axis = 0) > 0]
pd.DataFrame({'column_name': numeric_data.columns, 
             'number_of_outliers':outliers.sum(axis = 0)
            })


# Let's see the distribution of the columns with outliers along with the column discription from the data dictionary

# In[16]:

data_dict_df = pd.read_csv('../../data/AcceptedDataDictionary.csv')


# In[17]:

data_dict = dict(zip(data_dict_df.LoanStatNew, data_dict_df.Description))


# In[18]:

fig, axes = plt.subplots(len(outlier_cols), figsize = (10,30))
for idx, ax in enumerate(axes):
    sns.distplot(numeric_data[outlier_cols[idx]], 
                 hist=False,
                 ax=ax,
                 rug = True,
                 rug_kws={"color": "r", "alpha":0.3, "linewidth": 2, "height":0.5 }

                )
    ax.set_title("{}:{}".format(outlier_cols[idx],data_dict[outlier_cols[idx]]))
fig.tight_layout()


# The only outlier that looks particularly strange is the large value of ~55 for `pub_rec`. I will remove it

# In[19]:

numeric_data[numeric_data.pub_rec > 50]


# In[20]:

numeric_data = numeric_data[numeric_data.pub_rec < 50]

