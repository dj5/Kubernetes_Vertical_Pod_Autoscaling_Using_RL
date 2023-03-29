from kubernetes import client, config
import time
import  pandas as pd
config.load_kube_config()

api = client.CustomObjectsApi()
a,b=0,0
df= pd.DataFrame(columns=['POD NAME','CPU','Memory','Time'])
#with open('pods.csv', 'a', newline='') as csvfile:
    #spamwriter = csv.writer(csvfile, delimiter=' ',
     #                       quotechar=',', quoting=csv.QUOTE_MINIMAL)
    #spamwriter.writerow(['POD NAME','CPU','Memory'])


while True:
 time.sleep(2)
   #with open('pods.csv', 'w', newline='') as csvfile:
 b=time.time()
 k8s_nodes = api.list_cluster_custom_object("metrics.k8s.io", "v1beta1", "pods")
#print(k8s_nodes)

 for stats in k8s_nodes['items']:
#   print(stats) 
   if 'nginx' in stats['metadata']['name']: 
    print("Node Name: %s" % (stats['metadata']['name']))
    cpu=0
    memory=0
    for c in stats['containers']:
     cpu+=int(c['usage']['cpu'].split('n')[0])
     memory+=int(c['usage']['memory'].split('Ki')[0])

    df.loc[len(df.index)]= [stats['metadata']['name'],cpu,memory,time.ctime()]
    print("CPU: %s\tMemory: %s" %(cpu,memory))
    if a==0 or b-a>15:
      df.to_csv('pods.csv')
       #with open('pods.csv', 'a', newline='') as csvfile:
       #spamwriter = csv.writer(csvfile, delimiter=' ',
        #                    quotechar=',', quoting=csv.QUOTE_MINIMAL)
       #spamwriter.writerow([stats['metadata']['name'],cpu,memory])
      a=time.time()
