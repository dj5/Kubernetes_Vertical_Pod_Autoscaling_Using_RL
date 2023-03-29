from kubernetes import client, config
import datetime

# Load Kubernetes configuration from default location
config.load_kube_config()

# Create Kubernetes API client
api = client.CoreV1Api()

# Set the namespace for which you want to fetch metrics
namespace = "default"

# Get list of all pods in the namespace
pods = api.list_namespaced_pod(namespace)

# Create Kubernetes metrics API client
metrics_api = client.MetricsV1beta1Api()

# Print header for the metrics
print("{:<50} {:<10} {:<10}".format("POD", "CPU(cores)", "MEMORY(bytes)"))

# Iterate through all pods and fetch CPU and memory usage metrics
for pod in pods.items:
    # Fetch CPU usage metric
    cpu_usage = metrics_api.list_namespaced_pod_metric(pod.metadata.name, namespace).items[0].containers[0].usage["cpu"]
    cpu_cores = float(cpu_usage.strip("n")) / 1000000000
    # Fetch memory usage metric
    memory_usage = metrics_api.list_namespaced_pod_metric(pod.metadata.name, namespace).items[0].containers[0].usage["memory"]
    memory_bytes = int(memory_usage.strip("Ki")) * 1024
    # Print pod name, CPU usage, and memory usage
    print("{:<50} {:<10.2f} {:<10d}".format(pod.metadata.name, cpu_cores, memory_bytes))

