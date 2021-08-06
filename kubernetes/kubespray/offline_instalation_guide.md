## Preparation on the VM with internet connection

```
sudo yum install -y epel-release.noarch
sudo yum-config-manager --add-repo=https://download.docker.com/linux/centos/docker-ce.repo
sudo yum-config-manager --enable docker-ce-nightly
sudo yum makecache fast
```
```
mkdir ~/docker
cd ~/docker
sudo yumdownloader --resolve docker-ce
tar cvzf ~/docker.tar.gz *
```
> Save `docker.tar.gz` file to be uploaded to offline VM

```
sudo docker save docker.io/cloudifyplatform/premium-cloudify-manager-aio > ~/cloudify-docker-image.tar
```
> Save `cloudify-docker-image.tar` file to be uploaded to offline VM

```
sudo yum install createrepo
sudo yum install yum-utils
sudo mkdir –p ~/ngagk
sudo reposync -g -l -d -m --repoid=base --newest-only --download-metadata --download_path=/home/centos/ngagk/
sudo createrepo ~/ngagk
```
> Save `ngagk` repo to be uploaded to offline VM under `/ngagk`

```
docker save registry:latest | gzip > registry.tar.gz
```
> Save `registry.tar.gz` to be uploaded to offline VM

```
mkdir -p ~/files_repo
cd files_repo
FILE_REPO_DIR=${PWD}
KUBE_VERSION="v1.21.0"
IMAGE_ARCH="amd64"
ETCD_VERSION="v3.4.13"
CNI_VERSION="v0.9.1"
CRICTRL_VERSION="v1.21.0"
CALICO_VERSION="v3.18.4"
CALICO_CTL_VERSION=${CALICO_VERSION}
ANSIBLE_SYSTEM="linux"
cd ${FILE_REPO_DIR}
mkdir -p kubernetes/${KUBE_VERSION} kubernetes/etcd kubernetes/cni kubernetes/cri-tools kubernetes/calico/
curl -L https://dl.k8s.io/release/${KUBE_VERSION}/bin/linux/${IMAGE_ARCH}/kubeadm -o kubernetes/${KUBE_VERSION}/kubeadm
curl -L https://dl.k8s.io/release/${KUBE_VERSION}/bin/linux/${IMAGE_ARCH}/kubectl -o kubernetes/${KUBE_VERSION}/kubectl
curl -L https://dl.k8s.io/release/${KUBE_VERSION}/bin/linux/${IMAGE_ARCH}/kubelet -o kubernetes/${KUBE_VERSION}/kubelet
curl -L https://github.com/etcd-io/etcd/releases/download/${ETCD_VERSION}/etcd-${ETCD_VERSION}-linux-${IMAGE_ARCH}.tar.gz -o kubernetes/etcd/etcd-${ETCD_VERSION}-linux-${IMAGE_ARCH}.tar.gz
curl -L https://github.com/containernetworking/plugins/releases/download/${CNI_VERSION}/cni-plugins-linux-${IMAGE_ARCH}-${CNI_VERSION}.tgz -o kubernetes/cni/cni-plugins-linux-${IMAGE_ARCH}-${CNI_VERSION}.tgz
curl -L https://github.com/kubernetes-sigs/cri-tools/releases/download/${CRICTRL_VERSION}/crictl-${CRICTRL_VERSION}-linux-${IMAGE_ARCH}.tar.gz -o kubernetes/cri-tools/crictl-${CRICTRL_VERSION}-linux-${IMAGE_ARCH}.tar.gz
curl -L https://github.com/projectcalico/calicoctl/releases/download/${CALICO_CTL_VERSION}/calicoctl-linux-${IMAGE_ARCH} -o kubernetes/calico/calicoctl-linux-${IMAGE_ARCH}
curl -L https://github.com/projectcalico/calico/releases/download/${CALICO_VERSION}/release-${CALICO_VERSION}.tgz -o kubernetes/calico/${CALICO_VERSION}.tar.gz
```
> Save `files_repo` directory to be uploaded to offline VM under `/files_repo`


