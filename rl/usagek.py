from getlimit import get_limits
from cpumemory import metricsCpu
import pandas as pd
import time
while True:
    df=pd.read_csv("resource_usage_k8.csv")
    percent=metricsCpu()[0]/get_limits()[0]
    df.loc[len(df.index)]=[percent, time.ctime()]
    df.to_csv("resource_usage_k8.csv",index=False)
    time.sleep(5)
