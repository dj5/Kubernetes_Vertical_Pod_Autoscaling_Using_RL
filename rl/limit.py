from kubernetes import client, config

# Load the Kubernetes configuration from the default location
config.load_kube_config()

# Create a Kubernetes API client
api = client.AppsV1Api()

# Get the deployment by name
deployment_name = "nginx"
deployment = api.read_namespaced_deployment(deployment_name, "default")

# Modify the CPU and memory limits based on the action
#if action == 0:
    # Decrease CPU and memory limits by 10%
cpus=str(int(deployment.spec.template.spec.containers[0].resources.limits['cpu'].split("m")[0])* 0.9) +'m'
print(deployment.spec.template.spec.containers[0].resources.limits['cpu'])
memorys=str(int(deployment.spec.template.spec.containers[0].resources.limits['memory'].split("Mi")[0])* 0.9) +'Mi'
deployment.spec.template.spec.containers[0].resources.limits['cpu']=cpus 
deployment.spec.template.spec.containers[0].resources.limits['memory'] = memorys
# elif action == 1:
#     # Increase CPU and memory limits by 10%
#     deployment.spec.template.spec.containers[0].resources.limits['cpu'] *= 1.1
#     deployment.spec.template.spec.containers[0].resources.limits['memory'] *= 1.1

# Update the deployment with the new resource limits
api.replace_namespaced_deployment(deployment_name, "default", deployment)

