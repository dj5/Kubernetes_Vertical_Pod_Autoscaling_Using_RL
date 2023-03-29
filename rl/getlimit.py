from kubernetes import client, config

# Load the Kubernetes configuration from the default location
def get_limits():
    config.load_kube_config()

    # Create a Kubernetes API client
    api = client.AppsV1Api()

    # Get the deployment by name

    deployment_name = "nginx"
    deployment = api.read_namespaced_deployment(deployment_name, "default")

    # Modify the CPU and memory limits based on the action
    #if action == 0:
        # Decrease CPU and memory limits by 10%
    cpus=float(deployment.spec.template.spec.containers[0].resources.limits['cpu'].split("m")[0])
    memorys=float(deployment.spec.template.spec.containers[0].resources.limits['memory'].split("Mi")[0])
    # print(deployment.spec.template.spec.containers[0].resources.limits['cpu'])
    
    # deployment.spec.template.spec.containers[0].resources.limits['cpu']=cpus 
    # deployment.spec.template.spec.containers[0].resources.limits['memory'] = memorys
    # elif action == 1:
    #     # Increase CPU and memory limits by 10%
    #     deployment.spec.template.spec.containers[0].resources.limits['cpu'] *= 1.1
    #     deployment.spec.template.spec.containers[0].resources.limits['memory'] *= 1.1

    # Update the deployment with the new resource limits
    # api.replace_namespaced_deployment(deployment_name, "default", deployment)
    print("Limit:s ",cpus)
    return cpus,memorys
get_limits()