## Preparation on the Kubernetes VMs - MASTER and WORKERS

```
sudo systemctl stop firewalld
sudo systemctl disable firewalld
sudo sed -i 's/DEFROUTE="yes"/DEFROUTE="no"/g' /etc/sysconfig/network-scripts/ifcfg-ens192
sudo mkdir -p /etc/docker/
sudo sh -c "echo '{ \"insecure-registries\":[\"172.16.167.159:5000\"] }' > /etc/docker/daemon.json"
sudo rm /etc/yum.repos.d/CentOS*.repo
sudo sh -c "cat  << EOF >> /etc/yum.repos.d/docker-ce.repo
[docker-ce]
name=Docker-CE Repository
baseurl=http://172.16.167.159:8003
enabled=1
gpgcheck=0
EOF"
sudo sh -c "cat  << EOF > /etc/resolv.conf
nameserver 127.0.0.1
EOF"
```
> This script assumes your Kubernetes Master VM has IP address `172.16.167.159`.


## Preparation on the offline VM - without connection to the internet


TODO: ipaddr and netaddr install on venv
TODO: docker-ce repo -> already mentioned below



> Upload to the offline VM all files, repos and directories specified in previous section

```
mkdir docker
tar xvf docker.tar.gz -C ~/docker
cd docker
sudo rpm -ivh --replacefiles --replacepkgs *.rpm
sudo systemctl enable docker.service
sudo systemctl start docker.service

mkdir ansible
sudo docker load < cloudify-docker-image.tar

sudo systemctl stop firewalld
sudo systemctl disable firewalld

mv /etc/yum.repos.d/*.repo /tmp/
sudo sh -c "cat  << EOF >> /etc/yum.repos.d/remote.repo
[remote]
name=Cloudify lokal yum repository
baseurl=http://127.0.0.1:8001
enabled=1
gpgcheck=0
EOF"

ssh-keygen -f ~/.ssh/ng_demo
ssh-copy-id -i ~/.ssh/ng_demo.pub centos@<<ip_address>
# `ssh-copy-id` command should be performed to the Master and Workers VMs (specify proper IP adresses) 
```

> Upload plugins wagons and yaml files into the `/cm_plugins` directory
> These should be: ansible plugin 2.12.0, docker plugin 2.0.3, fabric plugin 2.0.8, kubernetes plugin 2.13.0, utilities plugin 1.24.4

```
sudo docker run --name cfy_manager_northrop_grumman -d --restart unless-stopped \
  -v /sys/fs/cgroup:/sys/fs/cgroup:ro -v /home/centos/ansible:/ansible_repo:ro -v /home/centos/cm_plugins:/cloudify_plugins:ro \
  -v /home/centos/ngagk_repo:/yum_repo:ro -v /home/centos/files_repo:/files_repo:ro -v /home/centos/docker-ce:/docker-ce:ro \
  --tmpfs /run --tmpfs /run/lock \
  --security-opt seccomp:unconfined --cap-add SYS_ADMIN \
  -p 80:80 -p 443:443 -p 5671:5671 -p 6443:6443 -p 53333:53333 -p 8000:8000 \
  -p 8001:8001 -p 8002:8002 -p 8003:8003 \
  cloudifyplatform/premium-cloudify-manager-aio
```

> Upload a license into the Cloudify Manager (via Web Console or CLI)

> Run http servers INSIDE Cloudify Manager's docker container:
```
cd /yum_repo
nohup python -m SimpleHTTPServer 8001 &
cd /files_repo
nohup python -m SimpleHTTPServer 8002 &
cd /docker-ce
nohup python -m SimpleHTTPServer 8003 &
```

> Upload `tomcat-img.tar.gz` archive into the offline VM and run:
```
sudo docker run -d -p 5000:5000 --restart=always --name registry registry:2
sudo docker image load -i tomcat-img.tar.gz
sudo docker image tag bitnami/tomcat "0.0.0.0:5000/tomcat-serv"
sudo docker push 0.0.0.0:5000/tomcat-serv
```
