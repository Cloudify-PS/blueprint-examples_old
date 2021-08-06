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
> Save `ngagk` repo to be uploaded to offline VM under `/ngagk` directory

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
> Save `files_repo` directory to be uploaded to offline VM under `/files_repo` directory

```
mkdir ~/docker-ce
sudo reposync -l -d -m --repoid=base --newest-only --download-metadata --download_path=/home/centos/docker-ce/
sudo reposync -l -d -m --repoid=extras --newest-only --download-metadata --download_path=/home/centos/docker-ce/
sudo reposync -l -d -m --repoid=docker-ce --newest-only --download-metadata --download_path=/home/centos/docker-ce/
sudo createrepo ~/docker-ce
```
> Save `docker-ce` repo to be uploaded to offline VM under `/docker-ce` directory

```
# Minimum image
sudo /usr/bin/docker pull quay.io/coreos/etcd:v3.4.13
sudo docker image tag quay.io/coreos/etcd:v3.4.13 172.16.167.159:5000/coreos/etcd:v3.4.13
sudo docker push 172.16.167.159:5000/coreos/etcd:v3.4.13
sudo /usr/bin/docker pull quay.io/coreos/flannel:v0.13.0-amd64
sudo docker image tag quay.io/coreos/flannel:v0.13.0-amd64 172.16.167.159:5000/coreos/flannel:v0.13.0-amd64
sudo docker push 172.16.167.159:5000/coreos/flannel:v0.13.0-amd64
sudo /usr/bin/docker pull k8s.gcr.io/pause:3.3
sudo docker image tag k8s.gcr.io/pause:3.3 172.16.167.159:5000/pause:3.3
sudo docker push 172.16.167.159:5000/pause:3.3
sudo /usr/bin/docker pull k8s.gcr.io/coredns:1.7.0
sudo docker image tag k8s.gcr.io/coredns:1.7.0 172.16.167.159:5000/coredns:1.7.0
sudo docker push 172.16.167.159:5000/coredns:1.7.0
sudo /usr/bin/docker pull k8s.gcr.io/dns/k8s-dns-node-cache:1.17.1
sudo docker image tag k8s.gcr.io/dns/k8s-dns-node-cache:1.17.1 172.16.167.159:5000/dns/k8s-dns-node-cache:1.17.1
sudo docker push 172.16.167.159:5000/dns/k8s-dns-node-cache:1.17.1
sudo /usr/bin/docker pull k8s.gcr.io/cpa/cluster-proportional-autoscaler-amd64:1.8.3
sudo docker image tag k8s.gcr.io/cpa/cluster-proportional-autoscaler-amd64:1.8.3 172.16.167.159:5000/cpa/cluster-proportional-autoscaler-amd64:1.8.3
sudo docker push 172.16.167.159:5000/cpa/cluster-proportional-autoscaler-amd64:1.8.3
sudo /usr/bin/docker pull k8s.gcr.io/kube-apiserver:v1.20.7
sudo docker image tag k8s.gcr.io/kube-apiserver:v1.20.7 172.16.167.159:5000/kube-apiserver:v1.20.7
sudo docker push 172.16.167.159:5000/kube-apiserver:v1.20.7
sudo /usr/bin/docker pull docker.io/library/nginx:1.19
sudo docker image tag docker.io/library/nginx:1.19 172.16.167.159:5000/library/nginx:1.19
sudo docker push 172.16.167.159:5000/library/nginx:1.19
sudo /usr/bin/docker pull docker.io/library/haproxy:2.3
sudo docker image tag docker.io/library/haproxy:2.3 172.16.167.159:5000/library/haproxy:2.3
sudo docker push 172.16.167.159:5000/library/haproxy:2.3
sudo /usr/bin/docker pull k8s.gcr.io/kube-controller-manager:v1.20.7
sudo docker image tag k8s.gcr.io/kube-controller-manager:v1.20.7 172.16.167.159:5000/kube-controller-manager:v1.20.7
sudo docker push 172.16.167.159:5000/kube-controller-manager:v1.20.7
sudo /usr/bin/docker pull k8s.gcr.io/kube-scheduler:v1.20.7
sudo docker image tag k8s.gcr.io/kube-scheduler:v1.20.7 172.16.167.159:5000/kube-scheduler:v1.20.7
sudo docker push 172.16.167.159:5000/kube-scheduler:v1.20.7
sudo /usr/bin/docker pull k8s.gcr.io/kube-proxy:v1.20.7
sudo docker image tag k8s.gcr.io/kube-proxy:v1.20.7 172.16.167.159:5000/kube-proxy:v1.20.7
sudo docker push 172.16.167.159:5000/kube-proxy:v1.20.7
```


