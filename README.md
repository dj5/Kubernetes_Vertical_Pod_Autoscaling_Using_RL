# Kubernetes_Vertical_Pod_Autoscaling_Using_RL
## Setup Kubernetes Cluster

The implementation of FIRM is based on Kubernetes.

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

- [**BOTH NODES**] Disable the swap memory on each server: `sudo swapoff 
-a`.
- [**BOTH NODES**] Assign unique hostname for each server node: `sudo 
hostnamectl set-hostname your_hostname`.
- [**HOST**] Initialize Kubernetes on the master node: `sudo kubeadm init 
--pod-network-cidr=10.244.0.0/16`.
    - Once this command finishes, it will display a `kubeadm join` message 
at the end. Make a note of the whole entry because it will be used to join 
the worker nodes to the cluster.
    - `--pod-network-cidr=10.244.0.0/16` is for the flannel virtual 
network to work.
- [**HOST**] Create a directory for the cluster:
    - `mkdir -p $HOME/.kube`;
    - `sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config`;
    - `sudo chown $(id -u):$(id -g) $HOME/.kube/config`;
- [**HOST**] Deploy pod network to the cluster. A pod network is a way to 
allow communication between different nodes in the cluster.
    - `sudo kubectl apply -f 
https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml`;
    - Verify the pod network is working: `kubectl get pods 
--all-namespaces`;
- [**WORKER**] Connect each worker node to the cluster.
    - `sudo kubeadm join --discovery-token abcdef.1234567890abcdef 
--discovery-token-ca-cert-hash ` (replace the alphanumeric codes with 
those from your master server during initialization);
    - If you forget the command or the token is expired, run `kubeadm 
token create --print-join-command` from the master server to get a new 
token.
- [**MASTER**] Check the worker nodes joined to the clusster: `kubectl get 
nodes`. You should have something like this:



```




