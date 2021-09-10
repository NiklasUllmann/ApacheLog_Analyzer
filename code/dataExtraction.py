import numpy as np
import pandas as pd
import re


def getStatusCodeCount(df):
    x = df['status'].value_counts()
    return pd.DataFrame({'status': x.index, 'count': x.values})
    
def getStatusCodeTimeLine(df):

    x = df.groupby(['year', 'month','day', 'status']).size().unstack(level=-1).fillna(0)
    x = x.reset_index()
    x = x.reindex(index=range(0, len(x)))
    d = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dez': 12}
    x['month'] = x['month'].map(d)
    x['date'] = x['year'].apply(str) + '-' + x['month'].apply(str) + '-' + x['day'].apply(str)
    x = x.sort_values(by=['date'])
    x.drop(['year', 'month', 'day'], axis=1, inplace=True)
    return x

def getUsageHours(df):

    x = df.groupby(['hour', 'minute']).size()
    x = x.reset_index(name='counts')
    x['time'] = x['hour'].apply(str) + ':' + x['minute'].apply(str)
    x = x.sort_values(by=['time'])
    x.drop(['hour', 'minute'], axis=1, inplace=True)

    return x

def getUsageDays(df):

    x = df.groupby(['year', 'month','day']).size()
    x = x.reset_index(name='counts')
    x = x.reindex(index=range(0, len(x)))
    d = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dez': 12}
    x['month'] = x['month'].map(d)
    x['date'] = x['year'].apply(str) + '-' + x['month'].apply(str) + '-' + x['day'].apply(str)
    x = x.sort_values(by=['date'])
    x.drop(['year', 'month', 'day'], axis=1, inplace=True)

    return x


def getRequestCount(df):

    x = df.groupby("request").size()
    x = x.reset_index(name='counts')
    x = x.sort_values(by=['counts'], ascending=False)
    x = x[x['request'].str.contains("GET")]
    x = x.head(10)
    x = x.sort_values(by=['counts'], ascending=True)
    return x

def getReferrer(df):

    df['referrer'] = df['referrer'].apply(lambda x: _regex(x))

    df = df.groupby("referrer").size()
    x = df.reset_index(name='counts')
    x = x.sort_values(by=['counts'], ascending=False)



    print(x)


def _regex(ref):
    if ("www" in ref or "http" in ref):
        re.findall
        return re.findall('^(?:https?:\/\/)?(?:[^@\/\n]+@)?(?:www\.)?([^:\/?\n]+)', ref)[0]
    else:
        return ref