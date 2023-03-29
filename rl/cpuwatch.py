from kubernetes import client, config
import time
import pandas as pd

def metricsCpu():
    config.load_kube_config()
    api = client.CustomObjectsApi()
    cpu = 0
    memory = 0
    cpul = []
    memoryl = []
    k8s_nodes = api.list_cluster_custom_object("metrics.k8s.io", "v1beta1", "pods")

    for stats in k8s_nodes['items']:
        if 'nginx' in stats['metadata']['name']: 
            print("Node Name: %s" % (stats['metadata']['name']))
            print(stats)
            for c in stats['containers']:
                cpul.append(int(c['usage']['cpu'].split('n')[0])/1000000)
                # memoryl.append(int(c['usage']['memory'].split('Ki')[0])*1024/1048576)
                cpu += int(c['usage']['cpu'].split('n')[0])
                # memory += int(c['usage']['memory'].split('Ki')[0]
                # print(cpul,memoryl)
            print("CPU: %s\tMemory: %s" %(max(cpul), 0))
            # Update CPU value in CSV file
            pods_df = pd.DataFrame(columns=['name','cpu','time'])
            pods_df.loc[len(pods_df.index)]=[stats['metadata']['name'],(max(cpul)),time.ctime()]
            pods_df.to_csv('pods.csv', index=False,mode='a')
            time.sleep(31)
            cpul=[]

    return max(cpul), 0

metricsCpu()
