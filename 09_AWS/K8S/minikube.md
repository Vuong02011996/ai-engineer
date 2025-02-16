# Setup 
# Architecture
+ Cluster
  + Master Node(Control Plane)
    + ETCD : 1 Database kiểu key-value , là một data storage lưu tất cả thông tin ứng dụng(Pods) trên Worker node .
    + Scheduler : Kết nối với API server và ETCD để chọn Worker Node nào có thể triển khai ứng dụng.(không kết nối trực tiếp Worker Node)
    + API server : nhận yêu cầu từ admin kết nối Master Node vs Worker Node 
    + Control Manager : kết nối với API server để làm việc với các Worker Node như replicate , ...
    + Cloud Manager: làm việc với các cloud Provider như AWS, GCP, ...
    + Tất cả các thành phần trên đều là container runtime.
  + Worker Node(Data Plane)
    + 1 Node chứa nhiều Pods 
    + 1 Pods chứa 1 hoặc nhiều container runtime.
    + Kubelet: thuyền trưởng của một Worker Node , quản lý các Pods và giao tiếp với Master Node qua API server 
    + Kube-proxy: Giao tiếp giữa các Pods trong một Worker Node.
  + `1 Cluster có thể có 1 hoặc nhiều Master Node và Worker Node.`
  
## Ràng buộc về Version: 
  + kubelet vs api-server
  + api-server giữa các Master Node 
  + https://kubernetes.io/releases/version-skew-policy/
# Error
+ minikube start
    ```
    Enabling 'default-storageclass' returned an error: running callbacks: [sudo KUBECONFIG=/var/lib/minikube/kubeconfig /var/lib/minikube/binaries/v1.32.0/kubectl apply --force -f /etc/kubernetes/addons/storageclass.yaml: Process exited with status 1
    ```
    minikube delete
