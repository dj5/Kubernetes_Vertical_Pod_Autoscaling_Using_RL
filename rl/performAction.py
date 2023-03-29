from kubernetes import client, config

# Load the Kubernetes configuration from the default location
def perform_action(action):
    config.load_kube_config()

    # Create a Kubernetes API client
    api = client.AppsV1Api()

    # Get the deployment by name
    deployment_name = "nginx"
    deployment = api.read_namespaced_deployment(deployment_name, "default")

    # Modify the CPU and memory limits based on the action
    #if action == 0:

        # Decrease CPU and memory limits by 10%
    cpu = int(deployment.spec.template.spec.containers[0].resources.limits['cpu'].split("m")[0])  
    cpus=str(int(cpu)) +'m'
    if action==1 and cpu<2000 :
        print('Action ',action)
        cpu = int(deployment.spec.template.spec.containers[0].resources.limits['cpu'].split("m")[0])*1.3
        cpus=str(int(cpu)) +'m'
        deployment.spec.template.spec.containers[0].resources.limits['cpu']=cpus
        deployment.spec.template.spec.containers[0].resources.requests['cpu']=cpus	
        api.replace_namespaced_deployment(deployment_name, "default", deployment) 
    elif action==0:
        print('Action',action)
        cpu =int(deployment.spec.template.spec.containers[0].resources.limits['cpu'].split("m")[0])*0.7   
        cpus=str(int(cpu)) +'m'
        deployment.spec.template.spec.containers[0].resources.limits['cpu']=cpus 
        deployment.spec.template.spec.containers[0].resources.requests['cpu']=cpus
        api.replace_namespaced_deployment(deployment_name, "default", deployment) 
        #cpu =int(deployment.spec.template.spec.containers[0].resources.limits['cpu'].split("m")[0])*0.9   
        #cpus=str(int(cpu)) +'m'
    else:
        cpu = int(deployment.spec.template.spec.containers[0].resources.limits['cpu'].split("m")[0])
        cpus=str(int(cpu)) +'m'
