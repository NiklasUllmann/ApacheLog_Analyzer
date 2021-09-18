import numpy as np
import pandas as pd

def dataPreparation(df):

    try:
        # Split time into columns
        df['day'] = df['time'].str.split('/', expand=True)[0]
        df['month'] = df['time'].str.split('/', expand=True)[1]
        df['year'] = df['time'].str.split('/', expand=True)[2].str.split(':', expand=True)[0]
        df['hour'] = df['time'].str.split('/', expand=True)[2].str.split(':', expand=True)[1]
        df['minute'] = df['time'].str.split('/', expand=True)[2].str.split(':', expand=True)[2]
        d = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dez': 12}
        df['month'] = df['month'].map(d)
        df = df.drop(columns=['time'])

        return df

    except:
        raise Exception("Failed to prepare Data")