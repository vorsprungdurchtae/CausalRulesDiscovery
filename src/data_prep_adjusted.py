import pandas as pd
import numpy as np

pd.set_option('display.max_columns', None)
from datetime import datetime
from dateutil.parser import parse

#df = pd.DataFrame(data, columns = ['Product','Price','Discount'])
#df = df.sample(n=3)
#every column should be manually modified, thus, columns are selectively processed
#this manually generated data contains duration and the number of companion, and these will be binned to group customers
def read_prep_data(file):

    df = pd.read_csv(r"../data/%s" % file, sep=',')

    #the maximum value from the duration is 28 and minimum is 1, thus, this will be binned in 4 quantiles
    df['BinnedDuration'] = pd.qcut(df['Duration'], 3, labels=['1-9', '10-19', '20-28'])
    df['BinnedDuration'] = df['BinnedDuration'].astype(str)

    #the minimum value of Companion is 1 and maximum 15 -> in 3 Quntiles binned
    df['BinnedCompanion'] = pd.qcut(df['Companion'], 3, labels=['1-5', '6-10', '11-15'])
    df['BinnedCompanion'] = df['BinnedCompanion'].astype(str)
    
    df['AgeCategory'] = df['AgeCategory'].astype(str)
    
    df['Upgrade'] = df['Upgrade'].astype(str)
    df['Reschedule'] = df['Reschedule'].astype(str)
    df['CancellationFee'] = df['CancellationFee'].astype(str)

    df = df.groupby('CustomerID').apply(keep_last)
    df = df.reset_index(drop=True)

    # lower case
    column = ['Accomodation', 'Rating', 'Acitivity']
    for col in column:
        df[col] = df[col].str.lower()
        
    return df


def keep_last(group):
    return group.tail(1)


def get_duration(gr):
    df = pd.DataFrame(gr)
    if len(df[(df["Activity"] == "A_Denied") | (df["Activity"] == "A_Cancelled") | (
            df["Activity"] == "A_Pending")]) > 0:
        df['new_date'] = [datetime.strptime(d, '%Y-%m-%d %H:%M:%S.%f') for d in df['time:timestamp']]

        first_dt = df[df['Activity'] == 'O_Create Offer']['new_date']
        last_dt = \
            df[(df["Activity"] == "A_Denied") | (df["Activity"] == "A_Cancelled") | (df["Activity"] == "A_Pending")][
                'new_date']

        first_dt = first_dt[first_dt.index.values[0]]
        # print(last_dt)
        last_dt = last_dt[last_dt.index.values[0]]

        d1 = parse(str(first_dt))
        d2 = parse(str(last_dt))

        delta_days = (d2 - d1).days
        # print(delta_days,'\n')
        df['durationDays'] = delta_days
        return df
