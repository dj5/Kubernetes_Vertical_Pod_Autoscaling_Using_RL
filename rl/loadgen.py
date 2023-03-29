import subprocess
import random
import time
import pandas as pd
from getlimit import get_limits
from cpumemory import metricsCpu
count=0
total=0
while True:
    try:
     load=random.randint(1200,15000)
     print(load)
     t=random.randint(0,50)
     command = f"ab -n {str(load)} -c 100 -s 2 http://10.107.122.233/"
     result = subprocess.run(command.split(), stdout=subprocess.PIPE)
     output = result.stdout.decode('utf-8')
     if "apr_socket_recv:" in output:
      print("Output err", output)
      count+=1
     total+=1
     df=pd.read_csv("fail.csv")
     df.loc[len(df.index)]= [count,total]
     df.to_csv("fail.csv",index=False)
     print(output)
     time.sleep(3)
     print("CPU USAGE: ", metricsCpu()[0]/get_limits()[0]*100)
     time.sleep(12)
    except:
      print("")
      df=pd.read_csv("fail.csv")
      count+=1
      total+=1
      df.loc[len(df.index)]= [count,total]
      df.to_csv("fail.csv",index=False)

