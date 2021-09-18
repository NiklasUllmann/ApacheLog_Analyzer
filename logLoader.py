import re
import sys
import numpy as np
import pandas as pd

parts = [
    r'(?P<host>\S+)',                  
    r'\S+',                             
    r'(?P<user>\S+)',                   
    r'\[(?P<time>.+)\]',                
    r'"(?P<request>.*)"',               
    r'(?P<status>[0-9]+)',              
    r'(?P<size>\S+)',                   
    r'"(?P<referrer>.*)"',              
    r'"(?P<agent>.*)"',                 
    ]

def loadLogFileToDF(path):
    pattern = re.compile(r'\s+'.join(parts)+r'\s*\Z')

    log_data = []

    try:

        with open(path) as file:
            lines = file.readlines()
            lines = [line.rstrip() for line in lines]

        for line in lines:
            log_data.append(pattern.match(line).groupdict())
        df = pd.DataFrame(log_data)
        df = df.drop(columns=['host'])

        return df
    except:
        raise Exception("Failed to load file")

    