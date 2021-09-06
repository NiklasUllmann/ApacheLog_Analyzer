import numpy as np
import pandas as pd

def dataPreparation(df):

    # Split time into columns
    df['day'] = df['time'].str.split('/', expand=True)[0]
    df['month'] = df['time'].str.split('/', expand=True)[1]
    df['year'] = df['time'].str.split('/', expand=True)[2].str.split(':', expand=True)[0]
    df['hour'] = df['time'].str.split('/', expand=True)[2].str.split(':', expand=True)[1]
    df['minute'] = df['time'].str.split('/', expand=True)[2].str.split(':', expand=True)[2]
    df = df.drop(columns=['time'])

    return df