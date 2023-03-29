from kubernetes import client, config

# Load the Kubernetes configuration from the default location
config.load_kube_config()

# Create a Kubernetes API client
api = client.AppsV1Api()

# Get the deployment by name
deployment_name = "nginx"
deployment = api.read_namespaced_deployment(deployment_name, "default")

# Modify the CPU and memory requests based on the action
#if action == 0:
    # Decrease CPU and memory requests by 10%
cpus=str(int(deployment.spec.template.spec.containers[0].resources.requests['cpu'].split("m")[0])* 0.9) +'m'
print(deployment.spec.template.spec.containers[0].resources.requests['cpu'])
memorys=str(int(deployment.spec.template.spec.containers[0].resources.requests['memory'].split("Mi")[0])* 0.9) +'Mi'
deployment.spec.template.spec.containers[0].resources.requests['cpu']=cpus 
deployment.spec.template.spec.containers[0].resources.requests['memory'] = memorys
# elif action == 1:
#     # Increase CPU and memory requests by 10%
#     deployment.spec.template.spec.containers[0].resources.requests['cpu'] *= 1.1
#     deployment.spec.template.spec.containers[0].resources.requests['memory'] *= 1.1

# Update the deployment with the new resource requests
api.replace_namespaced_deployment(deployment_name, "default", deployment)

