import pandas as pd
import numpy as np
import math
data = pd.read_csv('C:/Users/20212392/dbl Dropbox/Evert Bronstring/PC/Documents/Uni/Y2/Q2/Visualization/VISION/airbnb_open_data.csv')
num_not_nans = data['license'].notnull().sum()
#only 2 values in the license column are not an NaN, so we can safely remove this column

# Columns that can be removed:
# license: see above
# country: all listings are in the USA
# country code: see country
# last review: not relevant
del data['license'], data['country'], data['country code'], data['last review']
#there are more columns for which we can discuss removal during the meeting, but these can be removed for sure

#there are some listings where the minimum nights is negative. We remove these listings from the data
for i in range(len(data)):
    if data['minimum nights'][i] < 0:
        data = data.drop(i)

