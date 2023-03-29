# Kubernetes_Vertical_Pod_Autoscaling_Using_RL
## Setup Kubernetes Cluster



### Install Docker

- Update the package list: `sudo apt update`.
- Install Docker: `sudo apt install docker.io` 
- Check the installation and version: `docker -v`.

### Start and Enable Docker

- Set Docker to launch at boot: `sudo systemctl enable docker`.
- Verify if Docker is running: `sudo systemctl status docker`.
- Start Docker if it's not running: `sudo systemctl start docker`.

### Install Kubernetes

- Add Kubernetes signing key: `curl -s 
https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add`.
- Add Software Repositories of Kubernetes: `sudo apt-add-repository "deb 
http://apt.kubernetes.io/ kubernetes-xenial main"`.
- Install Kubernetes Admin
    - `sudo apt install kubeadm kubelet kubectl`;
    - `sudo apt-mark hold kubeadm kubelet kubectl`;
    - `kubeadm version` 
- Repeat for all Kubernetes nodes (HOST, WORKER)

### Deploy Kubernetes

**ALL NODES**
 - Disable the swap memory on each server: `sudo swapoff 
-a`.
-  Assign unique hostname for each server node: `sudo 
hostnamectl set-hostname your_hostname`. <br>

**HOST** 
- Initialize Kubernetes on the master node: `sudo kubeadm init 
--pod-network-cidr=10.244.0.0/16`.
    - Once this command finishes, it will display a `kubeadm join` message 
at the end. Make a note of the whole entry because it will be used to join 
the worker nodes to the cluster.
    - `--pod-network-cidr=10.244.0.0/16` is for the flannel virtual 
network to work.
-  Create a directory for the cluster:
    - `mkdir -p $HOME/.kube`;
    - `sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config`;
    - `sudo chown $(id -u):$(id -g) $HOME/.kube/config`;
-  Deploy pod network to the cluster. 
    - `sudo kubectl apply -f 
https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml`;
    - Verify the pod network is working: `kubectl get pods 
--all-namespaces`; <br>

**WORKER** 
- Connect each worker node to the cluster.
    - `sudo kubeadm join --discovery-token abcdef.1234567890abcdef 
--discovery-token-ca-cert-hash ` (replace the alphanumeric codes with 
those from your master server during initialization);
    - If you forget the command or the token is expired, run `kubeadm 
token create --print-join-command` from the master server to get a new 
token.<br>

**HOST** 
 - Check the worker nodes joined to the cluster: `kubectl get 
nodes`. 

## Kubernetes Metric Server Installation Steps 
1. Download the metric server manifest file using the following command:

```arduino

curl -L https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml -o metric-server.yaml
``` 
2. Open the metric-server.yaml file and search for the following lines:

```less

args:
  - --cert-dir=/tmp
  - --secure-port=4443
``` 
3. Add the following line below the lines mentioned in step 2:

```css

- --kubelet-insecure-tls
```

This enables the metric server to communicate with the kubelet securely. 
4. Apply the metric-server.yaml file using the following command:

```

kubectl apply -f metric-server.yaml
``` 
5. Wait for the metric server to start by checking the pod status with the following command:

```sql

kubectl get pods -n kube-system
```

The output should show a running pod for the metric server. 
6. Verify that the metric server is working properly by running the following command:

```css

kubectl top nodes
```
## Apache Benchmark Installation Steps 
1. Check if Apache is already installed on your system using the following command:

```

apache2 -v
```

If Apache is not installed, proceed to step 2. If Apache is already installed, skip to step 4. 
2. Install Apache using the following command:

```sql

sudo apt-get update
sudo apt-get install apache2
```
3. Check the Apache version again using the command in step 1 to verify that it was installed successfully. 
4. Install Apache Benchmark using the following command:

```arduino

sudo apt-get install apache2-utils
``` 
5. Verify that Apache Benchmark was installed successfully by running the following command:

```

ab -V
```
## Steps to start the app


1. Apply deployment and service YAML files using the following commands:     
```
kubectl apply -f ~/demoapp/deployment.yaml
kubectl apply -f ~/demoapp/service.yaml
```
2. Check pod usage with the following command:
```
kubectl top pods
``` 
3. Apply deployment YAML file again with the following command:     
```
kubectl apply -f ~/demoapp/deployment.yaml
```

## To run the load generator, use the following command:

```
sudo python loadgen.py
```

## To run RL, use the following command:

```
sudo python rl.py
```








