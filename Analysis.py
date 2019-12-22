# Import packages
from pandas_datareader import data
import pandas as pd
from datetime import date, datetime
import numpy as np
import matplotlib.pyplot as plt

# Define the tickers to be downloaded
tickers = ['EURHUF']

# Define the timeframe
start_date = '1990-01-01'
end_date = date.today().strftime('%Y-%m-%d')

# Alpha Vintage API Key: FC3TWPZYQYBD36XH
# Load data
df_raw_price = data.DataReader(tickers, 'av-daily', start_date, end_date, api_key='FC3TWPZYQYBD36XH')

# Convert the index from string to date time object
df_raw_price.index = pd.to_datetime(df_raw_price.index)

# Shift the index by 5 years and rename the 'close' column to 'five_year_close' and drop all other columns
df_five_year_price = df_raw_price.shift(freq=pd.DateOffset(years=-5))
df_five_year_price.rename(columns={'close': 'five_year_close'}, inplace=True)
df_five_year_price = df_five_year_price.loc[:, 'five_year_close']

# Merge the two dataframe
df_merged = df_raw_price.merge(df_five_year_price, left_index=True, right_index=True)

# Calculate 5-year return
df_merged['five_year_return'] = np.log(df_merged['five_year_close']/df_merged['close'])

# Delete rows where close is 0 or five_year_close is 0
mask = df_merged['close'] == 0
mask2 = df_merged['five_year_close'] == 0
all_filter = mask | mask2
df_merged = df_merged[~all_filter]

mydict = {
    'All': None,
    'Recession': ['2003-06-01', '2004-06-30'],
    'BeforeRecession': ['2006-01-01', '2007-12-31'],
    'RecentWeakness': ['2013-06-01', '2014-12-31']
}


def analysis(df, mydict):
    for key, value in mydict.items():
        if value == None:
            # Descriptive stats
            print(df['five_year_return'].describe())
            # Plot histogram and save it
            plt.figure()
            plt.hist(df['five_year_return'])
            plt.savefig('FiveYearReturnHist.png')
            plt.close()
        else:
            # Check result around the specified time
            df_temp = df.loc[value[0]:value[1]]
            # Repeat the steps as in the previous part of the 'if' condition
            print('Period: {}'.format(key))
            print(df_temp['five_year_return'].describe())
            plt.figure()
            plt.hist(df_temp['five_year_return'])
            plt.savefig('FiveYearReturnHist_{}.png'.format(key))
            plt.close()


if __name__ == '__main__':
    analysis(df_merged, mydict)