```
curl "http://repository.cloudifysource.org/cloudify/wagons/cloudify-kubernetes-plugin/2.13.0/cloudify_kubernetes_plugin-2.13.0-centos-Core-py36-none-linux_x86_64.wgn" --output cloudify_kubernetes_plugin-2.13.0-centos-Core-py36-none-linux_x86_64.wgn
curl "http://repository.cloudifysource.org/cloudify/wagons/cloudify-kubernetes-plugin/2.13.0/plugin.yaml" --output kubernetes-plugin.yaml
curl "http://repository.cloudifysource.org/cloudify/wagons/cloudify-fabric-plugin/2.0.8/cloudify_fabric_plugin-2.0.8-centos-Core-py27.py36-none-linux_x86_64.wgn" --output cloudify_fabric_plugin-2.0.8-centos-Core-py27.py36-none-linux_x86_64.wgn
curl "http://repository.cloudifysource.org/cloudify/wagons/cloudify-fabric-plugin/2.0.8/plugin.yaml" --output fabric-plugin.yaml
curl "https://github.com/cloudify-cosmo/cloudify-ansible-plugin/releases/download/2.12.0/cloudify_ansible_plugin-2.12.0-centos-Core-py36-none-linux_x86_64.wgn" --output cloudify_ansible_plugin-2.12.0-centos-Core-py36-none-linux_x86_64.wgn
curl "https://github.com/cloudify-cosmo/cloudify-ansible-plugin/releases/download/2.12.0/plugin.yaml" --output ansible-plugin.yaml
curl "???????" --output cloudify_utilities_plugin-????-centos-Core-py36-none-linux_x86_64.wgn
curl "???????" --output utilities-plugin.yaml
curl "https://files.pythonhosted.org/packages/c3/3b/fe5bda7a3e927d9008c897cf1a0858a9ba9924a6b4750ec1824c9e617587/netaddr-0.8.0.tar.gz" --output netaddr-0.8.0.tar.gz
curl "https://files.pythonhosted.org/packages/9d/a7/1b39a16cb90dfe491f57e1cab3103a15d4e8dd9a150872744f531b1106c1/ipaddr-2.2.0.tar.gz" --output ipaddr-2.2.0.tar.gz
```
> Save `netaddr-0.8.0.tar.gz` and `ipaddr-2.2.0.tar.gz` to be uploaded to offline VM under `/cm_plugins` directory

## Preparation on the Kubernetes VMs - MASTER and WORKERS

```
#!!!! The node has to have a default route (needed by flannel)
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


> Airgap config
```
sudo ip r add 172.16.0.0/16 via 172.16.167.1
sudo ip r del default
```

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
sudo sh -c "cat  << EOF >> /etc/yum.repos.d/docker-ce.repo
[docker-ce]
name=Docker-CE Repository
baseurl=http://127.0.0.1:8003
enabled=1
keepcache=1
gpgkey=https://download.docker.com/linux/centos/gp
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

> Install `netaddr` and `ipaddr` INSIDE Cloudify Manager's docker container:
```
cp /cloudify_plugins/ipaddr-2.2.0.tar.gz /opt/mgmtworker/env/bin/
cp /cloudify_plugins/netaddr-0.8.0.tar.gz /opt/mgmtworker/env/bin/
chmod 744 /opt/mgmtworker/env/bin/activate
cd /opt/mgmtworker/env/bin
./activate
pip3 install ./ipaddr-2.2.0.tar.gz
pip3 install ./netaddr-0.8.0.tar.gz
```

> Upload `tomcat-img.tar.gz` archive into the offline VM and run:
```
sudo docker run -d -p 5000:5000 --restart=always --name registry registry:2
sudo docker image load -i tomcat-img.tar.gz
sudo docker image tag bitnami/tomcat "0.0.0.0:5000/tomcat-serv"
sudo docker push 0.0.0.0:5000/tomcat-serv
```

> Note that majority of the configuration can be automated by a blueprint executed on Cloudify.
