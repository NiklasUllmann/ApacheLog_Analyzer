from datetime import datetime
import numpy as np
import pandas as pd
import re
from sklearn.neighbors import KNeighborsRegressor




def getStatusCodeCount(df, q):
    x = df['status'].value_counts()
    x = pd.DataFrame({'status': x.index, 'count': x.values})
    x = x.head(5)
    q.put(x)
    return x

def getOverallStats(df, q):
    allg = {}

    x, y = df.shape
    allg["length"] = x

    top = df.head(1)
    bottom= df.tail(1)

    start = datetime.strptime(str(top.iloc[0]['year']) + '-' + str(top.iloc[0]['month']) + '-' + str(top.iloc[0]['day']), "%Y-%m-%d").date()
    end = datetime.strptime(str(bottom.iloc[0]['year']) + '-' + str(bottom.iloc[0]['month'])+ '-' + str(bottom.iloc[0]['day']), "%Y-%m-%d").date()

    allg["start"] = start
    allg["end"] = end
    delta =  end - start
    delta = delta.days

    allg["delta"] = delta
    q.put(allg)
    return allg

    
def getStatusCodeTimeLine(df, q):

    x = df.groupby(['year', 'month','day', 'status']).size().unstack(level=-1).fillna(0)
    x = x.reset_index()
    x = x.reindex(index=range(0, len(x)))
    x['date'] = x['year'].apply(str) + '-' + x['month'].apply(str) + '-' + x['day'].apply(str)
    x = x.sort_values(by=['date'])
    x.drop(['year', 'month', 'day'], axis=1, inplace=True)
    q.put(x)
    return x

def getUsageHours(df,q):

    
    top = df.head(1)
    bottom= df.tail(1)

    start = datetime.strptime(str(top.iloc[0]['year']) + '-' + str(top.iloc[0]['month']) + '-' + str(top.iloc[0]['day']), "%Y-%m-%d").date()
    end = datetime.strptime(str(bottom.iloc[0]['year']) + '-' + str(bottom.iloc[0]['month'])+ '-' + str(bottom.iloc[0]['day']), "%Y-%m-%d").date()
    delta =  end - start
    delta = delta.days

    x = df
    x['minute'] = x['minute'].apply(lambda x: _minutesToQuarters(x))
    x = x.groupby(['hour', 'minute']).size()
    x = x.reset_index(name='counts')
    x['time'] = x['hour'].apply(str) + ':' + x['minute'].apply(str)
    x = x.sort_values(by=['time'])
    x.drop(['hour', 'minute'], axis=1, inplace=True)

    x['counts'] = x['counts'].div(delta)


    ### Add Trendline
    reg = KNeighborsRegressor(n_neighbors=10).fit(np.vstack(x.index), x['counts'])
    x['bestfit'] = reg.predict(np.vstack(x.index))


    q.put(x)
    return x

def getUsageDays(df, q):

    x = df.groupby(['year', 'month','day']).size()
    x = x.reset_index(name='counts')
    x = x.reindex(index=range(0, len(x)))
    
    x['date'] = x['year'].apply(str) + '-' + x['month'].apply(str) + '-' + x['day'].apply(str)
    x = x.sort_values(by=['date'])
    x.drop(['year', 'month', 'day'], axis=1, inplace=True)

    ### Add Trendline
    reg = KNeighborsRegressor(n_neighbors=5).fit(np.vstack(x.index), x['counts'])
    x['bestfit'] = reg.predict(np.vstack(x.index))
    q.put(x)
    return x


def getRequestCount(df,q):

    x = df.groupby("request").size()
    x = x.reset_index(name='counts')
    x = x.sort_values(by=['counts'], ascending=False)
    x = x[x['request'].str.contains("GET")]
    x = x.head(10)
    x = x.sort_values(by=['counts'], ascending=True)

    q.put(x)
    return x

def getReferrer(df, q):

    df['referrer'] = df['referrer'].apply(lambda x: _regex(x))

    df = df.groupby("referrer").size()
    x = df.reset_index(name='counts')
    x = x.sort_values(by=['counts'], ascending=False)
    x.to_csv("ref_list", sep='\t', encoding='utf-8')

    x = x.head(5)
    q.put(x)

    return x



def _regex(ref):
    if ("www" in ref or "http" in ref):
        re.findall
        return re.findall('^(?:https?:\/\/)?(?:[^@\/\n]+@)?(?:www\.)?([^:\/?\n]+)', ref)[0]
    else:
        return ref

def _minutesToQuarters(x):

    x = int(x)
    if(x >= 0 and x <=15):
        return 0
    elif(x >= 16 and x <=30):
        return 1
    elif(x >= 31 and x <=45):
        return 2
    elif(x >= 46 and x <=60):
        return 3
    else:
        return -1